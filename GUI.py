from ursina import *


app = Ursina()

r = 2
for i in range(1, r):
    t = i/r
    s = 10*i
    print(s)
    grid = Entity(model=Grid(s,s), scale=s, color=color.color(0,0,.8,lerp(.8,0,t)), rotation_x=90, y=0)
    subgrid = duplicate(grid)
    subgrid.model = Grid(s*2, s*2)
    subgrid.color = color.color(0,0,.8,lerp(.8,0,t))

x_axis_v = [Vec3(0,0,0), Vec3(1,0,0)]
y_axis_v = [Vec3(0,0,0), Vec3(0,1,0)]
z_axis_v = [Vec3(0,0,0), Vec3(0,0,1)]
x_axis = Entity(model=Mesh(vertices=x_axis_v, mode='line'),color=color.red)
y_axis = Entity(model=Mesh(vertices=y_axis_v, mode='line'),color=color.green)
z_axis = Entity(model=Mesh(vertices=z_axis_v, mode='line'),color=color.blue)

EditorCamera()

app.run()
