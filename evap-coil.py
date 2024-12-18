import magpylib as magpy
import numpy as np
import matplotlib.pyplot as plt


# Define arc and coil parameters
aw = .0045 #thickness of wire with insulation

a0xi = .130/2 + aw/2 #distance of coil from origin in x direction
a0yi = .1985/2 + aw/2 #distance of coil from origin in y direction

yl = -a0yi #bottom side of inner coil
yr = a0yi #top side of inner coil
xr = a0xi #right side of inner coil
xl = -a0xi #left side of inner coil

#inner arc dimensions
radius = 0.0133        # Radius of the arc
start_angle = 0      # Start angle in radians
end_angle = np.pi/2  # End angle in radians (90 degrees)


#inner line boundaries
xendl = xl +radius
xendr = xr -radius
yend_b = yl + radius
yend_u = yr -radius

#make a single line:
xseg1 = np.array([xr,xr])
yseg1 = np.array([yend_b,yend_u])
zseg1 = np.array([0,0])




##Test code for an arc
# Generate points along the arc
theta = np.linspace(start_angle, end_angle, 100)  # 100 points for smooth arc
x = radius * np.cos(theta) + xendr # x-coordinates
y = radius * np.sin(theta)  + yend_u # y-coordinates
z = np.zeros_like(x)        # z-coordinates (arc in the xy-plane)

print('before appending')
xseg1 = np.append(xseg1, x)
yseg1 = np.append(yseg1, y)
zseg1 = np.append(zseg1, z)

print('Printing xseg1')

print(xseg1)
# Combine into points array
arc_points = np.column_stack((xseg1, yseg1, zseg1))  # Shape: (N, 3)


# Create current-carrying arc
arc_current = magpy.current.Polyline(current=1, vertices=arc_points)  # 1 A current

# Visualize the arc
arc_current.show()

##end of test code