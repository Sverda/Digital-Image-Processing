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
    def CalculateHistogram(image, height, width):
        maxValue = numpy.iinfo(image.dtype).max
        histogram = numpy.zeros(maxValue+1, numpy.uint32)
        for h in range(height):
            for w in range(width):
                bin = image[h, w]
                histogram[bin] += 1

        bins = numpy.arange(maxValue+2).astype(numpy.uint32)
        return bins, histogram