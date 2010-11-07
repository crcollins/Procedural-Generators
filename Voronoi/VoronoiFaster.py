import math
import random
import Image
import ImageDraw
import time

class VoronoiFaster:
    '''Creates Voronoi/Worley Noise using a 3x3 grid to decrease running time.

Known Problems:
Nonsquare Starting Image
    Results in a messed up image. Problem seems to be\n that blocks are being placed on each other.
clip = 1
    Sorry but no one can divide by 0
'''
    def __init__(self, size, fValue, blockSize,
                 pointsList=None, distType="Linear", seed=None, center=False, clip=0, plated=False, platedColor=True, platedLines=False, minkowskiNumber=4):
        self.size = size
        self.fValue = int(fValue)
        if pointsList == None:
            self.pointsList = []
        else:
            self.pointsList = pointsList
        self.seed = seed
        self.pixelColorNumbers = range(self.size*self.size)
        self.clip = clip
        self.totalBlocks = int((self.size / blockSize) * (self.size / blockSize))
        print "Currently generating %s cell blocks. At and fValue of %f." % (self.totalBlocks, self.fValue)
        self.blockSize = blockSize
        self.distType = distType
        self.plated = plated
        self.platedColor = platedColor
        self.platedLines = platedLines
        self.minkowskiNumber = minkowskiNumber
        self.center = center
        self.otherFValue = 0
        self.new = []

        #if there is no prelisted points then this will make some
        if self.pointsList == []:
            #makes as many points as their are block in the image
            #note: the points made are relative to the block that they are in, so all numbers range from 0 to blocksize - 1
            self.generatePoints(self.totalBlocks)
            #converts the relative points to the absolute location within the image
            #at this point the index number corresponds to what block it is
            #block(0, 0) = pointsList[0], block(1, 0) = pointsList[1]...
            self.xyPoints(self.pointsList)
        if self.plated == True:
            self.generateCellColors(self.totalBlocks)
        if self.center:
            self.cellDist()

        self.main()

    def main(self):
        self.pixID = []
        #loops for total amount of pixels in the image
        for pixels in xrange(self.size * self.size):
            x, y = self.getLocation(pixels)
            xBlock, yBlock = self.getBlock(x, y)
            #finds the neighbors for the pixel
            neighbors, over = self.neighborCheck(xBlock, yBlock)
            #converts the neighbors block coords into xy coords
            neighbors2 = self.over(over, neighbors)
            #finds and saves the distance between the points
            if self.plated == True:
                nothing, ID = self.findNearestPoints(x, y, neighbors2, self.distType)
                self.pixelColorNumbers[pixels] = self.platedCheck(ID, neighbors2)
            elif self.center:
                self.pixelColorNumbers[pixels], relID = self.findNearestPoints(x, y, neighbors2, self.distType)
                absID = self.centerBlock(relID, neighbors2)
                self.pixID.append((absID, relID))
                (nx, ny) = neighbors2[4]
                (bx, by) = self.getBlock(nx, ny)
                blockID = self.getBlockID((bx,by))
                self.new.append(blockID)
            else:
                self.pixelColorNumbers[pixels], nothing = self.findNearestPoints(x, y, neighbors2, self.distType)
        if self.platedLines == True:
            self.draw()
        
    def findNearestPoints(self, x, y, neighbor, distMethod):
        pixelDist = []
        shortest = []
        shortestID = []
        if self.otherFValue != 0:
            fValue = self.otherFValue
        else:
            fValue = self.fValue
        for coords in neighbor:
            #self.lenght returns just the distance between the two points
            distance =  self.lenght((x, y), coords, distMethod)
            pixelDist.append(distance)
        for amount in xrange(fValue):
            #finds smallest distance
            minNum = min(pixelDist)
            idxNum = pixelDist.index(minNum)
            #removes the number from pixelDist and places it in shortest all in one swoop
            shortest.append(pixelDist[idxNum])
            pixelDist[idxNum] = self.size
            shortestID.append(idxNum)
        final = shortest.pop()
        ID = shortestID.pop()
        return final, ID

    def cellDist(self):
        self.neighborDists = []
        self.otherFValue = 2
        distMethod = self.distType
        for cells in self.pointsList:
            dists = []
            (x, y) = cells
            xBlock, yBlock = self.getBlock(x, y)
            neighbors, over = self.neighborCheck(xBlock, yBlock)
            neighbors2 = self.over(over, neighbors)
            nothing, newCoords = self.findNearestPoints(x, y, neighbors2, distMethod)
            for coords in neighbors2:
                if coords == neighbors2[4]:
                    coords = neighbors2[newCoords]
                    if coords == neighbors2[4]:
                        print "help!!!", coords
                here = self.lenght(coords, neighbors2[4], self.distType)
                dists.append(here)
            self.neighborDists.append(dists)
        self.otherFValue = 0
            
    def platedCheck(self, ID, neighbors):
        (x, y) = neighbors[ID]
        if x < 0:
            x += self.size
        if y < 0:
            y += self.size
        if x > self.size:
            x -= self.size
        if y > self.size:
            y -= self.size
        blockCoords = self.getBlock(x, y)
        bID = self.getBlockID(blockCoords)
        return self.cellColors[bID]

    def centerBlock(self, ID, neighbors):
        (x, y) = neighbors[ID]
        if x < 0:
            x += self.size
        if y < 0:
            y += self.size
        if x > self.size:
            x -= self.size
        if y > self.size:
            y -= self.size
        blockCoords = self.getBlock(x, y)
        bID = self.getBlockID(blockCoords)
        return bID

    def test(self):
        for pixel in xrange(self.size * self.size):
            (absID , relID) = self.pixID[pixel]
##            print absID, relID
##            print self.pixelColorNumbers[pixel], self.neighborDists[absID][relID]
            dist = self.neighborDists[absID][relID]
            self.pixelColorNumbers[pixel] = self.pixelColorNumbers[pixel] / dist
            
    def lenght(self, (x1, y1), (x2, y2), method="Linear"):
        dx = x2 - x1
        dy = y2 - y1
        if method == "SqLen":
            distance = (dx*dx+dy*dy)
        elif method == "Manhattan":
            distance = int(abs(dx)+abs(dy))
        elif method == "Chebyshev":
            #all this does is returns the smaller number out of dx and dy, or dx if they are the same
            if abs(dx) == abs(dy) or abs(dx) > abs(dy):
                distance = int(abs(dx))
            else:
                distance = int(abs(dy))
        elif method == "Quadratic":
            distance = (dx*dx+dy*dy+dx*dy)
        elif method == "Minkowski":
            a = ((abs(dx) ** self.minkowskiNumber) + (abs(dy) ** self.minkowskiNumber))
            distance = a ** (1.0/self.minkowskiNumber)
        else:
            distance = math.sqrt(dx*dx+dy*dy)
        return distance

    def generatePoints(self, amountBlocks):
        if self.seed == None:
            self.seed = random.randint(0, 10)
        seed = self.seed
        for number in xrange(amountBlocks):
            random.seed(seed)
            random1 = random.random() * (self.blockSize - 1)
            random.seed(seed+1)
            random2 = random.random() * (self.blockSize - 1)
            #This xyCoord is relative to the top left corner of the block
            self.pointsList.append((random1, random2))
            seed += 1
            
    def generateCellColors(self, amountBlocks):
        if self.seed == None:
            self.seed = random.randint(0, 10)
        seed = self.seed
        self.cellColors = []
        for number in xrange(amountBlocks):
            random.seed(seed)
            random1 = int(random.random() * 255)
            seed += 1
            self.cellColors.append(random1)
                
    def getLocation(self, idNumber):
        xloc = idNumber % self.size
        yloc = idNumber / self.size
        return (xloc, yloc)
    

    def getBlock(self, x, y):
        xblock = int(x / self.blockSize)
        yblock = int(y / self.blockSize)
        return (xblock, yblock)

    def getBlockStartXY(self, ID):
        x = (ID % (self.size / self.blockSize)) * self.blockSize
        y = (ID / (self.size / self.blockSize)) * self.blockSize
        return (x, y)

    def getBlockEndXY(self, ID):
        x = (ID % (self.size / self.blockSize)) * self.blockSize + self.blockSize
        y = (ID / (self.size / self.blockSize)) * self.blockSize + self.blockSize
        return (x, y)

    def getBlockID(self, (xblock, yblock)):
        blockID = int(yblock * (self.size / self.blockSize) + xblock)
        return blockID

    def neighborCheck(self, xblock, yblock):
        #this is just all the blocks in a 3x3 around the block including itself
        neighbors = [(xblock - 1, yblock + 1), (xblock, yblock + 1), (xblock + 1, yblock + 1),
                     (xblock - 1, yblock), (xblock, yblock), (xblock + 1, yblock),
                     (xblock - 1, yblock - 1), (xblock, yblock - 1), (xblock + 1, yblock - 1)]
        over = []
        #this goes through and checks it any of the blocks are off the picture
        maxX = (self.size / self.blockSize) - 1
        for number in xrange(len(neighbors)):
            x, y = neighbors[number]
            overX = 0
            overY = 0
            #this if/then block determines what kind of overshoot it is
            if x < 0:
                x = maxX
                overX = -1
            if y < 0:
                y = maxX
                overY = -1
            if x > maxX:
                x = 0
                overX = 1
            if y > maxX:
                y = 0
                overY = 1
            if overX != 0 or overY != 0:
                #this was going to be a dict, but i ran some tests and it was about 10% slower
                #structure is: (theIDfortheNumberinNeighbors, (typeOverX, typeOverY))
                over.append((number, (overX, overY)))
            neighbors[number] = (x, y)
        return neighbors, over

    def over(self, over, neighbors):
        neighborsIDs = []
        for roundNumber in xrange(len(neighbors)):
            #this converts all of the blockCoords into what ID they are
            #this is to associate them back with their point from self.pointsList
            neighborsIDs.append(self.getBlockID(neighbors[roundNumber]))
        #neighbors is cleared to get ready for the new numbers to be put in
        neighbors = []
        for nID in neighborsIDs:
            #this puts the xycoords from pointsList into neighbors
            neighbors.append(self.pointsList[nID])
        #now it goes through and checks to see which neighbor IDs have problems and corrects them
        for neighborID, (xOverBlock, yOverBlock) in over:
            x, y = neighbors[neighborID]
            #note: if it a point needs correcting it is moved a full image dimension across.
            #this means that the new numbers will be < 0 and > the height or width
            #this allows for the image to be tiled
            if xOverBlock == 1:
                x = x + self.size
            if xOverBlock == -1:
                x = x - self.size
            if yOverBlock == 1:
                y = y + self.size
            if yOverBlock == -1:
                y = y - self.size
            neighbors[neighborID] = (x, y)
        return neighbors

    def xyPoints(self, numList):
        #this goes through and makes all the points go from being relative to the block to being absolute
        for number in xrange(len(numList)):
            x, y = numList[number]
            #the block starting position
            xB, yB = self.getBlockStartXY(number)
            x = x + xB
            y = y + yB
            numList[number] = (x, y)
            
    def showIt(self, color="color", pointsOn=False,pointsColor=(0,0,0), border=False):
        #this was added in just to visualize all the blocks, and points
        img = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.ImageDraw(img)
        for number in xrange(len(self.pointsList)):
            start = self.getBlockStartXY(number)
            end = self.getBlockEndXY(number)
            #random generation of color of rectangles
            color1 = random.randint(0, 255)
            color2 = random.randint(0, 255)
            color3 = random.randint(0, 255)
            colorSet = (color1, color2, color3)
            if color == "mono":
                colorSet = (color1, color1, color1)
            elif color == "none":
                colorSet = (255, 255, 255)
            if border == True:
                draw.rectangle([start, end], fill=colorSet, outline="black")
            else:
                draw.rectangle([start, end], fill=colorSet)
        if pointsOn == True:
            for x, y in self.pointsList:
                draw.point((x, y), fill=pointsColor)
        img.show()
        img.save("test.png")

    def draw(self):
        #all the PIL stuff
        self.img = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.ImageDraw(self.img)

        #This is where the colors of the pixels are determined
        #I am currently in search of a new way to do this
        if self.plated == True:
            for pixel in xrange(self.size * self.size):
                x, y = self.getLocation(pixel)
                colorSet = self.pixelColorNumbers[pixel]
                draw.point((x, y), (colorSet, colorSet, colorSet))
            if self.platedLines == True:
                self.img2 = Image.new("RGB", (self.size, self.size), (255, 255, 255))
                draw2 = ImageDraw.ImageDraw(self.img2)
                for pixel in xrange(self.size * self.size):
                    x, y = self.getLocation(pixel)
                    border = self.isBorder((x,y))
                    if border == True:
                        draw2.point((x, y), (0,0,0))
                        self.pixelColorNumbers[pixel] = 1
                    else:
                        self.pixelColorNumbers[pixel] = 0
                self.img = self.img2
        else:
            if min(self.pixelColorNumbers) < 0:
                self.minNumber = min(self.pixelColorNumbers)
                self.maxNumber = max(self.pixelColorNumbers) - self.minNumber
            else:
                self.minNumber = min(self.pixelColorNumbers)
                self.maxNumber = max(self.pixelColorNumbers) - self.minNumber
            self.colorSpread = 255 / self.maxNumber
            #coloring
            if min(self.pixelColorNumbers) < 0:
                for pixel in xrange(self.size * self.size):
                    coords = self.getLocation(pixel)
                    color = int(self.colorSpread * (self.pixelColorNumbers[pixel] - self.minNumber))
                    colorSet = (color, color, color)
                    draw.point(coords, colorSet)
            else:
                for pixel in xrange(self.size * self.size):
                    coords = self.getLocation(pixel)
                    color = int(self.colorSpread * (self.pixelColorNumbers[pixel] - self.minNumber))
                    colorSet = (color, color, color)
                    draw.point(coords, colorSet)

    def isBorder(self, (x, y)):
        neighbors = [(x-1, y+1), (x, y+1), (x+1, y+1),
                     (x-1, y), (x+1, y),
                     (x-1, y-1), (x, y-1), (x+1, y-1)]
        over = []
        for number in xrange(len(neighbors)):
            x, y = neighbors[number]
            maxX = self.size - 1
            maxY = self.size - 1
            if x < 0:
                x = maxX
            if y < 0:
                y = maxY
            if x > maxX:
                x = 0
            if y > maxY:
                y = 0
            neighbors[number] = (x, y)
        getPixelColor = self.img.load()
        for (nx, ny) in neighbors:
            ncolor = getPixelColor[nx, ny]
            color = getPixelColor[x, y]
            if ncolor != color:
                return True
        return False
    
    def showMe(self):
        #more PIL stuff
        self.img.show()
        name = "Voronoi_" + self.distType + "_%s_" % (self.seed) + str(self.fValue) + ".png"
        self.img.save(name)

    def totals(self):
        #for diagnostic only
        print "self.def_main =", self.def_main
        print "self.def_findNearestPoints =", self.def_findNearestPoints
        print "self.def_lenght =", self.def_lenght
        print "self.def_generatePoints =", self.def_generatePoints
        print "self.def_getLocation =", self.def_getLocation
        print "self.def_getBlock =", self.def_getBlock
        print "self.def_getBlockStartXY =", self.def_getBlockStartXY
        print "self.def_getBlockEndXY =", self.def_getBlockEndXY
        print "self.def_getBlockID =", self.def_getBlockID
        print "self.def_neighborCheck =", self.def_neighborCheck
        print "self.def_xyPoints =", self.def_xyPoints
        print "self.def_showIt =", self.def_showIt
        print "self.def_draw =", self.def_draw

#start = time.time()
#thing = VoronoiFaster(100, 1, 10, distType="Linear", plated=True, platedColor=False)
#thing.showMe()
#print time.time() - start
##thing = VoronoiFaster(200, 1, 25, seed=1)
##thing.draw()
##thing.showMe()
##thing = VoronoiFaster(200, 1, 25, distType="SqLen", seed=1)
##thing.draw()
##thing.showMe()
##thing = VoronoiFaster(200, 1, 25, distType="Manhattan", seed=1)
##thing.draw()
##thing.showMe()
##thing = VoronoiFaster(200, 1, 25, distType="Chebyshev", seed=1)
##thing.draw()
##thing.showMe()
##thing = VoronoiFaster(200, 1, 25, distType="Quadratic", seed=1)
##thing.draw()
##thing.showMe()
##thing = VoronoiFaster(200, 1, 25, distType="Minkowski", seed=1, minkowskiNumber=1)
##thing.draw()
##thing.showMe()
##thing = VoronoiFaster(200, 1, 25, distType="Minkowski", seed=1, minkowskiNumber=3)
##thing.draw()
##thing.showMe()
