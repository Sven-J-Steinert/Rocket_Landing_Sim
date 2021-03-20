import numpy as np
import time
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import sys

from scipy.integrate import quad
from sympy import *


MAX_STEPS = 600
dt = 0.01                       # timestep size in seconds
t = 0
a_g = np.array([0,0,-9.81])     # gravitational acceleration
a_re_flat = 25                 # rocket engine flat acceleration
a_re_dir = np.array([0,0,1])    # rocket engine acceleration direction -> normed vector
a_re = a_re_flat*a_re_dir       # rocket engine acceleration

# INITIALS
a = np.array([0,0,0])           # acceleration vector
v = np.array([-20,0,-20])           # velocity vector
x = np.array([50,0,120])          # location vector

v_old = v                       # velocity vector from previous timestep


print('┌────────────────────────┐')
print('│        SETTINGS        │')
print('├────────────────────────┤')
print('│  g │ ' + str(a_g[2]) + ' m/s²        │')
print('│ re │ ' + str(a_re_flat) + ' m/s²           │')
print('│ dt │ ' + str(dt) + ' s            │')
print('└────────────────────────┘')

df = pd.DataFrame(columns=['t', 'x_0', 'x_1', 'x_2', 'v_0', 'v_1', 'v_2', 'a_0', 'a_1', 'a_2', 'a_re_dir_0', 'a_re_dir_1', 'a_re_dir_2', 'a_re_0','a_re_1','a_re_2'], index=range(0,MAX_STEPS))
df.iloc[0] = [t,x[0],x[1],x[2],v[0],v[1],v[2],a[0],a[1],a[2],a_re_dir[0],a_re_dir[1],a_re_dir[2],a_re[0],a_re[1],a_re[2]]

flight_mode = 'cruise'


for t_steps in range(1,MAX_STEPS):

    if flight_mode == 'direction_correction':
        # correct direction towards target on x/y coordinates
        v_diff_y = - ( x[0]/(np.sqrt(x[0]**2 + x[1]**2)) )
        v_diff_x = np.sqrt(1-v_diff_y**2)
        a_re_dir = np.array([v_diff_x,v_diff_y,0])

        # determine when to switch to cruise
        if 0.90 < abs(x[0]/v[0])/abs(x[1]/v[1]) < 1.1 :
            flight_mode = 'cruise'


    if flight_mode == 'cruise':
        # engine cutoff
        a_re_dir = np.array([0,0,0])

        # determine required time for suicide_burn
        dt_1 = np.linalg.norm(v)/np.linalg.norm(a_re_flat)
        dt_2 = (np.linalg.norm(a_g) * dt_1)/np.linalg.norm(a_re_flat)
        dt_R = dt_1 + dt_2
        #print('dt: ' + str(dt_R), end=' ')

        # function: resulting acceleration in z axis during suicide_burn
        #def a_R_z(x):
        #    return (np.sin((dt_R/40*np.pi)*x)*(a_re_flat+a_g[2]))

        #init_printing(use_unicode=False, wrap_line=False)
        i = Symbol('i')
        a_equation = sin((dt_R/40*np.pi)*i)*(a_re_flat+a_g[2])
        v_equation = integrate(a_equation, i) + (a_re_flat+a_g[2])
        c = (a_re_flat+a_g[2])/(dt_R/40*np.pi)
        h = integrate(v_equation + c, (i,0, dt_R))
        #print('   h: ' + str(h))

        # function: resulting velocity in z axis during suicide_burn

        # integrate function over dt_R





        if x[2] <= h:
            flight_mode = 'suicide_burn'

    if flight_mode == 'suicide_burn':
        # accelerate in velocity direction
        a_re_dir = -(v/np.linalg.norm(v))


    # GENERAL PHYSICS
    a_re = a_re_flat*a_re_dir
    a = a_g + a_re                              # compute new acceleration
    v = v_old + a*dt                            # compute new velocity
    x = x + v_old*dt + 0.5*(v - v_old)*dt       # compute new location

    v_old = v
    t = t_steps * dt


    # save data
    df.iloc[t_steps] = [t,x[0],x[1],x[2],v[0],v[1],v[2],a[0],a[1],a[2],a_re_dir[0],a_re_dir[1],a_re_dir[2],a_re[0],a_re[1],a_re[2]]

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


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
skip=5




def animate(i):
    ax.clear()

    ax.quiver(df_x.iloc[skip*i][0],df_x.iloc[skip*i][1],df_x.iloc[skip*i][2], df_v.iloc[skip*i][0],df_v.iloc[skip*i][1],df_v.iloc[skip*i][2], color='blue')             # velocity vector

    ax.quiver(df_x.iloc[skip*i][0],df_x.iloc[skip*i][1],df_x.iloc[skip*i][2], df_a_re.iloc[skip*i][0],df_a_re.iloc[skip*i][1],df_a_re.iloc[skip*i][2], color='red')     # acceleration rocket engine vector


    ax.scatter(df_x.iloc[skip*i][0],df_x.iloc[skip*i][1],df_x.iloc[skip*i][2], marker='o', color='black', label='point')

    ax.scatter(0,0,0, marker='X', color='black', label='point')
    #matplotlib.widgets.TextBox(ax, text='t = ' , initial='', color='.95', hovercolor='1', label_pad=0.01)
    #axLabel = plt.axes([0.7, 0.05, 0.21, 0.075])
    #textbox = matplotlib.widgets.TextBox(axLabel, 'time: ')
    #textbox.set_val("jojojo")

    ax.set_xlim([-50, 50])
    ax.set_ylim([-50, 50])
    ax.set_zlim([0, 100])



ani = animation.FuncAnimation(fig, animate, interval=100, repeat=True, frames=int(len(df)/skip))
plt.show()

print('')
print('end.')
