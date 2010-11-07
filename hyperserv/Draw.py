import math
import Image
import ImageDraw

class Draw:
    def __init__(self, values, size, intPolType="Linear"):
        self.values = values
        self.size = size
        self.intPolType = intPolType
        
    def draw(self):
        self.img = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.ImageDraw(self.img)
        minnumbers = []
        maxnumbers = []
        for number in xrange(len(self.values)):
            minnumbers.append(min(self.values[number]))
            maxnumbers.append(max(self.values[number]))
        self.maxNumber = max(maxnumbers) - min(minnumbers)
        
        for y in xrange(self.size):
            for x in xrange(self.size):
                coords = (x,y)
                self.values[y][x] = self.values[y][x] / self.maxNumber
                number = self.interpolate(self.values[y][x])
                color = int(255 * number)
                colorSet = (color, color, color)
                draw.point(coords, colorSet)
        self.img.show()

    def write(self):
        for y in xrange(self.size):
            for x in xrange(self.size):
                string = "%.3f " % self.values[y][x]
                sys.stdout.write(string)
            sys.stdout.write("\n")

    def interpolate(self, x):
        if self.intPolType == "sin":
            ans = math.sin(x)
        elif self.intPolType == "smoothStep":
            ans = (3 * x)**2 - (2 * x)**3
        elif self.intPolType == "squared":
            ans = x**2
        elif self.intPolType == "sqrt":
            ans = x**.5
        elif self.intPolType == "cubed":
            ans = x**3
        elif self.intPolType == "cubedrt":
            ans = x**float(1/3)
        else:
            ans = x
        return ans
