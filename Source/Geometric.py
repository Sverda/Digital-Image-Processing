import numpy
import collections
from PIL import Image
from DjVuImageDecoder import DjVuImageDecoder

class Geometric(object):
    def __init__(self, firstPath):
        self.decoder = DjVuImageDecoder(firstPath)

    def translate(self, deltaX = 0, deltaY = 0):
        print('translation start')
        height, width = self.decoder.height, self.decoder.width
        image = self.decoder.getPixels24Bits()
        result = numpy.zeros((height, width, 3), numpy.uint8)

        for y in range(height):
            for x in range(width):  
                if 0 < y + deltaY < height and 0 < x + deltaX < width:
                    result[y + deltaY][x + deltaX] = image[y][x]

        img = Image.fromarray(result, mode='RGB')
        img.save('Resources/tGeometric.png')
        print('translation done')