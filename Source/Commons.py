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