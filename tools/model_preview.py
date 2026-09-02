#!/usr/bin/env python3
"""Preview render of the 1:10 printable parts + assembled layout."""
import numpy as np, trimesh, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

D = os.path.join(os.path.dirname(__file__), '..', 'models', '1to10')
def load(n): return trimesh.load(os.path.join(D, n + '.stl'))
def draw(ax, m, T=np.eye(4), color='#e8a33d', alpha=0.9, stride=1):
    v = trimesh.transform_points(m.vertices, T); f = m.faces[::stride]
    ax.add_collection3d(Poly3DCollection(v[f], facecolor=color, edgecolor='none', alpha=alpha))
def tf(rot_deg=(0,0,0), t=(0,0,0)):
    T = trimesh.transformations.euler_matrix(*np.radians(rot_deg))
    T[:3,3] = t; return T

fig = plt.figure(figsize=(8, 8))
# --- left: print plate layout (span-vertical panels on 256 bed)
ax = fig.add_subplot(1, 1, 1, projection='3d')
plate = np.array([[0,0,0],[256,0,0],[256,256,0],[0,256,0]])
ax.add_collection3d(Poly3DCollection([plate], facecolor='#9aa7b5', alpha=0.25))
wi, wo, fin, pod = load('wing_inner'), load('wing_outer'), load('fin_blank'), load('capsule_pod')
# panel prints stand on Z: mesh z = span already; place 4 panels + 2 fins on one plate
for i, (m, c) in enumerate([(wi,'#e8a33d'),(wo,'#e8a33d'),(wi,'#3dbf9b'),(wo,'#3dbf9b')]):
    draw(ax, m, tf(t=(20 + i*60, 40, 0)), color=c)
draw(ax, fin, tf(t=(30, 190, 0)), color='#b06fd4'); draw(ax, fin, tf(t=(150, 190, 0)), color='#b06fd4')
ax.set_xlim(0,256); ax.set_ylim(0,256); ax.set_zlim(0,256); ax.set_box_aspect((1,1,1))
ax.set_title('One plate: 4 wing panels + 2 fins, span-vertical (256 mm cube)')
ax.set_xlabel('mm'); ax.set_ylabel('mm'); ax.set_zlabel('mm')

plt.tight_layout()
out = os.path.join(D, '..', '..', 'docs', 'model_1to10_preview.png')
plt.savefig(out, dpi=110); print('wrote', out)
