import math
import numpy
import collections
from PIL import Image

class Commons(object):
    @staticmethod
    def Normalization(image, result):
        maxValue = numpy.iinfo(image.dtype).max
        fmin = numpy.amin(result)
        fmax = numpy.amax(result)
        result = result.astype(numpy.float32)
        result = maxValue * ((result - fmin) / (fmax - fmin))
        result = result.astype(numpy.uint8)
        return result
    
    @staticmethod
    def CalculateGrayHistogram(image, height, width):
        maxValue = numpy.iinfo(image.dtype).max
        histogram = numpy.zeros(maxValue+1, numpy.uint32)
        for h in range(height):
            for w in range(width):
                bin = image[h, w]
                histogram[bin] += 1

        bins = numpy.arange(maxValue+2).astype(numpy.uint32)
        return bins, histogram
    
    @staticmethod
    def CalculateColorHistogram(image, height, width):
        maxValue = numpy.iinfo(image.dtype).max
        histogram = numpy.zeros((3, maxValue+1), numpy.uint32)
        for h in range(height):
            for w in range(width):
                r = image[h, w, 0]
                g = image[h, w, 1]
                b = image[h, w, 2]
                histogram[0, r] += 1
                histogram[1, g] += 1
                histogram[2, b] += 1

        bins = numpy.arange(maxValue+1).astype(numpy.uint32)
        return bins, histogram