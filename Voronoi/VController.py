import VoronoiFaster
import math
import random
import Image
import ImageDraw
import Interpolation

class Voronoi:
    def __init__(self, size, blockSize=None, octave=None, fValue=None, clip=0, center=False,
                 seed=None, distType="Linear", plated=False, platedColor=True, platedLines=False, minkowskiNumber=4, intPolType="Linear"):
        self.size = size
        self.octave = octave
        self.blockSize = blockSize
        self.fValue = fValue
        self.seed = seed
        self.clip = clip
        self.center = center
        self.distType= distType
        self.plated = plated
        self.platedColor = platedColor
        self.platedLines = platedLines
        self.minkowskiNumber = minkowskiNumber
        self.new = []
        self.intPolType = intPolType

        if self.seed == None:
            self.seed = random.randint(0, 10)
        if self.fValue == None:
            self.fValue = [1]
        if self.octave == None:
            self.octave = [1]
        if self.blockSize == None:
            self.blockSize = [10]
        self.fValueParser()
        self.octaveParser()
        self.blockSizeParser()
        self.main()
        self.draw()

    def fValueParser(self):
        self.fValueRun = []
        self.fValueOld = self.fValue
        self.fValue = []
        for number in xrange(len(self.fValueOld)):
            if self.fValueOld[number] != 0:
                self.fValueRun.append(number+1)
                self.fValue.append(self.fValueOld[number])
                
    def octaveParser(self):
        self.octaveRun = []
        self.octaveOld = self.octave
        self.octave = []
        for number in xrange(len(self.octaveOld)):
            if self.octaveOld[number] != 0:
                self.octaveRun.append(number+1)
                self.octave.append(self.octaveOld[number])

    def blockSizeParser(self):
        self.blockSizeOld = self.blockSize
        self.blockSize = []
        for number in xrange(len(self.blockSizeOld)):
            if self.blockSizeOld[number] != 0:
                self.blockSize.append(self.blockSizeOld[number])

    def main(self):
        self.octaveLoop()

    def octaveLoop(self):
        self.octaveNumbers = []
        for number in xrange(len(self.octaveRun)):
            blockSize = self.blockSize[number]
            self.fValueLoop(blockSize)
            a = self.fValueNumbers
            b = self.octave[number]
            if len(self.octave) == 1:
                if self.octave[number] != 1:
                    self.octaveNumbers = self.mult(a, b)
                else:
                    self.octaveNumbers = a
            else:
                self.octaveNumbers.append(self.mult(a, b))
                if len(self.octaveNumbers) == 2:
                    new = zip(self.octaveNumbers[0], self.octaveNumbers[1])
                    self.octaveNumbers = []
                    newer = []
                    if len(self.octave) == number + 1:
                        for pair in new:
                            self.octaveNumbers.append(sum(pair))
                    else:
                        for pair in new:
                            newer.append(sum(pair))
                        self.octaveNumbers.append(newer)

    def fValueLoop(self, blockSize):
        self.fValueNumbers = []
        self.pixIDs = []
        a = []
        for number in xrange(len(self.fValueRun)):
            fValue = self.fValueRun[number]
            thing = VoronoiFaster.VoronoiFaster(self.size, fValue, blockSize, distType=self.distType, seed=self.seed, center=self.center,
                                                plated=self.plated, platedColor=self.platedColor, platedLines=self.platedLines, minkowskiNumber=self.minkowskiNumber)
            if self.center:
                a.append(thing.pixelColorNumbers)
                self.dists = thing.neighborDists
                self.pixIDs.append(thing.pixID)
                self.new.append(thing.new)
                if len(a) > 1:
                    d = zip(a[0], a[1])
                    for num in xrange(len(d)):
                        d[num] = sum(d[num])
                    for num in xrange(len(d)):
                        print self.new[0][num], self.new[1][num]
                        print self.pixIDs[0][num], self.pixIDs[1][num]
                        firstID = self.pixIDs[0][num][0]
                        secondID = self.pixIDs[1][num][1]
                        secondID = 1
                        dist = self.dists[firstID][secondID]
                        percent = d[num] / dist
                        d[num] = percent
                    self.fValueNumbers = d
                    
            else:
                a = thing.pixelColorNumbers
                b = self.fValue[number]
                if len(self.fValueRun) == 1:
                    self.fValueNumbers = self.mult(a, b)
                else:
                    self.fValueNumbers.append(self.mult(a, b))
                    if len(self.fValueNumbers) == 2:
                        new = zip(self.fValueNumbers[0], self.fValueNumbers[1])
                        self.fValueNumbers = []
                        for pair in new:
                            self.fValueNumbers.append(sum(pair))

    def mult(self, aList, multNumber):
        for number in xrange(len(aList)):
            aList[number] *= multNumber
        return aList

    def getLocation(self, idNumber):
        xloc = idNumber % self.size
        yloc = idNumber / self.size
        return (xloc, yloc)
    
    def draw(self):
        self.img = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.ImageDraw(self.img)
        self.minNumber = min(self.octaveNumbers)
        self.maxNumber = max(self.octaveNumbers) - self.minNumber
        for pixel in xrange(self.size * self.size):
            coords = self.getLocation(pixel)
            self.octaveNumbers[pixel] = self.octaveNumbers[pixel] / self.maxNumber
            number = Interpolation.Interpolation(self.octaveNumbers[pixel], self.intPolType)
            color = int(255 * number.y)
            colorSet = (color, color, color)
            draw.point(coords, colorSet)
        self.img.show()
            
        
    def oldDraw(self):
        self.img = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.ImageDraw(self.img)
        self.minNumber = min(self.octaveNumbers)
        self.maxNumber = max(self.octaveNumbers) - self.minNumber
        self.colorSpread = 255 / (self.maxNumber * (1 - self.clip)) 
        for pixel in xrange(self.size * self.size):
            coords = self.getLocation(pixel)
            color = int(self.colorSpread * (self.octaveNumbers[pixel] - self.minNumber))
            colorSet = (color, color, color)
            draw.point(coords, colorSet)

        self.img.show()

##thing1 = Voronoi(400, 1, 80, fValue=[-1, 1], seed=42)
##thing1.draw()
##thing1.img.save("Voronoi.1Oct.png")
