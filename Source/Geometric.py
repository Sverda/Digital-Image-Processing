import math
import numpy
import collections
from PIL import Image

from ImageDecoder import ImageDecoder
from ImageHelper import ImageHelper

class GeometricColor(object):
    def __init__(self, firstPath, imageType):
        self.decoder = ImageDecoder(firstPath, imageType)
        self.imageType = imageType

    # Ex4.1
    def translate(self, deltaX = 0, deltaY = 0):
        print('Translation color image {} to point ({},{})'.format(self.decoder.name, deltaX, deltaY))
        height, width = self.decoder.height, self.decoder.width
        image = self.decoder.getPixels()
        result = numpy.zeros((height, width, 3), numpy.uint8)

        for y in range(height):
            for x in range(width):  
                if 0 < y + deltaY < height and 0 < x + deltaX < width:
                    result[y + deltaY][x + deltaX] = image[y][x]
                    
        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'translate', False, self.decoder)

    # Ex4.2
    def homogeneousScaling(self, scale = 1.0):
        print('Homogeneous scaling color image {} about scale {}'.format(self.decoder.name, scale))
        image = self.decoder.getPixels()

        result = self._scale(image, scale, scale)
        self._interpolateColor(result)
        
        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'homogeneous-scaling', False, self.decoder)

    # Ex4.2
    def nonUniformScaling(self, scaleX = 1.0, scaleY = 1.0):
        print('Non-uniform scaling color image {} with scale ({},{})'.format(self.decoder.name, scaleX, scaleY))
        image = self.decoder.getPixels()

        result = self._scale(image, scaleX, scaleY)
        self._interpolateColor(result)
        
        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'nonuniform-scaling', False, self.decoder)

    def _scale(self, matrix, scaleX, scaleY):
        height, width = self.decoder.height, self.decoder.width
        result = numpy.full((height, width, 3), 1, numpy.uint8)
        for y in range(height):
            for x in range(width):  
                if scaleY * y < height and scaleX * x < width:
                    result[int(scaleY * y)][int(scaleX * x)] = matrix[y][x]
        return result

    # Ex4.3
    def rotation(self, phi):
        print('Rotation color image {} about angle {}'.format(self.decoder.name, phi))
        image = self.decoder.getPixels()

        result = self._rotate(image, phi)
        self._interpolateColor(result)
        
        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'rotate', False, self.decoder)

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

    # Ex4.4
    def axisSymmetry(self, ox, oy):
        print('Axis symmetry color image {} on axis {} and {}'.format(self.decoder.name, ox, oy))
        image = self.decoder.getPixels()

        result = self._symmetryOXorOY(image, ox, oy)
        
        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'axis-symmetry-{}-{}'.format(ox, oy), False, self.decoder)

    def _symmetryOXorOY(self, image, ox, oy):
        height, width = self.decoder.height, self.decoder.width
        result = numpy.zeros((height, width, 3), numpy.uint8)
        for y in range(height):
            for x in range(width): 
                if ox and not oy:
                    result[y][x] = image[y][(width-1)-x]
                elif not ox and oy:
                    result[y][x] = image[(height-1)-y][x]
                elif ox and oy:
                    result[y][x] = image[(height-1)-y][(width-1)-x]
        return result

    # Ex4.4
    def customSymmetryX(self, ox):
        print('Custom axis symmetry X color image {} on axis {}'.format(self.decoder.name, ox))
        if not self._validateSymmetryAxisX(ox):
            return

        image = self.decoder.getPixels()
        height, width = self.decoder.height, self.decoder.width
        resultWidth = ox*2
        result = numpy.zeros((height, resultWidth, 3), numpy.uint8)
        for y in range(height):
            for x in range(ox):
                result[y][x] = image[y][x]
                result[y][resultWidth-1-x] = image[y][x]
                
        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'x-symmetry', False, self.decoder, None, ox)

    def _validateSymmetryAxisX(self, ox):
        width = self.decoder.width
        if ox <= 0 or ox > width:
            return False
        return True
    
    # Ex4.4
    def customSymmetryY(self, oy):
        print('Custom axis symmetry Y color image {} on axis {}'.format(self.decoder.name, oy))
        if not self._validateSymmetryAxisY(oy):
            return

        image = self.decoder.getPixels()
        height, width = self.decoder.height, self.decoder.width
        resultHeight = oy*2
        result = numpy.zeros((resultHeight, width, 3), numpy.uint8)
        for y in range(oy):
            for x in range(width):
                result[y][x] = image[y][x]
                result[resultHeight-1-y][x] = image[y][x]
                
        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'y-symmetry', False, self.decoder, None, oy)

    def _validateSymmetryAxisY(self, oy):
        height = self.decoder.height
        if oy <= 0 or oy > height:
            return False
        return True

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

    # Ex4.5
    def crop(self, (x1, y1), (x2, y2)):
        print('Crop image {} from ({},{}) to ({},{})'.format(self.decoder.name, x1, y1, x2, y2))
        image = self.decoder.getPixels()

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                image[y, x] = (0, 0, 0)
                
        ImageHelper.Save(image, self.imageType, 'crop', False, self.decoder)

    # Ex4.6
    def copy(self, (x1, y1), (x2, y2)):
        print('Copy image {} from ({},{}) to ({},{})'.format(self.decoder.name, x1, y1, x2, y2))
        image = self.decoder.getPixels()
        height, width = self.decoder.height, self.decoder.width
        result = numpy.zeros((height, width, 3), numpy.uint8)

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                result[y, x] = image[y, x]
                
        ImageHelper.Save(result, self.imageType, 'copy', False, self.decoder)