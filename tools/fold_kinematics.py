#!/usr/bin/env python3
"""Shapeshifter fold kinematics — parametric model of the two-stage,
all-vertical-axis 'zig-zag' fold.

Stage 1 (double-back): each side's outer-panel pair + fin rotates about
vertical axes at the mid-span knuckles; the fin is the coupler of a
parallelogram, so it translates without rotating. Outer panels end up
doubled back over the inner panels (raised by the knuckle z-offset).

Stage 2 (scissor): each side's inner-panel pair (carrying the folded
outer bundle) rotates about vertical axes at the wing roots; the folded
bundle is the coupler of the second parallelogram.

All hinge axes are vertical -> panels swing in plan, gravity-neutral.
Flight loads (flapwise bending, torsion) cross every hinge perpendicular
to its free axis and are carried by bearing couples; locks carry only
in-plane moments, which are small.

Outputs: fold sequence geometry, plan-collision report (with z-band
awareness), folded envelope, lock/bearing static loads, actuator sizing.
"""
import numpy as np
import json, sys

P = dict(
    # hull = narrow footwell forward-low + main cabin. The footwell taper is a
    # FOLD REQUIREMENT: the doubled-back front outer panels' trailing edges
    # sweep through y >= 0.20 at z 0.30..0.45 over the first ~0.8 m of hull.
    capsule=dict(L=2.10, W=0.74, z0=0.10, z1=1.50, nose_x=0.0,
                 footwell=dict(x1=0.80, half_w=0.16, z0=0.10, z1=0.50)),
    root_front=dict(x=0.55, z=0.25),
    root_rear=dict(x=2.05, z=1.65),          # stagger 1.50 m, gap 1.40 m
    half_w=0.61,                              # root hinge on a 200 mm fixed stub: LE-corner swing arc (f*c=0.18 m) must clear the capsule wall
    inner_span=2.25, outer_span=2.25, chord=0.72,  # stub 0.24 + 2.25 + 2.25 = 4.74 m half-span; equal spans -> outer folds back onto inner exactly
    hinge_chord_frac=0.25,                    # vertical hinge at 25% chord
    knuckle_dz=0.12,                          # folded outer stacks above inner
    fin_chord=0.35, fin_dz=1.40, fin_dx=1.50,
    nacelle=dict(span_pos=0.83, fwd=0.45, r_folded_prop=0.20),
    psi_fold=177.0,                           # stage-1 angle, deg
    phi_fold=88.0,                            # stage-2 angle, deg
    panel_t=0.11,                             # panel thickness for z-bands
)

def rot(a_deg):
    a = np.radians(a_deg)
    return np.array([np.cos(a), np.sin(a)])

def panel_poly(root_xy, alpha, span, chord, f):
    """Plan rectangle of a panel: root hinge point, span azimuth alpha (deg,
    90 = +y outboard, deployed), hinge at fraction f of chord."""
    s = rot(alpha)
    c = np.array([np.sin(np.radians(alpha)), -np.cos(np.radians(alpha))])  # +x aft when alpha=90
    r = np.array(root_xy)
    le, te = -f * chord, (1 - f) * chord
    return np.array([r + le*c, r + te*c, r + te*c + span*s, r + le*c + span*s])

def rect_poly(x0, y0, x1, y1):
    return np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]])

def seg_poly(p0, p1, width):
    """Rectangle along segment p0->p1 with given width (fin plan footprint)."""
    d = np.array(p1) - np.array(p0)
    L = np.linalg.norm(d)
    if L < 1e-9: d = np.array([1.0, 0.0]); L = 1.0
    d = d / L
    n = np.array([-d[1], d[0]]) * (width/2)
    return np.array([p0+n, p1+n, p1-n, p0-n])

def polys_overlap(A, B):
    """Separating axis test for two convex polygons."""
    for poly in (A, B):
        for i in range(len(poly)):
            e = poly[(i+1) % len(poly)] - poly[i]
            ax = np.array([-e[1], e[0]])
            pa, pb = A @ ax, B @ ax
            if pa.max() < pb.min() or pb.max() < pa.min():
                return False
    return True

def zband_overlap(a, b):
    return not (a[1] < b[0] or b[1] < a[0])

def side_geometry(psi, phi, sweep_sign=+1):
    """All plan polygons + z-bands for the right side at fold state
    (psi: stage-1 angle 0..psi_fold, phi: stage-2 angle 0..phi_fold).
    sweep_sign=+1 sweeps forward (azimuth 90 -> 90+phi), -1 sweeps aft."""
    g = {}
    hw, c, f = P['half_w'], P['chord'], P['hinge_chord_frac']
    a_in = 90 + sweep_sign * phi
    a_out = a_in - psi                       # stage-1 folds tip through aft side
    for name, rp, z in (('front', P['root_front'], P['root_front']['z']),
                        ('rear',  P['root_rear'],  P['root_rear']['z'])):
        root = np.array([rp['x'], hw])
        inner = panel_poly(root, a_in, P['inner_span'], c, f)
        mid = root + P['inner_span'] * rot(a_in)
        outer = panel_poly(mid, a_out, P['outer_span'], c, f)
        tip = mid + P['outer_span'] * rot(a_out)
        zi = (z - P['panel_t']/2, z + P['panel_t']/2)
        zo_off = P['knuckle_dz'] * (psi / P['psi_fold'])   # knuckle ramps offset
        zo = (zi[0] + zo_off, zi[1] + zo_off)
        g[name] = dict(inner=inner, outer=outer, mid=mid, tip=tip, z_in=zi, z_out=zo)
    # fin: coupler between the two tips (parallelogram => translates)
    ft, rt = g['front']['tip'], g['rear']['tip']
    d = (rt - ft); d = d / max(np.linalg.norm(d), 1e-9)
    g['fin'] = dict(poly=seg_poly(ft - 0.15*d, rt + 0.15*d, 0.08),
                    z=(P['root_front']['z'], P['root_rear']['z'] + P['panel_t'] + P['knuckle_dz']))
    # nacelle+folded prop on rear inner panel, forward of LE
    s = rot(a_in)
    ch = np.array([np.sin(np.radians(a_in)), -np.cos(np.radians(a_in))])
    nac_c = (np.array([P['root_rear']['x'], hw]) + P['nacelle']['span_pos'] * s
             + (-f*P['chord'] - P['nacelle']['fwd']) * ch)
    g['nacelle'] = dict(center=nac_c, r=P['nacelle']['r_folded_prop'],
                        z=(P['root_rear']['z'] - 0.06, P['root_rear']['z'] + 0.22))  # nacelle above wing plane
    return g

def capsule_polys():
    """Hull as two boxes: narrow footwell (nose, low) + main cabin."""
    cp = P['capsule']; fw = cp['footwell']
    foot = (rect_poly(cp['nose_x'], -fw['half_w'], fw['x1'], fw['half_w']), (fw['z0'], fw['z1']))
    main = (rect_poly(fw['x1'], -cp['W']/2, cp['nose_x'] + cp['L'], cp['W']/2), (cp['z0'], cp['z1']))
    # cabin above the footwell (canopy slope region), full width but only above z 0.50
    over = (rect_poly(cp['nose_x'] + 0.25, -cp['W']/2, fw['x1'], cp['W']/2), (fw['z1'], cp['z1']))
    return [('footwell', *foot), ('cabin', *main), ('nose-upper', *over)]

def circle_poly(c, r, n=12):
    return np.array([c + r*rot(360*i/n) for i in range(n)])

def collision_report(sweep_sign, n_steps=40):
    """Sweep both stages in sequence; report any capsule conflicts."""
    hull = capsule_polys()
    hits = []
    # stage 1 first (phi=0), then stage 2 (psi=psi_fold)
    states = [(P['psi_fold']*t, 0.0) for t in np.linspace(0, 1, n_steps)] + \
             [(P['psi_fold'], P['phi_fold']*t) for t in np.linspace(0, 1, n_steps)]
    for psi, phi in states:
        g = side_geometry(psi, phi, sweep_sign)
        checks = [('front inner', g['front']['inner'], g['front']['z_in']),
                  ('front outer', g['front']['outer'], g['front']['z_out']),
                  ('rear inner',  g['rear']['inner'],  g['rear']['z_in']),
                  ('rear outer',  g['rear']['outer'],  g['rear']['z_out']),
                  ('fin',         g['fin']['poly'],    g['fin']['z']),
                  ('nacelle/prop', circle_poly(g['nacelle']['center'], g['nacelle']['r']),
                                   g['nacelle']['z'])]
        for name, poly, zb in checks:
            for hname, hpoly, hz in hull:
                if zband_overlap(zb, hz) and polys_overlap(poly, hpoly):
                    hits.append((round(psi,1), round(phi,1), f'{name} vs {hname}'))
    # collapse to first occurrence per member
    seen, out = set(), []
    for psi, phi, name in hits:
        if name not in seen:
            seen.add(name); out.append((name, psi, phi))
    return out

def folded_envelope(sweep_sign):
    g = side_geometry(P['psi_fold'], P['phi_fold'], sweep_sign)
    pts = [h[1] for h in capsule_polys()]
    for k in ('front','rear'):
        pts += [g[k]['inner'], g[k]['outer']]
    pts += [g['fin']['poly'], circle_poly(g['nacelle']['center'], g['nacelle']['r'])]
    allp = np.vstack(pts)
    xmin, xmax = allp[:,0].min(), allp[:,0].max()
    ymax = allp[:,1].max()                       # mirror for left side
    zmax = P['root_rear']['z'] + P['panel_t'] + P['knuckle_dz'] + 0.05
    return dict(length=round(xmax - xmin, 2), width=round(2*ymax, 2),
                height=round(zmax + 0.15, 2),   # + stance allowance
                x_range=(round(xmin,2), round(xmax,2)))

def static_loads():
    """Lock and bearing loads. Box-wing element: root flap bending 0.76 kN·m
    limit (propped beam); mid-span field moment ~0.7x root; ultimate = 1.5x."""
    M_root_ult = 0.76 * 1.5
    M_mid_ult = 0.53 * 1.5
    bear_dz_mid, bear_dz_root = 0.15, 0.20      # knuckle / root spigot bearing spacing
    thrust_max, nac_arm = 275.0, P['nacelle']['span_pos']
    lock_arm = (1 - P['hinge_chord_frac']) * P['chord']  # lock pin at TE
    inplane_mid_ult = 0.10 * 1.5                 # kN·m: drag+maneuver chordwise moment
    return dict(
        mid_bearing_kN=round(M_mid_ult / bear_dz_mid, 1),
        root_bearing_kN=round(M_root_ult / bear_dz_root, 1),
        mid_lock_kN=round(inplane_mid_ult / lock_arm, 2),
        scissor_lock_kN=round(1.5 * thrust_max * nac_arm / 1000 / lock_arm, 2),
        note='flap bending crosses hinges perpendicular -> bearing couples; '
             'locks see only in-plane moments')

def actuator_sizing():
    """Gravity-neutral fold: sizing case is wind on the swinging panel."""
    wind = 4.0                                   # m/s allowed fold wind
    q = 0.5 * 1.225 * wind**2
    A_outer = P['outer_span'] * P['chord'] * 1.4 # + fin share
    arm = P['outer_span'] / 2
    T_wind = q * A_outer * arm
    return dict(fold_wind_limit_ms=wind,
                stage1_Nm=round(2.5 * T_wind, 0),  # margin + friction
                stage2_Nm=round(2.5 * T_wind * 1.8, 0),  # larger swept area
                note='gravity-neutral (vertical axes); size on wind + friction')

if __name__ == '__main__':
    print('=== Shapeshifter fold kinematics ===')
    for label, sgn in (('FORWARD sweep (stage 2 folds wings toward nose)', +1),
                       ('AFT sweep (stage 2 folds wings toward tail)', -1)):
        print(f'\n--- {label} ---')
        hits = collision_report(sgn)
        if hits:
            for name, psi, phi in hits:
                print(f'  COLLISION with capsule: {name} first at psi={psi} phi={phi}')
        else:
            print('  no capsule collisions through full fold sequence')
        env = folded_envelope(sgn)
        print(f'  folded envelope: {env["length"]} x {env["width"]} x {env["height"]} m '
              f'(x {env["x_range"][0]}..{env["x_range"][1]})')
    print('\n--- static loads (ultimate) ---')
    for k, v in static_loads().items(): print(f'  {k}: {v}')
    print('\n--- fold actuator sizing ---')
    for k, v in actuator_sizing().items(): print(f'  {k}: {v}')
