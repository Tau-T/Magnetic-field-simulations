import magpylib as magpy
import numpy as np
import matplotlib.pyplot as plt

# Example: Create a simple magnet and visualize the magnetic field
magnet = magpy.magnet.Cuboid(magnetization=(0, 0, 1000), dimension=(1, 1, 1))
sensor = magpy.Sensor(position=(0, 0, 1))

# Calculate the field at the sensor
field = magnet.getB(sensor.position)
print("Magnetic field at sensor:", field)


# Compute the B-field for some positions.

points = [(0,0,-.01), (0,0,0), (0,0,1), (1,0,0)] # in SI Units (m)
B = magpy.getB(magnet, points)

print(B.round(2))

# Visualize the magnet and sensor
magpy.show(magnet, sensor)
