import math
import numpy
import collections
from PIL import Image
from DjVuImageDecoder import DjVuImageDecoder

class Filters(object):
    def __init__(self, firstPath):
        self.decoder = DjVuImageDecoder(firstPath)

    # Ex9.1
    def lowPass(self):
        print('low pass filtering start')
        height, width = self.decoder.height, self.decoder.width
        image = self.decoder.getPixels()

        result = numpy.empty((height, width), numpy.uint8)
        mask = numpy.ones((3, 3))

        for y in range(height):
            for x in range(width):
                avg, n = 0, 0
                for iOff in range(-1, 1):
                    for jOff in range(-1, 1):
                        iSafe = y if ((y + iOff) > (height - 1)) else (y + iOff)
                        jSafe = x if ((x + jOff) > (width - 1)) else (x + jOff)
                        avg += image[iSafe, jSafe] * mask[iOff + 1, jOff + 1]
                        n += mask[iOff + 1, jOff + 1]
                avg = int(round(avg/n))
                result[y, x] = avg

        img = Image.fromarray(result, mode='L')
        img.save('Resources/filter-lowpass.png')
        print('low pass filtering done')