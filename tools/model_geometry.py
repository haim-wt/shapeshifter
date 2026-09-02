#!/usr/bin/env python3
"""Shapeshifter 1:10 printable geometry generator.

Emits STL parts sized for a 256 mm cube bed (Bambu P-series), all in mm:
  - 4 x wing panels (inner/outer, L/R mirrored by symmetry -> print 2 of each)
  - fin blank, root stub, capsule pod
  - hinge lugs for the fold knuckles and root pivots
Wing panels loft the real section (14.3% t/c, 1.2% camber) with the outer
panel's 3 deg washout, carry a 5.2 mm spar hole and a 2.2 mm alignment pin
hole, and print span-vertical (Z = span) — one piece each, 225 mm tall.

Scale rule: geometry is 1:10; loads are NOT (see docs/model-1to10.md).
"""
import numpy as np, trimesh, os, json
from shapely.geometry import Polygon, Point

OUT = os.path.join(os.path.dirname(__file__), '..', 'models', '1to10')
SCALE = 0.1
CHORD = 720 * SCALE                 # 72 mm
INNER, OUTER, STUB = 2250*SCALE, 2250*SCALE, 240*SCALE
SPAR_D, SPAR_X = 5.2, 0.32          # carbon tube hole, at 32% chord
PIN_D, PIN_X = 2.2, 0.65            # alignment/anti-rotation pin at 65% chord
FIN_CHORD, FIN_LEN, FIN_T = 350*SCALE, 2050*SCALE, 0.12
WASHOUT_DEG = 3.0

def naca4(m=0.012, p=0.30, t=0.143, n=80):
    """Closed airfoil outline (unit chord), TE at x=1, upper then lower."""
    x = 0.5*(1-np.cos(np.linspace(0, np.pi, n)))         # cosine spacing
    yt = 5*t*(0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1036*x**4)
    yc = np.where(x < p, m/p**2*(2*p*x - x**2), m/(1-p)**2*((1-2*p) + 2*p*x - x**2))
    dyc = np.where(x < p, 2*m/p**2*(p-x), 2*m/(1-p)**2*(p-x))
    th = np.arctan(dyc)
    xu, yu = x - yt*np.sin(th), yc + yt*np.cos(th)
    xl, yl = x + yt*np.sin(th), yc - yt*np.cos(th)
    pts = np.vstack([np.column_stack([xu, yu])[::-1], np.column_stack([xl, yl])[1:-1]])
    return pts

def section_polygon(chord, twist_deg, holes=True, t=None, symmetric=False):
    """Shapely polygon of one station: airfoil (with holes) rotated by twist
    about the 25% chord point. Units mm. x = chordwise (aft +), y = up."""
    if symmetric:
        pts = naca4(m=0.0, p=0.30, t=t)
    else:
        pts = naca4(t=t) if t else naca4()
    pts = pts * chord
    pivot = np.array([0.25*chord, 0.0])
    a = np.radians(-twist_deg)                               # +twist = nose up
    R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    pts = (pts - pivot) @ R.T + pivot
    hole_list = []
    if holes:
        for frac, d in ((SPAR_X, SPAR_D), (PIN_X, PIN_D)):
            c = (np.array([frac*chord, 0.0]) - pivot) @ R.T + pivot
            # camber-line height at that chord fraction
            hole_list.append(Point(c[0], c[1] + 0.012*chord*0.9).buffer(d/2, resolution=24))
    return Polygon(pts, [list(h.exterior.coords) for h in hole_list])

def loft(polys, z_stations):
    """Loft a list of same-topology shapely polygons at given z into a
    watertight trimesh: side walls between stations, triangulated end caps."""
    rings = []
    for P in polys:
        rings.append([np.array(P.exterior.coords)[:-1]] + [np.array(h.coords)[:-1] for h in P.interiors])
    V, F = [], []
    # walls
    for r in range(len(rings[0])):                       # each ring (outer + holes)
        n = len(rings[0][r])
        base = len(V)
        for k, z in enumerate(z_stations):
            for p in rings[k][r]:
                V.append([p[0], p[1], z])
        for k in range(len(z_stations)-1):
            for i in range(n):
                a = base + k*n + i; b = base + k*n + (i+1) % n
                c = base + (k+1)*n + i; d = base + (k+1)*n + (i+1) % n
                if r == 0: F += [[a, b, d], [a, d, c]]
                else:      F += [[a, d, b], [a, c, d]]    # holes: reversed
    V = np.array(V, float); F = np.array(F, int)
    mesh = trimesh.Trimesh(V, F, process=False)
    # caps via shapely triangulation of first/last polygon
    for idx, z, flip in ((0, z_stations[0], True), (-1, z_stations[-1], False)):
        v2, f2 = trimesh.creation.triangulate_polygon(polys[idx], engine='earcut')
        v3 = np.column_stack([v2, np.full(len(v2), z)])
        if flip: f2 = f2[:, ::-1]
        mesh = trimesh.util.concatenate([mesh, trimesh.Trimesh(v3, f2, process=False)])
    mesh.merge_vertices()
    mesh.fix_normals()
    return mesh

def wing_panel(length, twist_root, twist_tip, name):
    n = 6
    zs = np.linspace(0, length, n)
    polys = [section_polygon(CHORD, twist_root + (twist_tip-twist_root)*k/(n-1)) for k in range(n)]
    m = loft(polys, zs)
    m.export(os.path.join(OUT, f'{name}.stl'))
    return m

def fin_blank():
    polys = [section_polygon(FIN_CHORD, 0, holes=False, t=FIN_T, symmetric=True)]*2
    # fin spar hole 3.2 mm at 30% chord
    ring = Polygon(np.array(polys[0].exterior.coords), [list(Point(0.30*FIN_CHORD, 0).buffer(1.6, resolution=20).exterior.coords)])
    m = loft([ring, ring], [0, FIN_LEN]); m.export(os.path.join(OUT, 'fin_blank.stl')); return m

def root_stub(incidence_deg=0.0, name='root_stub'):
    """Fixed root stub; carries the wing's incidence so decalage is built in
    (front pair +2.5 deg relative to rear)."""
    P = section_polygon(CHORD, incidence_deg)
    m = loft([P, P], [0, STUB]); m.export(os.path.join(OUT, f'{name}.stl')); return m

def superellipse(w, h, zc, n=64, e=2.5):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = (w/2)*np.sign(np.cos(t))*np.abs(np.cos(t))**(2/e)
    y = (h/2)*np.sign(np.sin(t))*np.abs(np.sin(t))**(2/e) + zc
    return Polygon(np.column_stack([x, y]))

def capsule_pod():
    """Hull loft, nose at station 0. Narrow low nose = footwell (fold-critical).
    x_station: (width, height, z_center) in mm at 1:10."""
    st = [(0,   6,  10, 55), (15, 18, 40, 60), (40, 28, 70, 70), (80, 34, 100, 75),
          (110, 58, 125, 80), (140, 74, 140, 80), (180, 74, 140, 80), (210, 56, 118, 80)]
    polys = [superellipse(w, h, zc) for _, w, h, zc in st]
    zs = [s[0] for s in st]
    m = loft(polys, zs); m.export(os.path.join(OUT, 'capsule_pod.stl')); return m

def lug(width=12, height=9, thick=5, hole=3.2, name='hinge_lug'):
    """Hinge lug: rounded plate with pin hole. Glue to panel end faces; two
    lugs + one fork make a knuckle. Print flat, PETG."""
    cy = height - width/2
    arc = [(width/2*np.cos(a), cy + width/2*np.sin(a)) for a in np.linspace(0, np.pi, 17)]
    outline = Polygon([(-width/2, 0), (width/2, 0)] + arc).buffer(0)
    P = Polygon(outline.exterior.coords, [list(Point(0, cy).buffer(hole/2, resolution=20).exterior.coords)])
    m = loft([P, P], [0, thick]); m.export(os.path.join(OUT, f'{name}.stl')); return m

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    parts = {}
    parts['wing_inner'] = wing_panel(INNER, 0.0, 0.0, 'wing_inner')            # print x4 (2 per side, front+rear)
    parts['wing_outer'] = wing_panel(OUTER, 0.0, -WASHOUT_DEG, 'wing_outer')   # print x4
    parts['fin_blank'] = fin_blank()                                          # x2
    parts['root_stub_front'] = root_stub(2.5, 'root_stub_front')              # x2, +2.5 deg decalage
    parts['root_stub_rear'] = root_stub(0.0, 'root_stub_rear')                # x2
    parts['capsule_pod'] = capsule_pod()                                      # x1
    parts['hinge_lug'] = lug()                                                # x24
    parts['hinge_lug_offset'] = lug(height=21, name='hinge_lug_offset')       # knuckle z-offset (12 mm) lugs, x8
    report = {}
    for k, m in parts.items():
        ext = m.extents
        report[k] = dict(watertight=bool(m.is_watertight), volume_cm3=round(float(m.volume)/1000, 2),
                         bbox_mm=[round(float(e), 1) for e in ext], fits_256=bool(np.all(ext <= 256)))
    json.dump(report, open(os.path.join(OUT, 'parts_report.json'), 'w'), indent=1)
    for k, v in report.items(): print(f'{k:20s} watertight={v["watertight"]!s:5s} bbox={v["bbox_mm"]} vol={v["volume_cm3"]} cm3 fits={v["fits_256"]}')
