# Shapeshifter 1:10 — Fusion 360 script (Python API)
#
# Builds the 1:10 model natively and parametrically inside Fusion 360:
# one component per part, real lofts from airfoil splines, spar/pin holes,
# hinge-lug pockets, and user parameters (Modify > Change Parameters) so the
# whole model regenerates when you edit chord, spans, washout, or decalage.
#
# Install: copy this folder to
#   Win: %APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\
#   Mac: ~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/
# then Utilities > Add-Ins > Scripts > Shapeshifter1to10 > Run, in a NEW design.
#
# NOTE: written without a Fusion instance to test against — if it throws,
# send the traceback (it is shown in a message box) and it will be fixed.

import adsk.core, adsk.fusion, traceback, math

# ---------------- parameters (mm) ----------------
PARAMS = [  # (name, value_mm, comment)
    ('ss_chord', 72.0, 'wing chord'),
    ('ss_inner', 225.0, 'inner panel span'),
    ('ss_outer', 225.0, 'outer panel span'),
    ('ss_stub', 24.0, 'fixed root stub'),
    ('ss_washout', 3.0, 'outer panel washout, deg (unitless param)'),
    ('ss_decalage', 2.5, 'front-pair incidence over rear, deg'),
    ('ss_spar_d', 5.2, 'carbon spar hole'),
    ('ss_pin_d', 2.2, 'alignment pin hole'),
    ('ss_fin_chord', 35.0, 'fin chord'),
    ('ss_fin_len', 205.0, 'fin length (slant)'),
    ('ss_pocket_t', 5.4, 'lug pocket thickness'),
    ('ss_pocket_d', 10.0, 'lug pocket depth (spanwise)'),
]
PIVOT_X, PIN_X = 0.25, 0.65          # chord fractions: hinge/spar axis, pin
T_C, CAMBER, CAMBER_POS = 0.143, 0.012, 0.30

def mm(v):            # Fusion internal length unit is cm
    return v / 10.0

def naca(t=T_C, m=CAMBER, p=CAMBER_POS, n=40):
    pts = []
    for i in range(n):
        x = 0.5 * (1 - math.cos(math.pi * i / (n - 1)))
        yt = 5*t*(0.2969*math.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1036*x**4)
        if m > 0:
            yc = m/p**2*(2*p*x - x**2) if x < p else m/(1-p)**2*((1-2*p) + 2*p*x - x**2)
            dyc = 2*m/p**2*(p-x) if x < p else 2*m/(1-p)**2*(p-x)
        else:
            yc, dyc = 0.0, 0.0
        th = math.atan(dyc)
        pts.append(((x - yt*math.sin(th), yc + yt*math.cos(th)), (x + yt*math.sin(th), yc - yt*math.cos(th))))
    upper = [u for u, _ in pts][::-1]          # TE -> LE
    lower = [l for _, l in pts][1:]            # LE -> TE
    out = upper + lower
    out[0] = (1.0, 0.0006); out[-1] = (1.0, -0.0006)
    return out

def rot(pts, deg, pivot):
    a = math.radians(-deg); c, s = math.cos(a), math.sin(a)
    return [(pivot[0] + (x-pivot[0])*c - (y-pivot[1])*s, pivot[1] + (x-pivot[0])*s + (y-pivot[1])*c) for x, y in pts]

def offset_plane(comp, z_mm):
    planes = comp.constructionPlanes
    inp = planes.createInput()
    inp.setByOffset(comp.xYConstructionPlane, adsk.core.ValueInput.createByReal(mm(z_mm)))
    return planes.add(inp)

def closed_spline_sketch(comp, plane, pts_mm, close_with_line=True):
    sk = comp.sketches.add(plane)
    coll = adsk.core.ObjectCollection.create()
    for x, y in pts_mm:
        coll.add(adsk.core.Point3D.create(mm(x), mm(y), 0))
    spl = sk.sketchCurves.sketchFittedSplines.add(coll)
    if close_with_line:
        sk.sketchCurves.sketchLines.addByTwoPoints(spl.endSketchPoint, spl.startSketchPoint)
    else:
        spl.isClosed = True
    return sk

def airfoil_sketch(comp, plane, chord, twist, t=T_C, m=CAMBER):
    pts = [(x*chord, y*chord) for x, y in naca(t=t, m=m)]
    pts = rot(pts, twist, (PIVOT_X*chord, 0.0))
    return closed_spline_sketch(comp, plane, pts)

def loft(comp, sketches):
    lofts = comp.features.loftFeatures
    li = lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    for sk in sketches:
        li.loftSections.add(sk.profiles.item(0))
    li.isSolid = True
    return lofts.add(li).bodies.item(0)

def cut_circle_through(comp, plane, x_mm, y_mm, d_mm):
    sk = comp.sketches.add(plane)
    sk.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(mm(x_mm), mm(y_mm), 0), mm(d_mm/2))
    ext = comp.features.extrudeFeatures
    ei = ext.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    ei.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
    ext.add(ei)

def cut_distance(comp, plane, profile_fn, dist_mm):
    sk = comp.sketches.add(plane)
    profile_fn(sk)
    ext = comp.features.extrudeFeatures
    ei = ext.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(mm(dist_mm)))
    ext.add(ei)

def rect_profile(cx, cy, w, h, deg=0.0):
    def fn(sk):
        corners = [(cx-w/2, cy-h/2), (cx+w/2, cy-h/2), (cx+w/2, cy+h/2), (cx-w/2, cy+h/2)]
        corners = rot(corners, deg, (cx, cy))
        lines = sk.sketchCurves.sketchLines
        p = [adsk.core.Point3D.create(mm(x), mm(y), 0) for x, y in corners]
        for i in range(4):
            lines.addByTwoPoints(p[i], p[(i+1) % 4])
    return fn

def new_component(root, name, x_offset_mm=0.0):
    tr = adsk.core.Matrix3D.create()
    tr.translation = adsk.core.Vector3D.create(mm(x_offset_mm), 0, 0)
    occ = root.occurrences.addNewComponent(tr)
    occ.component.name = name
    return occ.component

def wing_panel(root, name, x_off, chord, length, tw_root, tw_tip, spar_d, pin_d, pocket_t, pocket_d, n=5):
    comp = new_component(root, name, x_off)
    sks = []
    for k in range(n):
        z = length * k / (n-1)
        tw = tw_root + (tw_tip - tw_root) * k / (n-1)
        plane = comp.xYConstructionPlane if k == 0 else offset_plane(comp, z)
        sks.append(airfoil_sketch(comp, plane, chord, tw))
    loft(comp, sks)
    cy = CAMBER * chord * 0.9
    cut_circle_through(comp, comp.xYConstructionPlane, PIVOT_X*chord, cy, spar_d)          # spar on twist axis
    tip_plane = offset_plane(comp, length)
    for plane, tw, sign in ((comp.xYConstructionPlane, tw_root, +1), (tip_plane, tw_tip, -1)):
        px, py = rot([(PIN_X*chord, cy)], tw, (PIVOT_X*chord, 0.0))[0]
        cut_distance(comp, plane, lambda sk, px=px, py=py: sk.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(mm(px), mm(py), 0), mm(pin_d/2)), sign*20.0)
        cut_distance(comp, plane, rect_profile(PIVOT_X*chord, 0.0, pocket_t, 40.0, tw), sign*pocket_d)
    return comp

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get(); ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox('Open a (new) Fusion design first.'); return
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = design.rootComponent
        up = design.userParameters
        vals = {}
        for name, val, comment in PARAMS:
            unit = '' if 'deg' in comment else 'mm'
            if not up.itemByName(name):
                up.add(name, adsk.core.ValueInput.createByReal(mm(val) if unit == 'mm' else val), unit, comment)
            vals[name] = val
        c, spar, pin = vals['ss_chord'], vals['ss_spar_d'], vals['ss_pin_d']
        pt, pd = vals['ss_pocket_t'], vals['ss_pocket_d']

        wing_panel(root, 'wing_inner', 0, c, vals['ss_inner'], 0, 0, spar, pin, pt, pd)
        outer = wing_panel(root, 'wing_outer_R', 100, c, vals['ss_outer'], 0, -vals['ss_washout'], spar, pin, pt, pd)
        # left outer = mirror across the span-normal plane (chiral washout)
        mirrors = outer.features.mirrorFeatures
        coll = adsk.core.ObjectCollection.create(); coll.add(outer.bRepBodies.item(0))
        mi = mirrors.createInput(coll, outer.xYConstructionPlane)
        mirrors.add(mi)
        outer.bRepBodies.item(0).name = 'wing_outer_R'
        if outer.bRepBodies.count > 1: outer.bRepBodies.item(1).name = 'wing_outer_L'

        # root stubs carry decalage
        for name, inc, xo in (('root_stub_front', vals['ss_decalage'], 200), ('root_stub_rear', 0.0, 260)):
            comp = new_component(root, name, xo)
            sk = airfoil_sketch(comp, comp.xYConstructionPlane, c, inc)
            ext = comp.features.extrudeFeatures
            ei = ext.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(mm(vals['ss_stub'])))
            ext.add(ei)
            cut_circle_through(comp, comp.xYConstructionPlane, PIVOT_X*c, CAMBER*c*0.9, 3.2)   # vertical pivot bore

        # fin blank: symmetric 12% section, extruded
        comp = new_component(root, 'fin_blank', 320)
        fc = vals['ss_fin_chord']
        sk = closed_spline_sketch(comp, comp.xYConstructionPlane, [(x*fc, y*fc) for x, y in naca(t=0.12, m=0.0)])
        ext = comp.features.extrudeFeatures
        ei = ext.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(mm(vals['ss_fin_len'])))
        ext.add(ei)
        cut_circle_through(comp, comp.xYConstructionPlane, 0.30*fc, 0.0, 3.2)

        # capsule pod: loft of superellipse stations (nose taper = footwell)
        comp = new_component(root, 'capsule_pod', 400)
        st = [(0, 6, 10, 55), (15, 18, 40, 60), (40, 28, 70, 70), (80, 34, 100, 75),
              (110, 58, 125, 80), (140, 74, 140, 80), (180, 74, 140, 80), (210, 56, 118, 80)]
        sks = []
        for x, w, h, zc in st:
            pts = []
            for i in range(40):
                t = 2*math.pi*i/40; e = 2.5
                px = (w/2)*math.copysign(abs(math.cos(t))**(2/e), math.cos(t))
                py = (h/2)*math.copysign(abs(math.sin(t))**(2/e), math.sin(t)) + zc
                pts.append((px, py))
            plane = comp.xYConstructionPlane if x == 0 else offset_plane(comp, x)
            sks.append(closed_spline_sketch(comp, plane, pts, close_with_line=False))
        loft(comp, sks)

        # hinge lugs
        for name, height, xo in (('hinge_lug', 9.0, 520), ('hinge_lug_offset', 21.0, 560)):
            comp = new_component(root, name, xo)
            w, th, hole = 12.0, 5.0, 3.2
            cy = height - w/2
            sk = comp.sketches.add(comp.xYConstructionPlane)
            L = sk.sketchCurves.sketchLines; A = sk.sketchCurves.sketchArcs
            p = lambda x, y: adsk.core.Point3D.create(mm(x), mm(y), 0)
            l1 = L.addByTwoPoints(p(-w/2, 0), p(w/2, 0))
            l2 = L.addByTwoPoints(l1.endSketchPoint, p(w/2, cy))
            arc = A.addByThreePoints(l2.endSketchPoint, p(0, cy + w/2), p(-w/2, cy))
            L.addByTwoPoints(arc.endSketchPoint, l1.startSketchPoint)
            ext = comp.features.extrudeFeatures
            ei = ext.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(mm(th)))
            ext.add(ei)
            cut_circle_through(comp, comp.xYConstructionPlane, 0.0, cy, hole)

        ui.messageBox('Shapeshifter 1:10 built: 8 components. Edit ss_* in Modify > Change Parameters.')
    except:
        if ui: ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
