import math
import Image
import ImageDraw

class Draw:
    def __init__(self, values, size, intPolType="Linear"):
        self.values = values
        self.size = size
        self.intPolType = intPolType
        
    def getLocation(self, idNumber):
        xloc = idNumber % (self.size)
        yloc = idNumber / (self.size)
        return (xloc, yloc)
        
    def draw(self):
        self.img = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.ImageDraw(self.img)
        self.minNumber = min(self.values)
        self.maxNumber = max(self.values) - self.minNumber
        for pixel in xrange((self.size) * (self.size)):
            coords = self.getLocation(pixel)
            self.values[pixel] = self.values[pixel] / self.maxNumber
            number = self.interpolate(self.values[pixel])
            color = int(255 * number)
            colorSet = (color, color, color)
            draw.point(coords, colorSet)
        self.img.show()

    def write(self):
        for y in xrange(self.size):
            for x in xrange(self.size):
                ID = self.getID((x,y))
                string = "%.3f " % self.heights[ID]
                sys.stdout.write(string)
            sys.stdout.write("\n")

    def interpolate(self, x):
        if self.intPolType == "sin":
            ans = self.sin(x)
        elif self.intPolType == "smoothStep":
            ans = self.smoothStep(x)
        elif self.intPolType == "squared":
            ans = self.squared(x)
        elif self.intPolType == "sqrt":
            ans = self.sqrt(x)
        elif self.intPolType == "cubed":
            ans = self.cubed(x)
        elif self.intPolType == "cubedrt":
            ans = self.cubert(x)
        else:
            ans = self.linear(x)
        return ans
			
    def linear(self, x):
        y = x
        return y

    def smoothStep(self, x):
        y = (3 * x)**2 - (2 * x)**3
        return y
    
    def squared(self, x):
        y = x**2
        return y

    def sqrt(self, x):
        y = x**.5
        return y

    def cubed(self, x):
        y = x**3
        return y

    def cubert(self, x):
        y = x**float(1/3)
        return y

    def sin(self, x):
        y = math.sin(x)
        return y
    
