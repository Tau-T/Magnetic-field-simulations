import magpylib as magpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude

# Coil winding initialization all units are in SI
coil1 = magpy.Collection()
coil2 = magpy.Collection()

inchtomm = .0254  # 1 inch in 25.4 mm
coil_spacing = 3.02 * inchtomm
innerd = 6.02 * inchtomm
outerd = 7.82 * inchtomm
ht = .785 * inchtomm  # height of coil

nz = 4  # axial turns
nr = 5  # radial turns
rad_spacing = (outerd - innerd) / nr
z_spacing = ht / nz
coil1_z_origin = coil_spacing / 2


for z in np.linspace(coil1_z_origin, coil1_z_origin+ ht, 5):
    for d in np.linspace(innerd, outerd, 4):
        winding = magpy.current.Circle(
            current=10,
            diameter=d,
            position=(0, 0, z),
        )
        coil1.add(winding)

for z in np.linspace(coil1_z_origin, coil1_z_origin+ht, 5):
    for d in np.linspace(innerd, outerd, 4):
        winding = magpy.current.Circle(
            current= -10,
            diameter=d,
            position=(0, 0, -z),
        )
        coil2.add(winding)



helmholtz = magpy.Collection(coil1, coil2)


# -------------------------------------------------------------------------------
# Compute the field and gradient on the yz-grid
grid = np.mgrid[0:0:1j, -0.03:0.03:31j, -0.01:0.01:201j].T[:, :, 0]
_, Y, Z = np.moveaxis(grid, 2, 0)

# Get the magnetic field from helmholtz coil
B = magpy.getB(helmholtz, grid)
_, By, Bz = np.moveaxis(B, 2, 0)

# Compute the magnitude of B
Bamp = np.linalg.norm(B, axis=2)

print((Bamp[50,15])/2*10**4)
print(Bamp[100,15]*10**4)
print((Bamp[0,15])*10**4)
print((Bamp[200,15])*10**4)

# Compute the gradient magnitude of the field amplitude using gaussian_gradient_magnitude
field_gradient_magnitude = gaussian_gradient_magnitude(Bamp, sigma=1)

# Plotting the field and its gradient
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot the magnetic field streamlines
sp1 = ax1.streamplot(Y, Z, By, Bz, density=2, color=Bamp, linewidth=np.sqrt(Bamp) * 3, cmap='coolwarm')
ax1.set(title='Magnetic Field of Helmholtz Coil', xlabel='y-position (m)', ylabel='z-position (m)', aspect=1)
plt.colorbar(sp1.lines, ax=ax1, label='Magnetic Field Magnitude (T)')

# Plot the gradient magnitude of the field
sp2 = ax2.imshow(field_gradient_magnitude*10**4, extent=(Y.min(), Y.max(), Z.min(), Z.max()), origin='lower', cmap='inferno')
ax2.set(title='Field Gradient Magnitude', xlabel='y-position (m)', ylabel='z-position (m)', aspect=1)
plt.colorbar(sp2, ax=ax2, label='Gradient Magnitude (T/m)')

plt.tight_layout()
plt.show()

