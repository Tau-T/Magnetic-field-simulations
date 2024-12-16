import magpylib as magpy
import numpy as np
import matplotlib.pyplot as plt


# Define arc and coil parameters
aw = .0045 #thickness of wire with insulation

a0xi = .130/2 + aw/2 #distance of coil from origin in x direction
a0yi = .1985/2 + aw/2 #distance of coil from origin in y direction


radius = 0.0133        # Radius of the arc
start_angle = 0      # Start angle in radians
end_angle = np.pi/2  # End angle in radians (90 degrees)

# Generate points along the arc
theta = np.linspace(start_angle, end_angle, 100)  # 100 points for smooth arc
x = radius * np.cos(theta)  # x-coordinates
y = radius * np.sin(theta)  # y-coordinates
z = np.zeros_like(x)        # z-coordinates (arc in the xy-plane)

# Combine into points array
arc_points = np.column_stack((x, y, z))  # Shape: (N, 3)

# Create current-carrying arc
arc_current = magpy.current.Line(current=1, vertices=arc_points)  # 1 A current

# Visualize the arc
arc_current.show()