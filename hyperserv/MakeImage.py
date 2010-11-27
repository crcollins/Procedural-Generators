import math
import random
import Draw

#octave
#lacunarity
#frequency = lacunarity ** octave

class DiamondSquare:
    def __init__(self, mean, volatility, size, start=None, seed=None, intPolType="Linear"):
        if seed == None:
            seed = random.randrange(100000)
        self.seed = seed
        self.startseed = seed
        self.start = start
        self.size = size
        self.corners = [(0,0),(0,self.size), (self.size, 0), (self.size, self.size)]
        self.intPolType = intPolType
        self.mean = mean
        self.volatility = volatility
        
        self.makeList()
        self.logsize = int(math.log(self.size, 2))
        self.loop()
        self.hey = Draw.Draw(self.heights, self.intPolType)
        self.hey.draw()

    def save(self, imagename):
        self.hey.img.save(imagename)

    def makeList(self):
        self.heights =[]
        for y in xrange(self.size+1):
            b = []
            for x in xrange(self.size+1):
                b.append(0)
            self.heights.append(b)
        if self.start == None:
            count = self.seed * 34
            self.start = []
            random.seed(count)
            for x in xrange(4):
                self.start.append(random.random())
                count+=1
                random.seed(count)
        for number in xrange(len(self.start)):
            (x,y) = self.corners[number]
            self.heights[y][x] = self.start[number]
                

    def getDeltaMV(self, level):
        delta = 2 ** level
        #print delta,"---", level
        a = self.mean / float(delta)
        b = self.volatility / float(math.sqrt(delta))
        return a,b

    def square(self, coords, delta, level):
        self.solveAdj(coords, delta, level)

    def diamond(self, coords, delta, level):
        self.solveDiag(coords, delta, level)

    def diamondPoints(self, level):
        level += 1
        points = []
        delta = 2 ** (self.logsize - (level))
        for y in xrange(0, 2**level, 2):
            for x in xrange(0, 2**level, 2):
                endx = int(float((x + 1)) / float((2 ** level)) * self.size)
                endy = int(float((y + 1)) / float((2 ** level)) * self.size)
                points.append((endx,endy))
        #print points, delta
        print delta
        if delta >= 1:
            for x, y in points:
                self.diamond((x,y),delta, level)
                self.square((int(x-delta), y), delta, level)
                #print "Left"
                self.square((x, int(y-delta)), delta, level)
                #print "Up"
                self.square((int(x+delta), y), delta, level)
                #print "Right"
                self.square((x, int(y+delta)), delta, level)
                #print "Down\n"

    def loop(self):
        #print self.logsize
        for level in xrange(self.logsize):
            level
            print level
            self.diamondPoints(level)
            #print "\n"

    def gBm(self, deltamean, deltavol, deltaheight):
        self.nextSeed()
        height = math.e**(deltamean+(random.gauss(0,1)*deltavol))*deltaheight
        return height

    def solveAdj(self, center, delta, level):
        x,y = center
        delta_height = self.getNeighborsAvgAdj(center, delta)
        delta_mean, delta_volatility = self.getDeltaMV(level)
        #height = delta_height
        height = self.gBm(delta_mean, delta_volatility, delta_height)
        self.heights[y][x] = height

    def solveDiag(self, center, delta, level):
        x,y = center
        delta_height = self.getNeighborsAvgDiag(center, delta)
        delta_mean, delta_volatility = self.getDeltaMV(level)
        #height = delta_height
        height = self.gBm(delta_mean, delta_volatility, delta_height)
        #print height
        self.heights[y][x] = height

    def getNeighborsAvgDiag(self, center, delta):
        [cx, cy] = center
        a = (self.heights[cy+delta][cx-delta] + self.heights[cy-delta][cx-delta] + self.heights[cy-delta][cx+delta] + self.heights[cy+delta][cx+delta]) / 4
        return a

    def getNeighborsAvgAdj(self, center, delta):
        [cx, cy] = center
        ux, uy = [cx, cy+delta]
        lx, ly = [cx-delta, cy]
        dx, dy = [cx, cy-delta]
        rx, ry = [cx+delta, cy]
        here = []
        if ux >= 0 and uy >= 0 and ux <= self.size and uy <= self.size:
            here.append((ux, uy))
        if lx >= 0 and ly >= 0 and lx <= self.size and ly <= self.size:
            here.append((lx, ly))
        if dx >= 0 and dy >= 0 and dx <= self.size and dy <= self.size:
            here.append((dx, dy))
        if rx >= 0 and ry >= 0 and rx <= self.size and ry <= self.size:
            here.append((rx, ry))
        add = []
        for x,y in here:
            add.append(self.heights[y][x])
        #print sum(add), len(add)
        return sum(add) / float(len(add))
        
    def nextSeed(self):
        self.seed += 1
        random.seed(self.seed)
