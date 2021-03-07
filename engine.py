import numpy as np
import time

dt = 0.01 # timestep size in seconds
g = 9.81 # gravitational acceleration
a = np.array([0,0,-g]) # acceleration vector
v = np.array([0,0,0]) # velocity vector
x = np.array([0,0,100]) # location vector

v_old = np.array([0,0,0]) # velocity vector from previous timestep

print('┌────────────────────────┐')
print('│        SETTINGS        │')
print('├────────────────────────┤')
print('│  g │ ' + str(g) + ' m/s²         │')
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
    v = v_old + a*dt
    x = x + v_old*dt + 0.5*(v - v_old)*dt
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
