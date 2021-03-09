import numpy as np
import time
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import sys

from geomdl import NURBS

MAX_STEPS = 300
dt = 0.01                       # timestep size in seconds
t = 0
a_g = np.array([0,0,-9.81])     # gravitational acceleration
a_re_flat = 10                 # rocket engine flat acceleration
a_re_dir = np.array([0,0,1])    # rocket engine acceleration direction -> normed vector
a_re = a_re_flat*a_re_dir       # rocket engine acceleration
# INITIALS
a = np.array([0,0,0])           # acceleration vector
v = np.array([-3,-3,-10])           # velocity vector
x = np.array([5,5,20])          # location vector

v_old = v                       # velocity vector from previous timestep

# CALCULATE SPLINE
# Create a 3-dimensional B-spline Curve
curve = NURBS.Curve()
# Set degree
curve.degree = 3
# Set control points (weights vector will be 1 by default)
# Use curve.ctrlptsw is if you are using homogeneous points as Pw
curve.ctrlpts = [ [x[0], x[1], x[2]], [x[0]+v[0], x[1]+v[1] ,x[2]+v[2]] ,[0, 0, 1], [0, 0, 0]]
# Set knot vector
curve.knotvector = [0, 0, 0, 0, 1, 1, 1, 1]
# Set evaluation delta (controls the number of curve points)
curve.delta = 0.05
# Get curve points (the curve will be automatically evaluated)
curve_points = curve.evalpts
curve_points = np.array(curve_points)
spline_vec = np.zeros((len(curve_points)-1,6))

for i in range(len(curve_points)-1):
    spline_vec[i,0:3]=curve_points[i]
    spline_vec[i,3:6]=curve_points[i+1]


print('┌────────────────────────┐')
print('│        SETTINGS        │')
print('├────────────────────────┤')
print('│  g │ ' + str(a_g[2]) + ' m/s²        │')
print('│ re │ ' + str(a_re_flat) + ' m/s²           │')
print('│ dt │ ' + str(dt) + ' s            │')
print('└────────────────────────┘')
print('Initial values')
print('a: ' + str(a))
print('v: ' + str(v))
print('x: ' + str(x))
print('dt: ' + str(dt))

d_min = sys.float_info.max

for i in range(len(spline_vec)):
    d_vec = x-curve_points[i]
    d = np.linalg.norm(d_vec)
    if d < d_min:
        print('entered IF')
        d_min = d
        d_min_i = i
d_min = spline_vec[d_min_i]

#df = pd.DataFrame(np.array([t,x[0],x[1],x[2],v[0],v[1],v[2],a[0],a[1],a[2]]) ,columns=['t', 'x_0', 'x_1', 'x_2', 'v_0', 'v_1', 'v_2', 'a_0', 'a_1', 'a_2'])
df = pd.DataFrame(columns=['t', 'x_0', 'x_1', 'x_2', 'v_0', 'v_1', 'v_2', 'a_0', 'a_1', 'a_2', 'a_re_dir_0', 'a_re_dir_1', 'a_re_dir_2', 'a_re_0','a_re_1','a_re_2','d_min_0','d_min_1','d_min_2','d_min_3','d_min_4','d_min_5'], index=range(0,MAX_STEPS))
df.iloc[0] = [t,x[0],x[1],x[2],v[0],v[1],v[2],a[0],a[1],a[2],a_re_dir[0],a_re_dir[1],a_re_dir[2],a_re[0],a_re[1],a_re[2],d_min[0],d_min[1],d_min[2],d_min[3],d_min[4],d_min[5]]


for t_steps in range(1,MAX_STEPS):
    #norm1 = x / np.linalg.norm(x)
    d_min = sys.float_info.max
    for i in range(len(spline_vec)):
        d_vec = x-curve_points[i]
        d = np.linalg.norm(d_vec)
        if d < d_min:
            d_min = d
            d_min_i = i
    d_min = spline_vec[d_min_i]
    d_min_temp = -(spline_vec[d_min_i,3:6] - spline_vec[d_min_i,0:3])
    a_re_dir = d_min_temp/np.linalg.norm(d_min_temp)
    a_re = a_re_flat*a_re_dir
    a = a_g + a_re                              # compute new acceleration
    v = v_old + a*dt                            # compute new velocity
    x = x + v_old*dt + 0.5*(v - v_old)*dt       # compute new location

    v_old = v
    t = t_steps * dt

    df.iloc[t_steps] = [t,x[0],x[1],x[2],v[0],v[1],v[2],a[0],a[1],a[2],a_re_dir[0],a_re_dir[1],a_re_dir[2],a_re[0],a_re[1],a_re[2],d_min[0],d_min[1],d_min[2],d_min[3],d_min[4],d_min[5]]

    if x[2] <= 0:
        print('HIT THE GROUND')
        break
    #time.sleep(0.01)

df = df.dropna()
print(df)

df_t = df['t']
df_x = df[['x_0','x_1','x_2']]
df_v = df[['v_0','v_1','v_2']]
df_a = df[['a_0','a_1','a_2']]
df_a_re_dir = df[['a_re_dir_0','a_re_dir_1','a_re_dir_2']]
df_a_re = df[['a_re_0','a_re_1','a_re_2']]
df_d_min = df[['d_min_0','d_min_1','d_min_2','d_min_3','d_min_4','d_min_5']]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
skip=5




def animate(i):
    ax.clear()
    ax.plot(curve_points[:,0],curve_points[:,1],curve_points[:,2])

    ax.quiver(df_x.iloc[skip*i][0],df_x.iloc[skip*i][1],df_x.iloc[skip*i][2], df_v.iloc[skip*i][0],df_v.iloc[skip*i][1],df_v.iloc[skip*i][2], color='blue')             # velocity vector

    ax.quiver(df_x.iloc[skip*i][0],df_x.iloc[skip*i][1],df_x.iloc[skip*i][2], df_a_re.iloc[skip*i][0],df_a_re.iloc[skip*i][1],df_a_re.iloc[skip*i][2], color='red')     # acceleration rocket engine vector

    ax.quiver(df_d_min.iloc[skip*i][0],df_d_min.iloc[skip*i][1],df_d_min.iloc[skip*i][2], df_d_min.iloc[skip*i][3],df_d_min.iloc[skip*i][4],df_d_min.iloc[skip*i][5], color='green')             # vector to spline

    ax.scatter(df_x.iloc[skip*i][0],df_x.iloc[skip*i][1],df_x.iloc[skip*i][2], marker='o', color='black', label='point')

    ax.scatter(0,0,0, marker='x', color='black', label='point')
    #matplotlib.widgets.TextBox(ax, text='t = ' , initial='', color='.95', hovercolor='1', label_pad=0.01)
    #axLabel = plt.axes([0.7, 0.05, 0.21, 0.075])
    #textbox = matplotlib.widgets.TextBox(axLabel, 'time: ')
    #textbox.set_val("jojojo")

    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([0, 20])



ani = animation.FuncAnimation(fig, animate, interval=100, repeat=True, frames=int(len(df)/skip))
plt.show()

print('')
print('end.')
