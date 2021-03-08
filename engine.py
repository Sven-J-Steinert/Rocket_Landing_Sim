import numpy as np
import time

dt = 0.01                       # timestep size in seconds
a_g = np.array([0,0,-9.81])     # gravitational acceleration
a_re_flat = 14                # rocket engine flat acceleration
a_re_flat = 15                 # rocket engine flat acceleration
a_re_dir = np.array([0,0,1])    # rocket engine acceleration direction -> normed vector
a_re = a_re_flat*a_re_dir       # rocket engine acceleration
# INITIALS
a = np.array([0,0,0])           # acceleration vector
v = np.array([-5,2,-10])           # velocity vector
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

#df = pd.DataFrame(np.array([t,x[0],x[1],x[2],v[0],v[1],v[2],a[0],a[1],a[2]]) ,columns=['t', 'x_0', 'x_1', 'x_2', 'v_0', 'v_1', 'v_2', 'a_0', 'a_1', 'a_2'])
df = pd.DataFrame(columns=['t', 'x_0', 'x_1', 'x_2', 'v_0', 'v_1', 'v_2', 'a_0', 'a_1', 'a_2', 'a_re_dir_0', 'a_re_dir_1', 'a_re_dir_2', 'a_re_0','a_re_1','a_re_2'], index=range(0,MAX_STEPS))
df.iloc[0] = [t,x[0],x[1],x[2],v[0],v[1],v[2],a[0],a[1],a[2],a_re_dir[0],a_re_dir[1],a_re_dir[2],a_re[0],a_re[1],a_re[2]]


for t_steps in range(1,MAX_STEPS):
    a = a_g + a_re                              # compute new acceleration
    v = v_old + a*dt                            # compute new velocity
    x = x + v_old*dt + 0.5*(v - v_old)*dt       # compute new location

    v_old = v
    t = t_steps * dt

    df.iloc[t_steps] = [t,x[0],x[1],x[2],v[0],v[1],v[2],a[0],a[1],a[2],a_re_dir[0],a_re_dir[1],a_re_dir[2],a_re[0],a_re[1],a_re[2]]

    if x[2] <= 0:
        print('HIT THE GROUND')
        break
    #time.sleep(0.01)

print(df)

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

    ax.quiver(df_x.iloc[skip*i][0],df_x.iloc[skip*i][1],df_x.iloc[skip*i][2], df_v.iloc[skip*i][0],df_v.iloc[skip*i][1],df_v.iloc[skip*i][2]) # velocity vector

    ax.quiver(df_x.iloc[skip*i][0],df_x.iloc[skip*i][1],df_x.iloc[skip*i][2], df_a_re.iloc[skip*i][0],df_a_re.iloc[skip*i][1],df_a_re.iloc[skip*i][2], color='red') # a_re_dir vector

    ax.scatter(df_x.iloc[skip*i][0],df_x.iloc[skip*i][1],df_x.iloc[skip*i][2], marker='o', color='black', label='point')



    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([0, 20])



ani = animation.FuncAnimation(fig, animate, interval=100, repeat=True, frames=int(len(df)/skip))
plt.show()

print('')
print('end.')
