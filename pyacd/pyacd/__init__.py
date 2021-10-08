#!/usr/bin/env python3
#%%
import subprocess
import autograff.geom as geom
import numpy as np
import os

try:
    path = os.path.abspath(os.path.dirname(__file__))
except NameError:
    path = os.path.join(os.getcwd(), 'pyacd/pyacd')

def save_poly(S, fname):
    S = geom.fix_shape_winding(S, cw=False)
    holes = geom.get_holes(S)
    m = len(S)
    res = '%d\n'%m
    for P, hole in zip(S, holes):
        P = list(P.T)
        #P = P + [P[0]]
        inout = 'in' if hole else 'out'
        #if hole:
        #    P = P[::-1]
        res += '%d %s\n'%(len(P), inout)
        for p in P:
            res += '%.3f %.3f\n'%(p[0], p[1])
        res += ' '.join([str(i+1) for i in range(len(P))]) + '\n'
    f = open(fname, 'w')
    f.write(res)
    f.close()
    return S

def safe_split(line):
    return [s for s in line.split(' ') if s]

def load_poly(fname):
    s = open(fname).read()
    lines = s.split('\n')
    m = int(lines[0])
    i = 1
    c = 0
    S = []
    while c < m:
        line = safe_split(lines[i])
        n = int(line[0])
        i += 1
        V = []
        for j in range(n):
            line = safe_split(lines[i+j]) #lines[i+j].split(' ')
            x, y = [float(v) for v in line]
            V.append((x, y))
        line = safe_split(lines[i+n]) #lines[i+n].split(' ')
        P = [V[int(ind)-1] for ind in line]
        S.append(np.array(P).T)
        i += n + 1
        c += 1
    return S

def decompose(S,
              tau=0.0, # tolerance
              alpha=0.0, # concavity weight
              beta=1.0, # distance weight
              measure='hybrid1', # one of shortestpath (sp), straightline (sl), hybrid1, hybrid2
              verbose=False
            ):
    S = save_poly(S, './tmp.poly')
    res = subprocess.run(os.path.join(path, '../../acd2d_gui -g -s ' +
                                      f'-t {tau} ' +
                                      f'-a {alpha} ' +
                                      f'-b {beta} ' +
                                      f'-m {measure} ' +
                                      ' ./tmp.poly'),
                         shell=True,
                         stdout=subprocess.PIPE)
    stdout = res.stdout.decode("utf-8")
    if 'ERROR' in stdout:
        #print(stdout)
        print('Failed')
        return S

    if verbose:
        print(stdout)
    lines = stdout.split('\n')
    respath = lines[-2].split(' ')[-1]
    norm = float(lines[-4].split(' ')[-1])
    decomp = load_poly(respath)
    return [P*norm for P in decomp]


import autograff.svg as svg

S = svg.load_svg('/home/colormotor/develop/edavid_workspace/edavid_colormotor/images/R.svg')

Sp = load_poly('./test_env/hole1.poly')
#S = [geom.shapes.random_radial_polygon(20, 0.1, 0.5)*29] #[:,::-1]] #[:,:-1]]
decomp = decompose(S, alpha=1, beta=0, tau=0.2, measure='hybrid1')


#S = geom.affine_mul(geom.rect_in_rect_transform(geom.bounding_box(S),
#                                                geom.bounding_box(Sp)), S)
print('done')
import autograff.plut as plut
plut.figure(3,3)
plut.stroke_shape(S, 'r', closed=True)
plut.draw_arrow(S[0][:,0], S[0][:,1], 'r', head_width=0.1)
plut.stroke_shape(decomp, 'b', closed=True)
#plut.draw_arrow(Sp[0][:,0], Sp[0][:,1], 'b', head_width=0.1)
plut.show()
#S = load_poly('./test_env/hole4.poly-acd0.000-hybrid1.poly')
