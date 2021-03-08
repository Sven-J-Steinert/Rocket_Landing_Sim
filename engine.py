import numpy as np
import time

dt = 0.01                       # timestep size in seconds
a_g = np.array([0,0,-9.81])     # gravitational acceleration
a_re_flat = 14                # rocket engine flat acceleration
a_re_dir = np.array([0,0,1])    # rocket engine acceleration direction -> normed vector
a_re = a_re_flat*a_re_dir       # rocket engine acceleration
# INITIALS
a = np.array([0,0,0])           # acceleration vector
v = np.array([0,2,-10])           # velocity vector
x = np.array([0,0,10])          # location vector

v_old = v                       # velocity vector from previous timestep

print('┌────────────────────────┐')
print('│        SETTINGS        │')
print('├────────────────────────┤')
print('│  g │ ' + str(a_g[2]) + ' m/s²        │')
print('│ re │ ' + str(a_re_flat) + ' m/s²         │')
print('│ dt │ ' + str(dt) + ' s            │')
print('└────────────────────────┘')
print('Initial values')
print('a: ' + str(a))
print('v: ' + str(v))
print('x: ' + str(x))
print('dt: ' + str(dt))

print('')
print(' s                           x                                 v                                a            ')
print("{:.3f}".format(0) + ' │          │ ' + "{:.3f}".format(x[0]) + ' │ ' + "{:.3f}".format(x[1]) + ' │ ' + "{:.3f}".format(x[2]) + ' │         │ ' + "{:.3f}".format(v[0]) + ' │ ' + "{:.3f}".format(v[1]) + ' │ ' + "{:.3f}".format(v[2]) + ' │        │ ' + "{:.3f}".format(a[0]) + ' │ ' + "{:.3f}".format(a[1]) + ' │ ' + "{:.3f}".format(a[2])+ ' │ ')
f = open("log.csv", "w")
for t_steps in range(1,2000):
    a = a_g + a_re                              # compute new acceleration
    v = v_old + a*dt                            # compute new velocity
    x = x + v_old*dt + 0.5*(v - v_old)*dt       # compute new location

    v_old = v
    t = t_steps * dt

    f.write("{:.3f}".format(t) + ';' + "{:.3f}".format(x[0]) + ';' + "{:.3f}".format(x[1]) + ';' + "{:.3f}".format(x[2]) + ';' + "{:.3f}".format(v[0]) + ';' + "{:.3f}".format(v[1]) + ';' + "{:.3f}".format(v[2]) + ';' + "{:.3f}".format(a[0]) + ';' + "{:.3f}".format(a[1]) + ';' + "{:.3f}".format(a[2]) + '\n')

    print("{:.3f}".format(t) + ' │          │ ' + "{:.3f}".format(x[0]) + ' │ ' + "{:.3f}".format(x[1]) + ' │ ' + "{:.3f}".format(x[2]) + ' │         │ ' + "{:.3f}".format(v[0]) + ' │ ' + "{:.3f}".format(v[1]) + ' │ ' + "{:.3f}".format(v[2]) + ' │        │ ' + "{:.3f}".format(a[0]) + ' │ ' + "{:.3f}".format(a[1]) + ' │ ' + "{:.3f}".format(a[2])+ ' │ ', end='\r')
    if x[2] <= 0:
        print("{:.3f}".format(t) + ' │          │ ' + "{:.3f}".format(x[0]) + ' │ ' + "{:.3f}".format(x[1]) + ' │ ' + "{:.3f}".format(x[2]) + ' │         │ ' + "{:.3f}".format(v[0]) + ' │ ' + "{:.3f}".format(v[1]) + ' │ ' + "{:.3f}".format(v[2]) + ' │        │ ' + "{:.3f}".format(a[0]) + ' │ ' + "{:.3f}".format(a[1]) + ' │ ' + "{:.3f}".format(a[2])+ ' │ ')
        print('HIT THE GROUND')
        break
    #time.sleep(0.01)


f.close()
print('')
print('end.')
