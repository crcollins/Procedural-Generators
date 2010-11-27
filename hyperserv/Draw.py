import math
import Image
import ImageDraw
import random


#heights = range(7*255)
#random.shuffle(heights)


class Draw:
##    def __init__(self, values, size, intPolType="Linear"):
##        self.values = values
##        self.size = size
##        self.intPolType = intPolType
    def __init__(self, values, intPolType="Linear"):
        self.values = values
        self.size = len(values)
        self.intPolType = intPolType
        #self.draw()
        
    def draw(self):
        self.img = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.ImageDraw(self.img)
        minnumbers = []
        maxnumbers = []
        for number in xrange(len(self.values)):
            minnumbers.append(min(self.values[number]))
            maxnumbers.append(max(self.values[number]))
        self.maxNumber = max(maxnumbers) - min(minnumbers)
        self.spreadNum = (self.maxNumber) / 7.0
        for y in xrange(self.size):
            for x in xrange(self.size):
                coords = (x, y)
                colorSet = self.this(self.values[y][x])
                draw.point(coords, colorSet)
        self.img.show()

        
    def this(self, value):
        if value != 0:
            ans = int(value / self.spreadNum)
        else:
            ans = 0
        if ans == 0:
            colorPer = value / self.spreadNum
            colorInt = int(colorPer*255)
            #print "going to red: %i" % (colorInt)
            color = (colorInt, 0, 0)
        elif ans == 1:
            colorPer = (value - self.spreadNum) / self.spreadNum
            colorInt = int(colorPer*255)
            #print "going to yellow: %i" % (colorInt)
            color = (255, colorInt, 0)
        elif ans == 2:
            colorPer = 1.0 - ((value - (2 * self.spreadNum)) / self.spreadNum)
            colorInt = int(colorPer*255)
            #print "going to green: %i" % (colorInt)
            color = (colorInt, 255, 0)
        elif ans == 3:
            colorPer = (value - (3 * self.spreadNum)) / self.spreadNum
            colorInt = int(colorPer*255)
            #print "going to cyan: %i" % (colorInt)
            color = (0, 255, colorInt)
        elif ans == 4:
            colorPer = 1.0 - ((value - (4 * self.spreadNum)) / self.spreadNum)
            colorInt = int(colorPer*255)
            #print "going to blue: %i" % (colorInt)
            color = (0, colorInt, 255)
        elif ans == 5:
            colorPer = (value - (5 * self.spreadNum)) / self.spreadNum
            colorInt = int(colorPer*255)
            #print "going to magenta: %i" % (colorInt)
            color = (colorInt, 0, 255)
        elif ans == 6:
            colorPer = (value - (6 * self.spreadNum)) / self.spreadNum
            colorInt = int(colorPer*255)
            #print "going to white: %i" % (colorInt)
            color = (255, colorInt, 255)
        else:
            #print "white"
            color = (255, 255, 255)
        return color
