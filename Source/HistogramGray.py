import math
import numpy
import collections
from PIL import Image

from ImageDecoder import ImageDecoder
from Unification import Unification
from ImageHelper import ImageHelper
from Commons import Commons

class HistogramGray(object):
    def __init__(self, firstPath, imageType):
        self.firstDecoder = ImageDecoder(firstPath, imageType)
        self.imageType = imageType

    # Ex5.1
    def calculateHistogram(self):
        print('Compute histogram from gray image {}'.format(self.firstDecoder.name))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        bins, histogram = Commons.CalculateHistogram(image, height, width)
        ImageHelper.SaveHistogram(bins, histogram, 'calculate', False, self.firstDecoder)

    # Ex5.2
    def moveHistogram(self, constValue):
        print('Move histogram in gray image {} about {}'.format(self.firstDecoder.name, constValue))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        maxValue = float(numpy.iinfo(image.dtype).max)
        minValue = float(numpy.iinfo(image.dtype).min)
        result = numpy.ones((height, width), numpy.uint8)
        for h in range(height):
            for w in range(width):
                computed = int(image[h, w]) + constValue
                computed = maxValue if computed > maxValue else computed
                computed = minValue if computed < minValue else computed
                result[h, w] = computed
                
        ImageHelper.Save(result, self.imageType, 'move-histogram-image', False, self.firstDecoder, None, constValue)
        bins, histogram = Commons.CalculateHistogram(result, height, width)
        ImageHelper.SaveHistogram(bins, histogram, 'move-histogram', False, self.firstDecoder, None, constValue)

    # Ex5.3
    def extendHistogram(self):
        print('Extend histogram in gray image {}'.format(self.firstDecoder.name))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        result = Commons.Normalization(image, image)

        ImageHelper.Save(result, self.imageType, 'extend-histogram-image', False, self.firstDecoder)
        bins, histogram = Commons.CalculateHistogram(result, height, width)
        ImageHelper.SaveHistogram(bins, histogram, 'extend-histogram', False, self.firstDecoder)