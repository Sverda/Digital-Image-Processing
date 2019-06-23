import math
import numpy
import collections
from PIL import Image
from DjVuImageDecoder import DjVuImageDecoder

class Filters(object):
    def __init__(self, firstPath):
        self.decoder = DjVuImageDecoder(firstPath)

    # Ex9.1
    def lowPassBoxBlur(self, kernelSize=(9,9)):
        print('box blur with size {}x{} start'.format(kernelSize[0], kernelSize[1]))
        height, width = self.decoder.height, self.decoder.width
        image = self.decoder.getPixels()

        result = numpy.empty((height, width), numpy.uint8)
        kernel = numpy.ones(kernelSize)

        kernelHeight, kernelWidth = kernel.shape
        overlapHeight, overlapWidth = int(math.ceil(kernelHeight/2)), int(math.ceil(kernelWidth/2))
        for y in range(height):
            for x in range(width):
                average, hitsCount = 0, 0
                for yOff in range(-overlapHeight, overlapHeight):
                    for xOff in range(-overlapWidth, overlapWidth):
                        ySafe = y if ((y + yOff) > (height - 1) or (y + yOff) < 0) else (y + yOff)
                        xSafe = x if ((x + xOff) > (width - 1) or (x + xOff) < 0) else (x + xOff)
                        average += image[ySafe, xSafe] * kernel[yOff + 1, xOff + 1]
                        hitsCount += kernel[yOff + 1, xOff + 1]
                average = int(round(average/hitsCount))
                result[y, x] = average

        img = Image.fromarray(result, mode='L')
        img.save('Resources/filter-boxblur{}x{}.png'.format(kernelSize[0], kernelSize[1]))
        print('box blur with size {}x{} start'.format(kernelSize[0], kernelSize[1]))