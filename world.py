import numpy as np
import time
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.animation as animation


def normalize(x):
    return (x/np.linalg.norm(x))

class World:

    def __init__(self):
        self.dt = 0.01                      # timestep size in seconds
        self.max_steps = int(1/self.dt * 100)     # 100 real time seconds
        self.t = 0                           # start time = 0

        self.a_g = np.array([0,0,-9.81])     # gravitational acceleration
        self.a_re_flat = 25                 # rocket engine flat acceleration
        self.a_re_dir = np.array([0,0,1])    # rocket engine acceleration direction -> normed vector
        self.a_re = self.a_re_flat*self.a_re_dir       # rocket engine acceleration

        # INITIALS
        self.a = np.array([0,0,0])           # acceleration vector
        self.v = np.array([-20,0,0])           # velocity vector
        self.x = np.array([50,50,120])          # location vector

        self.v_old = self.v                       # velocity vector from previous timestep

        # start mode
        self.flight_mode = 'direction_correction'

        # df setup
        self.df = pd.DataFrame(columns=['t', 'x_0', 'x_1', 'x_2', 'v_0', 'v_1', 'v_2', 'a_0', 'a_1', 'a_2', 'a_re_dir_0', 'a_re_dir_1', 'a_re_dir_2', 'a_re_0','a_re_1','a_re_2'], index=range(0,self.max_steps))
        self.df.iloc[0] = [self.t,self.x[0],self.x[1],self.x[2],self.v[0],self.v[1],self.v[2],self.a[0],self.a[1],self.a[2],self.a_re_dir[0],self.a_re_dir[1],self.a_re_dir[2],self.a_re[0],self.a_re[1],self.a_re[2]]

        self.print_settings()

        for self.t_steps in range(1,self.max_steps):
            if self.step_forward(): break
            #time.sleep(0.01)
        
        self.evaluate_df()

    def print_settings(self):
        print('┌────────────────────────┐')
        print('│        SETTINGS        │')
        print('├────────────────────────┤')
        print('│  g │ ' + str(self.a_g[2]) + ' m/s²        │')
        print('│ re │ ' + str(self.a_re_flat) + ' m/s²           │')
        print('│ dt │ ' + str(self.dt) + ' s            │')
        print('└────────────────────────┘')
    
    # inner simulation for every step
    def check_suicide_burn(self,x,v):
        v_old = v

        for i in range(1000):
            a_re_dir = -(v/np.linalg.norm(v))
            # GENERAL PHYSICS
            a_re = self.a_re_flat*a_re_dir
            a = self.a_g + a_re                              # compute new acceleration
            v = v_old + a*self.dt                            # compute new velocity
            x = x + v_old*self.dt + 0.5*(v - v_old)*self.dt       # compute new location

            v_old = v

            # early stopping for efficiency
            if x[2] <= 0:
                #print('hit')
                break
            if abs(v[2]) < 1 and x[2] > 10:
                #print('early hover')
                break

        if x[2] <= 0:
            return True
        else:
            return False

    def evaluate_df(self):
        self.df = self.df.dropna()
        print(self.df)

        df_t = self.df['t']
        df_x = self.df[['x_0','x_1','x_2']]
        df_v = self.df[['v_0','v_1','v_2']]
        df_a = self.df[['a_0','a_1','a_2']]
        df_a_re_dir = self.df[['a_re_dir_0','a_re_dir_1','a_re_dir_2']]
        df_a_re = self.df[['a_re_0','a_re_1','a_re_2']]


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        skip= int((1/self.dt)/30)

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


        ani = animation.FuncAnimation(fig, animate, interval=10, repeat=True, frames=int(len(self.df)/skip))
        plt.show()

        print('')
        print('end.')



    def step_forward(self):
        if self.flight_mode == 'direction_correction':

            # determine if suicide_burn should be started by simulating
            if self.check_suicide_burn(x=self.x, v=self.v):
                self.flight_mode = 'suicide_burn'

            # correct direction towards target on x/y coordinates
            if not ((self.x[0] == 0) and (self.x[1] == 0)):
                self.v_diff_y = - ( self.x[0]/(np.sqrt(self.x[0]**2 + self.x[1]**2)) )
                self.v_diff_x = np.sqrt(1-self.v_diff_y**2)
                self.a_re_dir = np.array([self.v_diff_x,self.v_diff_y,0])

                # determine when to switch to cruise
                if 0.90 < abs(self.x[0]/self.v[0])/abs(self.x[1]/self.v[1]) < 1.1 :
                    self.flight_mode = 'cruise'
            else:
                self.flight_mode = 'cruise'


        if self.flight_mode == 'cruise':
            # engine cutoff
            self.a_re_dir = np.array([0,0,0])

            # determine if suicide_burn should be started by simulating
            if self.check_suicide_burn(x=self.x, v=self.v):
                self.flight_mode = 'suicide_burn'


        if self.flight_mode == 'suicide_burn':
            # accelerate in the direction of the velocity
            self.a_re_dir = -(self.v/np.linalg.norm(self.v))

            if self.a_re_dir[2] < 0:
                self.flight_mode = 'landing'


        if self.flight_mode == 'landing':
            # final engine cutoff
            self.a_re_dir = np.array([0,0,0])


        # GENERAL PHYSICS
        self.a_re = self.a_re_flat*self.a_re_dir
        self.a = self.a_g + self.a_re                              # compute new acceleration
        self.v = self.v_old + self.a*self.dt                            # compute new velocity
        self.x = self.x + self.v_old*self.dt + 0.5*(self.v - self.v_old)*self.dt       # compute new location

        self.v_old = self.v
        self.t = self.t_steps * self.dt


        # save data
        self.df.iloc[self.t_steps] = [self.t,self.x[0],self.x[1],self.x[2],self.v[0],self.v[1],self.v[2],self.a[0],self.a[1],self.a[2],self.a_re_dir[0],self.a_re_dir[1],self.a_re_dir[2],self.a_re[0],self.a_re[1],self.a_re[2]]

        if self.x[2] <= 0:
            if abs(self.v[2]) < 3:
                print('LANDING SUCCESSFUL', end=' ')
            else:
                print('HIT THE GROUND TO HARD', end=' ')
            print('touchdown with ' + "{:.2f}".format(abs(self.v[2])) + ' m/s')

            return True


NewWorld = World()
