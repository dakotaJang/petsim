# PET scan simulation
Positron Emission Tomography (PET) scan simulation in 2 dimension

## Online
The online version is available at the link below.
You can manipulate some key parameters to experiment with different settings.
(Parameter that you can modify are limited on online version)

http://petsim.dakotajang.me/

## Requirements
+ python
+ scikit-image

## Instruction
1. run python in the same in the drexctory as petsim.py
2. import petsim
3. execute petsim.sample()

Example terminal
> cd petsim

> python

> \>\>\> import petsim

> \>\>\> petsim.sample()

> phi_progress = 0.000000,x_progress = 0.000000

> phi_progress = 0.000000,x_progress = 1.492537

> phi_progress = 0.000000,x_progress = 2.985075

> ...

> phi_progress = 99.000000,x_progress = 97.014925

> phi_progress = 99.000000,x_progress = 98.507463

> phi_progress = 100,x_progress = 100

Check the sample() function to run a sample simulation.
Modify the variables in sample() to simulation different experiments.
