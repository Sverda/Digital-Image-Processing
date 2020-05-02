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