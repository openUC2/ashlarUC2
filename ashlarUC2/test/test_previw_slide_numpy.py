import numpy as np
import sys
import numpy as np
import skimage.transform
import skimage.util
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.text as mtext
from ashlarUC2 import utils

# Create example numpy arrays
num_images = 4
num_channels = 2
height, width = 100, 200
arrays = [np.random.rand(num_images, num_channels, height, width)]
# create a 2D list of xy positions 
pixel_size = 0.5
position_list = np.array(([0, 0], [0, 1], [1, 0], [1, 1]))*260. +(130., 130.) # micometer
maximum_shift_microns = 50

numbers = False
bounds = False
channel = 0
downsample = 5
log = False
flip_x = False
flip_y = False
nImages = num_images
positions = position_list
origin = np.array([0, 0])
size = np.array([height, width])
resolution_scale = 1 / downsample

# compute size based on stage coordinates 
size = np.array((np.max(position_list[:,0]) - np.min(position_list[:,0]), np.max(position_list[:,1]) - np.min(position_list[:,0])))/pixel_size # pixels

positions = (positions - origin) * resolution_scale
pmax = (positions + size * resolution_scale).max(axis=0)
mshape = (pmax + 0.5).astype(int)
mosaic = np.zeros(mshape, dtype=np.uint16)

for i in range(nImages):
    sys.stdout.write("\rLoading %d/%d" % (i + 1, nImages))
    sys.stdout.flush()
    img = np.squeeze(arrays[0][i, 0, :, :])
    img = skimage.transform.rescale(img, resolution_scale, anti_aliasing=False)
    if flip_x:
        img = np.fliplr(img)
    if flip_y:
        img = np.flipud(img)
    img = skimage.img_as_uint(img)

    # Round position so paste will skip the expensive subpixel shift.
    pos = np.round(positions[i])
    utils.paste(mosaic, img, pos, np.maximum)

ax = plt.gca()

plt.imshow(X=mosaic, axes=ax, extent=(0, pmax[1], pmax[0], 0))

h, w = size * resolution_scale
for i, (x, y) in enumerate(np.fliplr(positions)):
    if bounds:
        rect = mpatches.Rectangle((x, y), w, h, color='black', fill=False)
        ax.add_patch(rect)
    if numbers:
        xc = x + w / 2
        yc = y + h / 2
        circle = mpatches.Circle((xc, yc), w / 5, color='salmon', alpha=0.5)
        text = mtext.Text(
            xc, yc, str(i), color='k', size=10, ha='center', va='center'
        )
        ax.add_patch(circle)
        ax.add_artist(text)

plt.show()

