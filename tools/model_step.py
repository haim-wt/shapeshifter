#!/usr/bin/env python3
"""Shapeshifter 1:10 — true B-rep STEP parts via CadQuery (OpenCascade).

Same geometry as model_geometry.py but as editable solids that import into
Fusion 360 / Onshape / FreeCAD as bodies. Upgrades over the STL version:
  - lug POCKETS cut into every panel end at the hinge axis (25% chord), so
    hinge lugs register instead of being glued by eye
  - spar hole sits on the 25%-chord twist axis (straight through the
    washed-out outer panel), alignment pins are blind holes at each end
Units mm. Output: models/1to10/step/*.step
"""
import numpy as np, os, cadquery as cq, json

OUT = os.path.join(os.path.dirname(__file__), '..', 'models', '1to10', 'step')
S = 0.1
CHORD, INNER, OUTER, STUB = 72.0, 225.0, 225.0, 24.0
PIVOT_X = 0.25                       # hinge axis + spar on the 25% chord line
SPAR_D, PIN_D, PIN_X, PIN_DEPTH = 5.2, 2.2, 0.65, 20.0
POCKET = (5.4, 12.5, 10.0)           # lug pocket: thickness (chordwise), width(vertical? no: spanwise depth), see below
FIN_CHORD, FIN_LEN = 35.0, 205.0
WASHOUT = 3.0

def naca4(m=0.012, p=0.30, t=0.143, n=60, symmetric=False):
    if symmetric: m = 0.0
    x = 0.5*(1-np.cos(np.linspace(0, np.pi, n)))
    yt = 5*t*(0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1036*x**4)
    if m > 0:
        yc = np.where(x < p, m/p**2*(2*p*x - x**2), m/(1-p)**2*((1-2*p) + 2*p*x - x**2))
        dyc = np.where(x < p, 2*m/p**2*(p-x), 2*m/(1-p)**2*(p-x))
    else:
        yc = np.zeros_like(x); dyc = np.zeros_like(x)
    th = np.arctan(dyc)
    up = np.column_stack([x - yt*np.sin(th), yc + yt*np.cos(th)])[::-1]   # TE -> LE upper
    lo = np.column_stack([x + yt*np.sin(th), yc - yt*np.cos(th)])[1:]     # LE -> TE lower
    pts = np.vstack([up, lo])
    pts[0] = [1.0, 0.0006]; pts[-1] = [1.0, -0.0006]                        # blunt TE 0.09 mm
    return pts

def rot_about(pts, deg, pivot):
    a = np.radians(-deg); R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    return (pts - pivot) @ R.T + pivot

def airfoil_pts(chord, twist, t=0.143, symmetric=False):
    pts = naca4(t=t, symmetric=symmetric) * chord
    return rot_about(pts, twist, np.array([PIVOT_X*chord, 0.0]))

def loft_airfoil(chord, length, twist_root, twist_tip, n=5, t=0.143, symmetric=False):
    wp = cq.Workplane("XY")
    zs = np.linspace(0, length, n)
    for k, z in enumerate(zs):
        tw = twist_root + (twist_tip - twist_root) * k/(n-1)
        pts = [tuple(p) for p in airfoil_pts(chord, tw, t, symmetric)]
        wp = wp.workplane(offset=(z if k == 0 else zs[k]-zs[k-1])).spline(pts).close()
    return wp.loft(ruled=False, combine=True)

def cyl(x, y, z0, d, h):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(d/2).extrude(h)

def wing_panel(length, tw_root, tw_tip, name):
    body = loft_airfoil(CHORD, length, tw_root, tw_tip)
    cy = 0.012*CHORD*0.9
    # spar: straight hole on the twist axis (25% chord), through
    body = body.cut(cyl(PIVOT_X*CHORD, cy, -1, SPAR_D, length + 2))
    # alignment pins: blind holes from each end, in the local (twisted) frame
    for z0, tw, sgn in ((0.0, tw_root, +1), (length, tw_tip, -1)):
        p = rot_about(np.array([[PIN_X*CHORD, cy]]), tw, np.array([PIVOT_X*CHORD, 0.0]))[0]
        body = body.cut(cyl(p[0], p[1], z0 - (1 if sgn > 0 else PIN_DEPTH), PIN_D, PIN_DEPTH + 1))
    # lug pockets at each end: slot centred on the hinge axis, thickness across the chord,
    # open to the end face, 10 mm deep spanwise, full airfoil height (through)
    for z0, tw, sgn in ((0.0, tw_root, +1), (length, tw_tip, -1)):
        pocket = (cq.Workplane("XY").workplane(offset=(z0 - 1) if sgn > 0 else (z0 - POCKET[2]))
                  .center(PIVOT_X*CHORD, 0).rect(POCKET[0], 40).extrude(POCKET[2] + 1)
                  .rotate((PIVOT_X*CHORD, 0, 0), (PIVOT_X*CHORD, 0, 1), -tw))
        body = body.cut(pocket)
    body = body.val()
    export(body, name); return body

def fin_blank():
    body = loft_airfoil(FIN_CHORD, FIN_LEN, 0, 0, n=2, t=0.12, symmetric=True)
    body = body.cut(cyl(0.30*FIN_CHORD, 0, -1, 3.2, FIN_LEN + 2)).val()
    export(body, 'fin_blank'); return body

def root_stub(incidence, name):
    body = loft_airfoil(CHORD, STUB, incidence, incidence, n=2)
    cy = 0.012*CHORD*0.9
    body = body.cut(cyl(PIVOT_X*CHORD, cy, -1, 3.2, STUB + 2))          # vertical-pivot pin bore (root pivot)
    body = body.val(); export(body, name); return body

def superellipse_pts(w, h, zc, n=48, e=2.5):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = (w/2)*np.sign(np.cos(t))*np.abs(np.cos(t))**(2/e)
    y = (h/2)*np.sign(np.sin(t))*np.abs(np.sin(t))**(2/e) + zc
    return [(float(a), float(b)) for a, b in zip(x, y)]

def capsule_pod():
    st = [(0, 6, 10, 55), (15, 18, 40, 60), (40, 28, 70, 70), (80, 34, 100, 75),
          (110, 58, 125, 80), (140, 74, 140, 80), (180, 74, 140, 80), (210, 56, 118, 80)]
    wp = cq.Workplane("XY"); prev = 0
    for x, w, h, zc in st:
        wp = wp.workplane(offset=x - prev).spline(superellipse_pts(w, h, zc), periodic=True, makeWire=True); prev = x
    body = wp.loft(ruled=False).val(); export(body, 'capsule_pod'); return body

def lug(height, name, width=12.0, thick=5.0, hole=3.2):
    cy = height - width/2
    body = (cq.Workplane("XY").moveTo(-width/2, 0).lineTo(width/2, 0).lineTo(width/2, cy)
            .threePointArc((0, cy + width/2), (-width/2, cy)).close().extrude(thick)
            .faces(">Z").workplane().center(0, cy).hole(hole)).val()
    export(body, name); return body

def export(solid, name):
    os.makedirs(OUT, exist_ok=True)
    cq.exporters.export(cq.Workplane("XY").add(solid), os.path.join(OUT, f'{name}.step'))

if __name__ == '__main__':
    parts = {
        'wing_inner': wing_panel(INNER, 0, 0, 'wing_inner'),
        'wing_outer_R': wing_panel(OUTER, 0, -WASHOUT, 'wing_outer_R'),
        'fin_blank': fin_blank(),
        'root_stub_front': root_stub(2.5, 'root_stub_front'),
        'root_stub_rear': root_stub(0.0, 'root_stub_rear'),
        'capsule_pod': capsule_pod(),
        'hinge_lug': lug(9.0, 'hinge_lug'),
        'hinge_lug_offset': lug(21.0, 'hinge_lug_offset'),
    }
    # left outer = mirror of right outer across the SPAN-normal plane (z -> -z),
    # then shifted back to z = 0..225. Mirroring X would reverse the chord.
    mirrored = cq.Workplane("XY").add(parts['wing_outer_R']).mirror("XY").translate((0, 0, OUTER)).val()
    export(mirrored, 'wing_outer_L'); parts['wing_outer_L'] = mirrored
    rep = {}
    for k, b in parts.items():
        bb = b.BoundingBox()
        rep[k] = dict(valid=bool(b.isValid()), volume_cm3=round(b.Volume()/1000, 2),
                      bbox=[round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1)])
        print(f'{k:18s} valid={rep[k]["valid"]!s:5s} bbox={rep[k]["bbox"]} vol={rep[k]["volume_cm3"]} cm3')
    json.dump(rep, open(os.path.join(OUT, 'parts_report.json'), 'w'), indent=1)
