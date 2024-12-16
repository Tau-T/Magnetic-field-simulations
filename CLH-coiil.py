import magpylib as magpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter

# Coil winding initialization all units are in SI
coil1 = magpy.Collection()
coil2 = magpy.Collection()

inchtomm = .0254  # 1 inch in 25.4 mm
coil_spacing = .034 #m
innerd = .0237*2 #m
outerd = .0358*2 # m
ht = .012  # height of coil #35 windings...

nz = 6  # axial turns
nr = 6  # radial turns
rad_spacing = (outerd - innerd) / nr
z_spacing = ht / nz
coil1_z_origin = coil_spacing / 2

for z in np.linspace(0, ht, nz):
    for d in np.linspace(innerd, outerd, nr):
        winding = magpy.current.Circle(
            current=50,
            diameter=d,
            position=(0, 0.005, z),
        )
        coil1.add(winding)

for z in np.linspace(0, ht, nz):
    for d in np.linspace(innerd, outerd, nr):
        winding = magpy.current.Circle(
            current=50,
            diameter=d,
            position=(0, 0, -z),
        )
        coil2.add(winding)


coil1.position = (0, 0, coil1_z_origin)

helmholtz = magpy.Collection(coil1, coil2)

fig1 = plt.figure(figsize = (4,4))

ax3 = fig1.add_subplot(111,projection = "3d")

helmholtz.show(canvas = ax3)


# -------------------------------------------------------------------------------
# Compute the field and gradient on the yz-grid
grid = np.mgrid[0:0:1j, -0.1:0.1:200j, -0.1:0.1:200j].T[:, :, 0]
_, Y, Z = np.moveaxis(grid, 2, 0)

# Get the magnetic field from helmholtz coil
B = magpy.getB(helmholtz, grid)
_, By, Bz = np.moveaxis(B, 2, 0)

# Compute the magnitude of B
Bamp = np.linalg.norm(B, axis=2)

# Compute the gradient magnitude of the field amplitude using gaussian_gradient_magnitude
field_gradient_magnitude = gaussian_gradient_magnitude(Bamp, sigma=1)

# Plotting the field and its gradient
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot the magnetic field streamlines
sp1 = ax1.streamplot(Y*100, Z*100, By, Bz, density=2, color=Bamp, linewidth=np.sqrt(Bamp) * 3, cmap='coolwarm')
ax1.set(title='Magnetic Field of offset Coil Pair', xlabel='y-position (cm)', ylabel='z-position (cm)', aspect=1)
plt.colorbar(sp1.lines, ax=ax1, label='Magnetic Field Magnitude (T)')

# Plot the gradient magnitude of the field
'''sp2 = ax2.imshow(field_gradient_magnitude*10**4, extent=(Y.min(), Y.max(), Z.min(), Z.max()), origin='lower', cmap='inferno')
ax2.set(title='Field Gradient Magnitude', xlabel='y-position (m)', ylabel='z-position (m)', aspect=1)
plt.colorbar(sp2, ax=ax2, label='Gradient Magnitude (T/m)')
'''
#plt.tight_layout()
#plt.show()

# Continuation from above - ensure previous code is executed

#fig, ax = plt.subplots(1, 1, figsize=(6,5))

# Create a figure and add a 3D subplot
fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(111, projection='3d')  # Set up a 3D axis

#Plot the color map as well
fig2, ax2 = plt.subplots(1, 1, figsize=(6,5))

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
# Compute field of the coil pair on yz-grid
grid = np.mgrid[0:0:1j, -.003:.003:200j, -.003:.003:200j].T[:,:,0]
_, Y, Z = np.moveaxis(grid, 2, 0)

B = helmholtz.getB(grid)

# Field at center
B0 = helmholtz.getB((0,0,0))
B0amp = np.linalg.norm(B0)

# Homogeneity error
err = np.linalg.norm((B-B0)/B0amp, axis=2)



# Plot error on grid
levels = np.linspace(0,5,50)
#sp = ax.contourf(Y, Z, err*100, levels)
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------


sp = ax.plot_surface(Y*100,Z*100, err*100)
# Set axis labels and title
ax.set_xlabel('Y-position (cm)')
ax.set_ylabel('Z-position (cm)')
ax.set_zlabel('Error (% of B0)')
ax.set_title('Helmholtz Coil Homogeneity Error')


# Plot error on grid
sp2 = ax2.contourf(Y*100, Z*100, err*100,levels)

# Figure styling
ax2.set(
    title='Helmholtz homogeneity error',
    xlabel='y-position (cm)',
    ylabel='z-position (cm)',
    aspect=1,
)
plt.colorbar(sp2, ax=ax2, label='(% of B0)')



plt.tight_layout()
plt.show()