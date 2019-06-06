import math
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

    # Ex4.2
    def homogeneousScaling(self, scale = 1.0):
        print('homogeneous scaling start')
        image = self.decoder.getPixels24Bits()

        print('scaling')
        result = self._scale(image, scale)
        print('interpolation')
        self._interpolateColor(result)

        img = Image.fromarray(result, mode='RGB')
        img.save('Resources/hsGeometric.png')
        print('homogeneous scaling done')

    def _scale(self, matrix, scaleXY):
        return self._scale(matrix, scaleXY, scaleXY)

    # Ex4.3
    def nonUniformScaling(self, scaleX = 1.0, scaleY = 1.0):
        print('non-uniform scaling start')
        image = self.decoder.getPixels24Bits()

        print('scaling')
        result = self._scale(image, scaleX, scaleY)
        print('interpolation')
        self._interpolateColor(result)

        img = Image.fromarray(result, mode='RGB')
        img.save('Resources/nusGeometric.png')
        print('non-uniform scaling done')

    def _scale(self, matrix, scaleX, scaleY):
        height, width = self.decoder.height, self.decoder.width
        result = numpy.full((height, width, 3), 1, numpy.uint8)
        for y in range(height):
            for x in range(width):  
                if scaleY * y < height and scaleX * x < width:
                    result[int(scaleY * y)][int(scaleX * x)] = matrix[y][x]
        return result

    # Ex4.4
    def rotation(self, phi):
        print('rotation start')
        image = self.decoder.getPixels24Bits()

        print('rotating')
        result = self._rotate(image, phi)
        print('interpolation')
        self._interpolateColor(result)

        img = Image.fromarray(result, mode='RGB')
        img.save('Resources/rGeometric.png')
        print('rotation done')

    def _rotate(self, image, phi):
        height, width = self.decoder.height, self.decoder.width
        result = numpy.full((height, width, 3), 1, numpy.uint8)
        radian = math.radians(phi)
        for y in range(height):
            for x in range(width): 
                newX = x*math.cos(radian) - y*math.sin(radian)
                newY = x*math.sin(radian) + y*math.cos(radian)
                if newY < height and newY >= 0 and newX >= 0 and newX < width:
                    result[int(newY)][int(newX)] = image[y][x]
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
                            if (result[hSafe, wSafe][0] > 0) | (result[hSafe, wSafe][1] > 0) | (result[hSafe, wSafe][2] > 0):
                                r += result[hSafe, wSafe][0]
                                g += result[hSafe, wSafe][1]
                                b += result[hSafe, wSafe][2]
                                n += 1
                    result[h, w] = (r/n, g/n, b/n)