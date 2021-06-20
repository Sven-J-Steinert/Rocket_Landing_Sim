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



dt = 0.01                      # timestep size in seconds
MAX_STEPS = int(1/dt * 100)     # 100 real time seconds
t = 0                           # start time = 0
a_g = np.array([0,0,-9.81])     # gravitational acceleration
a_re_flat = 25                 # rocket engine flat acceleration
a_re_dir = np.array([0,0,1])    # rocket engine acceleration direction -> normed vector
a_re = a_re_flat*a_re_dir       # rocket engine acceleration

# INITIALS
a = np.array([0,0,0])           # acceleration vector
v = np.array([-20,0,0])           # velocity vector
x = np.array([50,50,120])          # location vector

v_old = v                       # velocity vector from previous timestep

def normalize(x):
    return (x/np.linalg.norm(x))


print('┌────────────────────────┐')
print('│        SETTINGS        │')
print('├────────────────────────┤')
print('│  g │ ' + str(a_g[2]) + ' m/s²        │')
print('│ re │ ' + str(a_re_flat) + ' m/s²           │')
print('│ dt │ ' + str(dt) + ' s            │')
print('└────────────────────────┘')

df = pd.DataFrame(columns=['t', 'x_0', 'x_1', 'x_2', 'v_0', 'v_1', 'v_2', 'a_0', 'a_1', 'a_2', 'a_re_dir_0', 'a_re_dir_1', 'a_re_dir_2', 'a_re_0','a_re_1','a_re_2'], index=range(0,MAX_STEPS))
df.iloc[0] = [t,x[0],x[1],x[2],v[0],v[1],v[2],a[0],a[1],a[2],a_re_dir[0],a_re_dir[1],a_re_dir[2],a_re[0],a_re[1],a_re[2]]


# inner simulation for every step
def check_suicide_burn(_x,_v):
    _v_old = _v

    for i in range(1000):
        _a_re_dir = -(_v/np.linalg.norm(_v))
        # GENERAL PHYSICS
        _a_re = a_re_flat*_a_re_dir
        _a = a_g + _a_re                              # compute new acceleration
        _v = _v_old + _a*dt                            # compute new velocity
        _x = _x + _v_old*dt + 0.5*(_v - _v_old)*dt       # compute new location

        _v_old = _v

        # early stopping for efficiency
        if _x[2] <= 0:
            #print('hit')
            break
        if abs(_v[2]) < 1 and _x[2] > 10:
            #print('early hover')
            break

    if _x[2] <= 0:
        return True
    else:
        return False

# start mode
flight_mode = 'direction_correction'


for t_steps in range(1,MAX_STEPS):



    if flight_mode == 'direction_correction':

        # determine if suicide_burn should be started by simulating
        if check_suicide_burn(_x=x, _v=v):
            flight_mode = 'suicide_burn'

        # correct direction towards target on x/y coordinates
        if not ((x[0] == 0) and (x[1] == 0)):
            v_diff_y = - ( x[0]/(np.sqrt(x[0]**2 + x[1]**2)) )
            v_diff_x = np.sqrt(1-v_diff_y**2)
            a_re_dir = np.array([v_diff_x,v_diff_y,0])

            # determine when to switch to cruise
            if 0.90 < abs(x[0]/v[0])/abs(x[1]/v[1]) < 1.1 :
                flight_mode = 'cruise'
        else:
            flight_mode = 'cruise'


    if flight_mode == 'cruise':
        # engine cutoff
        a_re_dir = np.array([0,0,0])

        # determine if suicide_burn should be started by simulating
        if check_suicide_burn(_x=x, _v=v):
            flight_mode = 'suicide_burn'


    if flight_mode == 'suicide_burn':
        # accelerate in the direction of the velocity
        a_re_dir = -(v/np.linalg.norm(v))

        if a_re_dir[2] < 0:
            flight_mode = 'landing'


    if flight_mode == 'landing':
        # final engine cutoff
        a_re_dir = np.array([0,0,0])


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
        if abs(v[2]) < 3:
            print('LANDING SUCCESSFUL', end=' ')
        else:
            print('HIT THE GROUND TO HARD', end=' ')
        print('touchdown with ' + "{:.2f}".format(abs(v[2])) + ' m/s')

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
skip= int((1/dt)/30)





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



ani = animation.FuncAnimation(fig, animate, interval=10, repeat=True, frames=int(len(df)/skip))
plt.show()

print('')
print('end.')
