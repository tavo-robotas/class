from PIL import Image, ImageFilter
import os

size_300 = (300, 300)
size_700 = (700, 700)

cwd = os.getcwd()
loc = os.path.join(cwd + '/data/board/')

for f in os.listdir(loc):
    if f.endswith('.JPG'):
        i = Image.open(loc + f)

        fn, fext = os.path.splitext(f)

        #i.thumbnail(size_300)
        i.rotate(90).filter(ImageFilter.GaussianBlur(8)).convert(mode='L').save(f'{loc}/300/{fn}_300{fext}')
        #i.save(f'{loc}/300/{fn}_300{fext}')
