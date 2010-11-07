def getLocation(self, idNumber, size):
    xloc = idNumber % size
    yloc = idNumber / size
    return (xloc, yloc)

def getID(self, (x,y), size):
        idNumber = (y * (size+1)) + x
        return idNumber
