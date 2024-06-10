import numpy as np
from ashlar.scripts.ashlar import process_images
# Create example numpy arrays
num_images = 4
num_channels = 2
height, width = 256, 256
arrays = [np.random.rand(num_images, num_channels, height, width)]
# create a 2D list of xy positions 
position_list = np.array(([0, 0], [0, 1], [1, 0], [1, 1]))*260.
pixel_size = 0.5
maximum_shift_microns = 50

# Process numpy arrays
process_images(filepaths=arrays,
                output='ashlar_output.tif',
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

