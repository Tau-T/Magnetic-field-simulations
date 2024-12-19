import magpylib as magpy
import numpy as np
import matplotlib.pyplot as plt
from rect_coil_geom import rect_coil_geom

### Define arc and coil parameters

coil1 = magpy.Collection()
coil2 = magpy. Collection()
aw = .0045 #thickness of wire with insulation

a0xi = .130/2 + aw/2 #distance of coil from origin in x direction
a0yi = .1985/2 + aw/2 #distance of coil from origin in y direction
z0 = .04 + aw/2

#sides of the coil
yl = -a0yi #bottom side of inner coil
yr = a0yi #top side of inner coil
xr = a0xi #right side of inner coil
xl = -a0xi #left side of inner coil

#inner arc dimensions
radius = 0.0133        # Radius of the arc
start_angle = 0      # Start angle in radians
end_angle = np.pi/2  # End angle in radians (90 degrees)

x_func, y_func, z_func = rect_coil_geom(a0xi, a0yi, 0, radius)

x_func2, y_func2, z_func2 = rect_coil_geom(a0xi+aw, a0yi+aw, 0, radius+aw)

#for l in np.linspace(a0xi, a0xi + 8*aw, 8)
for z in np.linspace(0, 6*aw, 6):
    for l in np.linspace(0, 8*aw, 8):
            x_func, y_func, z_func = rect_coil_geom(a0xi+l, a0yi+l, z0+z, radius+l)

            arc_points = np.column_stack((x_func, y_func, z_func)) 
            arc_current = magpy.current.Polyline(current = 13, vertices=arc_points)
            coil1.add(arc_current)
        


for z in np.linspace(0, 6*aw, 6):
    for l in np.linspace(0, 8*aw, 8):
            x_func, y_func, z_func = rect_coil_geom(a0xi+l, a0yi+l, -z0-z, radius+l)

            arc_points = np.column_stack((x_func, y_func, z_func)) 
            arc_current = magpy.current.Polyline(current = 13, vertices=arc_points)
            coil2.add(arc_current)
        
helmholtz = magpy.Collection(coil1,coil2)

helmholtz.show()

# -------------------------------------------------------------------------------
# Compute the field and gradient on the yz-grid
grid = np.mgrid[0:0:1j, -0.03:0.03:101j, -0.03:0.03:101j].T[:, :, 0]
_, Y, Z = np.moveaxis(grid, 2, 0)

# Get the magnetic field from helmholtz coil
B = magpy.getB(helmholtz, grid)
_, By, Bz = np.moveaxis(B, 2, 0)

# Compute the magnitude of B
Bamp = np.linalg.norm(B, axis=2)


# Compute the gradient magnitude of the field amplitude using gaussian_gradient_magnitude
print('Z spacing')
print(Z[0,1]-Z[0,0])
print('Y-spacing')
print(Y[0,1]-Y[0,0])
grad_y, grad_z = np.gradient(Bamp, Y[0,:], Z[0,:])

# Plotting the field and its gradient
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot the magnetic field streamlines
sp1 = ax1.streamplot(Y, Z, By, Bz, density=2, color=Bamp, linewidth=np.sqrt(Bamp) * 3, cmap='coolwarm')
ax1.set(title='Magnetic Field of Helmholtz Coil', xlabel='y-position (m)', ylabel='z-position (m)', aspect=1)
plt.colorbar(sp1.lines, ax=ax1, label='Magnetic Field Magnitude (T)')

# Plot the gradient magnitude of the field
sp2 = ax2.imshow(Bamp*10**4, extent=(Y.min(), Y.max(), Z.min(), Z.max()), origin='lower', cmap='inferno')
ax2.set(title='Field Magnitude', xlabel='y-position (m)', ylabel='z-position (m)', aspect=1)
plt.colorbar(sp2, ax=ax2, label='Field (G)')

plt.tight_layout()
plt.show()

print('This is grad_y')
print(grad_y*100)
print('this is grad_z')
print(grad_z*100)

#plt.streamplot(Y,Z, grad_y, grad_z, density=2, color=Bamp, linewidth=np.sqrt(Bamp)*3, cmap= 'coolowarm')

