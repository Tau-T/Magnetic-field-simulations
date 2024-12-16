import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1, figsize=(6,5))

# Compute field and plot the coil pair field on yz-grid
grid = np.mgrid[0:0:1j, -13:13:20j, -13:13:20j].T[:,:,0]
_, Y, Z = np.moveaxis(grid, 2, 0)

B = magpy.getB(helmholtz, grid)
_, By, Bz = np.moveaxis(B, 2, 0)

Bamp = np.linalg.norm(B, axis=2)
Bamp /= np.amax(Bamp)

sp = ax.streamplot(Y, Z, By, Bz, density=2, color=Bamp,
    linewidth=np.sqrt(Bamp)*3, cmap='coolwarm',
)

# Plot coil outline
from matplotlib.patches import Rectangle
for loc in [(4,4), (4,-6), (-6,4), (-6,-6)]:
    ax.add_patch(Rectangle(loc, 2, 2, color='k', zorder=10))

# Figure styling
ax.set(
    title='Magnetic field of Helmholtz',
    xlabel='y-position (m)',
    ylabel='z-position (m)',
    aspect=1,
)
plt.colorbar(sp.lines, ax=ax, label='(T)')

plt.tight_layout()
plt.show()

