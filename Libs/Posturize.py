def posturize(imagename, steps):
    '''This takes and simplifies images so that later they can be\
    optimized for putting in the game (ex: 10 cubes of same height\
    go together rather than in 10 calls. Because of this, it has a\
    similar look to maps in minecraft.'''
    im = Image.open(imagename)
    pixellist = im.load()
    (xsize, ysize) = im.size
    img = Image.new("RGB", (xsize, ysize))
    draw = ImageDraw.ImageDraw(img)
    stepsize = 255.0/(steps)
    mid = 255.0/(steps-1)
    level = {}
    futurepixels = {}
    for number in xrange(steps):
        level[number] = number*mid
    for y in xrange(ysize):
        for x in xrange(xsize):
            (r,g,b) = pixellist[x,y]
            coloravg = (r+g+b)/3.0
            lvlnumber = int(coloravg / stepsize)
            if lvlnumber >= steps:
                lvlnumber = steps - 1
            finalcolor = int(level[lvlnumber])
            colors = (finalcolor, finalcolor, finalcolor)
            coords = (x,y)
            futurepixels[x,y] = lvlnumber
            draw.point(coords, colors)
    img.save("here.png")
    return futurepixels, im.size
