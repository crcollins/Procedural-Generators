import Image

import base
import cubes

from hypershade.cubescript import playerCS, CSCommand
from hyperserv.servercommands import ServerError

class UseImage:
    def __init__(self, imagename, cubesize=16):
        self.imagename = imagename
        self.im = Image.open(self.imagename)
        self.pixels = self.im.load()
        (self.xsize, self.ysize) = self.im.size
        self.cubesize = cubesize
        
    def makeSurface(self):
        '''This makes a map based off on a heightmap. Note that \
        it only creates a suface rather than a full block.'''
        for y in xrange(self.ysize):
            for x in xrange(self.xsize):
                (r,g,b) = self.pixels[x,y]
                avg = int((r + g + b) / 3)
                cubes.makecube(caller,x,y,avg,self.cubesize)

    def makeVolume(self, base=10, steps=10, p=True):
        '''This makes a full map with depth based on a height map.\
        Base determines the amount of cubes under the lowest point \
        on the heightmap. '''
        if p:
            pixels = posturize(steps)
            makeVCubesP(pixels, base)
        else:
            makeVCubes()

    def makeVCubes(self):
        '''This makes the volume cubes without posturization.'''
        for y in xrange(self.ysize):
            for x in xrange(self.xsize):
                (r,g,b) = self.pixels[x,y]
                avg = int((r + g + b) / 3)
                cubes.makecolumn(caller,x,y,0,avg,self.cubesize)

    def makeVCubesP(self, pixels, base):
        '''This makes the volume cubes with posturization.'''
        #fills in base... someday
        #cubes.makecolumn(caller,x,y,0,self.xsize, self.ysize,base,self.cubesize)
        
        for y in xrange(self.ysize):
            for x in xrange(self.xsize):
                relheight = pixels[x,y]
                if relheight == 0:
                    pass
                else:
                    cubes.makecolumn(caller,x,y,base,relheight+base,self.cubesize)

    def posturize(self, steps):
        '''This takes and simplifies images so that later they can be\
        optimized for putting in the game (ex: 10 cubes of same height\
        go together rather than in 10 calls. Because of this, it has a\
        similar look to maps in minecraft.'''
        #img = Image.new("RGB", (xsize, ysize))
        #draw = ImageDraw.ImageDraw(img)
        stepsize = 255.0/(steps)
        mid = 255.0/(steps-1)
        level = {}
        futurepixels = {}
        for number in xrange(steps):
            level[number] = number*mid
        for y in xrange(ysize):
            for x in xrange(xsize):
                lvlnumber = int(coloravg / stepsize)
                if lvlnumber >= steps:
                    lvlnumber = steps - 1
                futurepixels[x,y] = lvlnumber
        return futurepixels

'''
Examples:

a = cube("someimage.png")


a.makeSurface()
This would output just the surface cubes. Note that it is
based on absolute height based on the pixel colors.


a.makeVolume()
This would output a full volume map with the presets of
a base of 10 and 10 height steps. Meaning the heightest
point on the map would be 20 cubes high.

a.makeVolume(p=False)
This would be the same as the makeSurface() except it would have volume.
'''
