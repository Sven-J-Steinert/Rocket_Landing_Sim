# Rocket Landing Simulator
Time step based physical simulation in python.

```
a = acceleration
v = velocity
x = location
```

core computation by integrating a over dt for v and integrating v over dt for x
<img src="https://latex.codecogs.com/svg.image?\int&space;a&space;\&space;dt" title="\int a \ dt" />

currently supported parameters

* gravitaional acceleration
* rocket engine acceleration
* rocket engine direction

currently supported flight modes

* direction correction
* cruise
* suicide burn

The timing for the suicide burn is determined by simulating one for every timestep

![](https://raw.githubusercontent.com/unconsciou5/Rocket_Landing_Sim/master/doc/preview.gif)
