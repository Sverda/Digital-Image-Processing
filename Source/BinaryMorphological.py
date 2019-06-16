import math
import numpy
import collections
from PIL import Image
from DjVuImageDecoder import DjVuImageDecoder

class BinaryMorphological(object):
    def __init__(self, firstPath):
        self.decoder = DjVuImageDecoder(firstPath)

    # Ex7.1
    def erosion(self):
        print('erosion start')
        height, width = self.decoder.height, self.decoder.width
        image = self.decoder.getPixels()
        result = numpy.zeros((height, width), numpy.uint8)

        minY, minX = 1, 1
        maxY, maxX = height-1, width-1
        for y in range(minY, maxY):
            for x in range(minX, maxX):
                neighbourPixels = [255, 255, 255, 255]

                neighbourPixels[0]=(image[y][x-1])
                neighbourPixels[1]=(image[y-1][x])
                neighbourPixels[2]=(image[y][x+1])
                neighbourPixels[3]=(image[y+1][x])

                if 255 in neighbourPixels:
                    result[y][x] = 255
                else:
                    result[y][x] = 0

        img = Image.fromarray(result, mode='L')
        img.save('Resources/morph-erosion.png')
        print('erosion done')