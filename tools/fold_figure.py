#!/usr/bin/env python3
"""Top-view fold sequence figure from the kinematics model."""
import importlib.util, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPoly, Circle

spec = importlib.util.spec_from_file_location('fk', __file__.replace('fold_figure.py','fold_kinematics.py'))
fk = importlib.util.module_from_spec(spec); spec.loader.exec_module(fk)

STATES = [(0,0,'deployed'), (90,0,'stage 1: 50%'), (177,0,'stage 1 done\n(outers doubled back)'),
          (177,30,'stage 2: 35%'), (177,60,'stage 2: 70%'), (177,88,'folded\n3.9 x 2.5 m')]
COL = dict(front='#e8a33d', rear='#3dbf9b', fin='#b06fd4', hull='#9aa7b5', nac='#d46f6f')

fig, axes = plt.subplots(2, 3, figsize=(15, 11))
for ax, (psi, phi, title) in zip(axes.flat, STATES):
    for mirror in (+1, -1):
        g = fk.side_geometry(psi, phi, +1)
        M = np.array([[1,0],[0,mirror]])
        for key, colkey in (('front','front'), ('rear','rear')):
            for part in ('inner','outer'):
                ax.add_patch(MplPoly(g[key][part] @ M, closed=True, fc=COL[colkey],
                                     ec='k', lw=0.6, alpha=0.85 if part=='inner' else 0.55))
        ax.add_patch(MplPoly(g['fin']['poly'] @ M, closed=True, fc=COL['fin'], ec='k', lw=0.6))
        c = g['nacelle']['center'] @ M
        ax.add_patch(Circle(c, g['nacelle']['r'], fc=COL['nac'], ec='k', lw=0.5, alpha=0.8))
    for hn, hp, hz in fk.capsule_polys():
        ax.add_patch(MplPoly(hp, closed=True, fc=COL['hull'], ec='k', lw=0.8,
                             alpha=0.5 if hn!='footwell' else 0.8))
    ax.set_title(title, fontsize=11)
    ax.set_xlim(-2.6, 5.6); ax.set_ylim(-5.6, 5.6); ax.set_aspect('equal')
    ax.grid(alpha=0.25, lw=0.4); ax.tick_params(labelsize=7)
    ax.axhline(0, color='k', lw=0.3)
fig.suptitle('Shapeshifter fold sequence — top view (x aft, y right; forward scissor)', fontsize=14)
fig.text(0.5, 0.015, 'Stage 1: outer panels + fin double back about vertical mid-span knuckles (parallelogram, fin translates). '
         'Stage 2: inner panels sweep FORWARD about root stubs.\nAll hinge axes vertical: gravity-neutral fold. '
         'Dark grey = narrow footwell (fold-critical hull constraint).', ha='center', fontsize=9)
plt.tight_layout(rect=[0,0.035,1,0.96])
out = __file__.replace('tools/fold_figure.py','docs/fold_sequence.png')
plt.savefig(out, dpi=110)
print('wrote', out)
