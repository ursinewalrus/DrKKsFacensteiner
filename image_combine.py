from os import listdir
from PIL import Image
from os.path import isfile, join

path = "./meat_factory/"
height = 0;
width = 0
nsize = 128,128

files = [Image.open(path + f) for f in listdir(path)]
for f in files:
	f.thumbnail(nsize,Image.ANTIALIAS)
# files = [f.thumbnail((250,250)) for f in files]
width = sum(f.size[0] for f in files)
height = max(f.size[1] for f in files)

joined_image = Image.new("RGB",(width,height))

width_offset = 0
for f in files:
	joined_image.paste(f,(width_offset,0))
	width_offset += f.size[0]
	
joined_image.save('faces.jpg')