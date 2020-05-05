import math
import numpy
import collections
from PIL import Image

from ImageDecoder import ImageDecoder
from Unification import Unification
from ImageHelper import ImageHelper
from Commons import Commons

class HistogramColor(object):
    def __init__(self, firstPath, imageType):
        self.firstDecoder = ImageDecoder(firstPath, imageType)
        self.imageType = imageType

    # Ex6.1
    def calculateHistogram(self):
        print('Compute histogram from color image {}'.format(self.firstDecoder.name))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        bins, histogram = Commons.CalculateColorHistogram(image, height, width)
        ImageHelper.SaveColorHistogram(bins, histogram, 'calculate', self.firstDecoder)

    # Ex6.2
    def moveHistogram(self, constValue=(0,0,0)):
        print('Move histogram in color image {} about {}'.format(self.firstDecoder.name, constValue))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        maxValue = float(numpy.iinfo(image.dtype).max)
        minValue = float(numpy.iinfo(image.dtype).min)
        result = numpy.ones((height, width, 3), numpy.uint8)
        for h in range(height):
            for w in range(width):
                computedR = int(image[h, w, 0]) + constValue[0]
                computedR = maxValue if computedR > maxValue else computedR
                computedR = minValue if computedR < minValue else computedR
                result[h, w, 0] = computedR
                computedG = int(image[h, w, 1]) + constValue[1]
                computedG = maxValue if computedG > maxValue else computedG
                computedG = minValue if computedG < minValue else computedG
                result[h, w, 1] = computedG
                computedB = int(image[h, w, 2]) + constValue[2]
                computedB = maxValue if computedB > maxValue else computedB
                computedB = minValue if computedB < minValue else computedB
                result[h, w, 2] = computedB
                
        ImageHelper.Save(result, self.imageType, 'move-histogram-image', False, self.firstDecoder, None, constValue)
        bins, histogram = Commons.CalculateColorHistogram(result, height, width)
        ImageHelper.SaveColorHistogram(bins, histogram, 'move-histogram', self.firstDecoder, constValue)
        
    # Ex6.3
    def extendHistogram(self):
        print('Extend histogram in color image {}'.format(self.firstDecoder.name))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        result = Commons.Normalization(image, image)

        ImageHelper.Save(result, self.imageType, 'extend-histogram-image', False, self.firstDecoder)
        bins, histogram = Commons.CalculateColorHistogram(result, height, width)
        ImageHelper.SaveColorHistogram(bins, histogram, 'extend-histogram', self.firstDecoder)
