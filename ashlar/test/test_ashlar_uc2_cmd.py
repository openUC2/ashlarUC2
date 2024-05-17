import os
import re
from datetime import datetime
import tifffile

# adjust to dataset:
input_dir = "/Users/bene/Dropbox/File requests/Raster Anabel Marr/input/"
#input_dir = r"C:\\Users\\T490\\Documents\\Anabel\\Bachelorarbeit\\Bilder\\Kontrastraster\\"

output_dir = "/Users/bene/Dropbox/File requests/Raster Anabel Marr/"

pixel_size = 0.327
maximum_shift_microns = 50

timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# adjust to desired output directories:
collected_tiles_file = os.path.join(input_dir, f'PATH_TO_TILE_COLLECTION.ome.tif')
ashlar_output_file = 'ashlar_output_cmd.tif'

# Get the list of files
images = os.listdir(input_dir)
images.sort()

with tifffile.TiffWriter(collected_tiles_file) as tif:
    for img_name in images:
        if img_name.find('tif') < 0: 
            continue
        image = tifffile.imread(input_dir + img_name)
        if img_name.find('ome') >= 0:
            continue
        match = re.search(r'\((.*?), (.*?)\)', img_name)
        # the positions in the file names provide the center of the tile,
        # # we need to subtract half the size of the image to get to the top left corner position
        x = float(match.group(1)) - image.shape[1] / 2. * pixel_size
        y = float(match.group(2)) - image.shape[0] / 2. * pixel_size
        print("Writing %s into OME-TIF at position %s:%s.." % (img_name, x, y))
        metadata = {
			'Pixels': {
				'PhysicalSizeX': pixel_size,
				'PhysicalSizeXUnit': 'µm',
				'PhysicalSizeY': pixel_size,
				'PhysicalSizeYUnit': 'µm'
			},
			'Plane': {
				'PositionX': x,
				'PositionY': y
			}
		}
        print(metadata)
        tif.write(image, metadata=metadata)

print("Stitching tiles with ashlar..")
from ashlar.scripts import ashlar
ashlar.main(['', collected_tiles_file, '-o', ashlar_output_file, '-m%s' % maximum_shift_microns]) # original