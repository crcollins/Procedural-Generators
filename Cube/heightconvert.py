import Image

def makeSurfaceCubes(imagename):
    '''This makes a map based off on a heightmap. Note that \
    it only creates a suface rather than a full block.'''
    im = Image.open(imagename)
    pixels = im.load()
    (xsize, ysize) = im.size
    cubelist = open("cubelist.txt", "w")
    add = str(im.size)+"\n\n"
    cubelist.write(add)
    #line = "Cube: "
    for y in xrange(ysize):
        for x in xrange(xsize):
            (r,g,b) = pixels[x,y]
            if r == g and g == b:
                coords = "(%i, %i, %i)\n" % (x,y,r)
            else:
                avg = (r + g + b) / 3
                coords = "(%i, %i, %i)\n" % (x,y,avg)
            cubelist.write(coords)

def makeCubes(pixels, size, base):
    '''This makes a full map with depth based on a height map.\
    Base determines the amount of cubes under the lowest point \
    on the heightmap. Note for this you must run "minecraft" to\
    get the size and pixels.'''
    cubelist = open("cubelist.txt", "w")
    xsize, ysize = size
    add = str(size)+"\n\n"
    cubelist.write(add)
    for y in xrange(ysize):
        for x in xrange(xsize):
            relheight = pixels[x,y]
            coords = ("(%i, %i, 0)" % (x,y))
            selection = "(1, 1, %i)\n" % (relheight+base)
            cubelist.write(coords+selection)

