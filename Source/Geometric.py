import numpy
import collections
from PIL import Image
from DjVuImageDecoder import DjVuImageDecoder

class Geometric(object):
    def __init__(self, firstPath):
        self.decoder = DjVuImageDecoder(firstPath)

    # Ex4.1
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

    def homogeneousScaling(self, scale = 1.0):
        print('homogeneous scaling start')
        image = self.decoder.getPixels24Bits()

        print('scaling')
        result = self._scaleXY(image, scale)
        print('interpolation')
        self._interpolateColor(result)

        img = Image.fromarray(result, mode='RGB')
        img.save('Resources/hsGeometric.png')
        print('homogeneous scaling done')

    def _scaleXY(self, matrix, scale):
        height, width = self.decoder.height, self.decoder.width
        result = numpy.full((height, width, 3), 1, numpy.uint8)
        for y in range(height):
            for x in range(width):  
                if scale * y < height and scale * x < width:
                    result[int(scale * y)][int(scale * x)] = matrix[y][x]
        return result

    def _interpolateColor(self, result):
        height, width = self.decoder.height, self.decoder.width
        for h in range(height):
            for w in range(width):
                r, g, b = 0, 0, 0
                n = 0
                if (result[h, w][0] == 1) & (result[h, w][1] == 1) & (result[h, w][2] == 1):
                    for hOff in range(-1, 2):
                        for wOff in range(-1, 2):
                            hSafe = h if ((h + hOff) > (height - 2)) | ((h + hOff) < 0) else (h + hOff)
                            wSafe = w if ((w + wOff) > (width - 2)) | ((w + wOff) < 0) else (w + wOff)
                            if (result[hSafe, wSafe][0] > 1) | (result[hSafe, wSafe][1] > 1) | (result[hSafe, wSafe][2] > 1):
                                r += result[hSafe, wSafe][0]
                                g += result[hSafe, wSafe][1]
                                b += result[hSafe, wSafe][2]
                                n += 1
                    result[h, w] = (r/n, g/n, b/n)