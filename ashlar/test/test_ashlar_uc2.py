import os
import re
from datetime import datetime
import tifffile
import numpy as np
from ashlar.scripts.ashlar import process_images
# adjust to dataset:
input_dir = "/Users/bene/Dropbox/File requests/Raster Anabel Marr/input/"
#input_dir = r"C:\\Users\\T490\\Documents\\Anabel\\Bachelorarbeit\\Bilder\\Kontrastraster\\"

output_dir = "/Users/bene/Dropbox/File requests/Raster Anabel Marr/"

pixel_size = 0.327
maximum_shift_microns = 50

timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# adjust to desired output directories:
collected_tiles_file = os.path.join(input_dir, f'PATH_TO_TILE_COLLECTION.ome.tif')
ashlar_output_file = os.path.join(output_dir, "PATH_TO_STITCH_RESULT.ome.tif")

# Get the list of files
images = os.listdir(input_dir)
images.sort()

arrays = []
position_list = []
for img_name in images:
    if img_name.find('tif') < 0: 
        continue
    image = tifffile.imread(input_dir + img_name)
    if img_name.find('ome') >= 0:
        continue
    match = re.search(r'\((.*?), (.*?)\)', img_name)
    # the positions in the file names provide the center of the tile,
    # we need to subtract half the size of the image to get to the top left corner position
    x = float(match.group(1)) - image.shape[1] / 2. * pixel_size
    y = float(match.group(2)) - image.shape[0] / 2. * pixel_size
    position_list.append([x, y])
    arrays.append(image)
arrays = [np.expand_dims(np.array(arrays), axis=1)] # ensure channel is set
position_list = np.array(position_list) # has to be a list

print("Stitching tiles with ashlar..")

# Process numpy arrays
process_images(filepaths=arrays,
                output='ashlar_output_numpy.tif',
                align_channel=0,
                flip_x=False,
                flip_y=False,
                flip_mosaic_x=False,
                flip_mosaic_y=False,
                output_channels=None,
                maximum_shift=maximum_shift_microns,
                stitch_alpha=0.01,
                maximum_error=None,
                filter_sigma=0,
                filename_format='cycle_{cycle}_channel_{channel}.tif',
                pyramid=False,
                tile_size=1024,
                ffp=None,
                dfp=None,
                barrel_correction=0,
                plates=False,
                quiet=False, 
                position_list=position_list,
                pixel_size=pixel_size)
#process_single(arrays, 'output_path_format', False, False, None, None, aligner_args, mosaic_args, False, False)

