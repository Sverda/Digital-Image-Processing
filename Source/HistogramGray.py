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
        bins, histogram = Commons.CalculateGrayHistogram(image, height, width)
        ImageHelper.SaveGrayHistogram(bins, histogram, 'calculate', False, self.firstDecoder)

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
        bins, histogram = Commons.CalculateGrayHistogram(result, height, width)
        ImageHelper.SaveGrayHistogram(bins, histogram, 'move-histogram', False, self.firstDecoder, None, constValue)

    # Ex5.3
    def extendHistogram(self):
        print('Extend histogram in gray image {}'.format(self.firstDecoder.name))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        result = Commons.Normalization(image, image)

        ImageHelper.Save(result, self.imageType, 'extend-histogram-image', False, self.firstDecoder)
        bins, histogram = Commons.CalculateGrayHistogram(result, height, width)
        ImageHelper.SaveGrayHistogram(bins, histogram, 'extend-histogram', False, self.firstDecoder)
        
    # Ex5.4
    def localThresholding(self, contrastThreshold, windowSize=3):
        print('Local thresholding gray image {} with contrast threshold of {}'.format(self.firstDecoder.name, contrastThreshold))
        if windowSize % 2 == 0:
            raise ValueError("Window size can't be even")

        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        maxValue = int(numpy.iinfo(image.dtype).max)
        minValue = int(numpy.iinfo(image.dtype).min)
        if contrastThreshold <= minValue or contrastThreshold >= maxValue:
            raise ValueError("Contrast threshold has to be in range of ({},{})".format(minValue, maxValue))

        result = numpy.zeros((height, width), numpy.uint8)
        overlap = int(math.ceil(windowSize/2))
        for h in range(height):
            for w in range(width):
                minH = minValue if h-overlap < 0 else h-overlap
                maxH = maxValue if h+overlap+1 > height else h+overlap+1
                minW = minValue if w-overlap < 0 else w-overlap
                maxW = maxValue if w+overlap+1 > height else w+overlap+1
                if minH >= maxH or minW >= maxW:
                    continue

                window = image[minH:maxH, minW:maxW]
                localMin = numpy.amin(window)
                localMax = numpy.amax(window)
                localContrast = localMax-localMin
                midGray = (int(localMax)+int(localMin))/2
                if localContrast < contrastThreshold:
                    if midGray >= maxValue/2:
                        result[minH:maxH, minW:maxW] = numpy.full((maxH-minH, maxW-minW), maxValue)
                    else:
                        result[minH:maxH, minW:maxW] = numpy.full((maxH-minH, maxW-minW), minValue)
                else:
                    if image[h, w] >= midGray:
                        result[h, w] = maxValue
                    else:
                        result[h, w] = minValue


        ImageHelper.Save(result, self.imageType, 'local-threshold-image', False, self.firstDecoder, None, contrastThreshold)
        bins, histogram = Commons.CalculateGrayHistogram(result, height, width)
        ImageHelper.SaveGrayHistogram(bins, histogram, 'local-threshold', False, self.firstDecoder, None, contrastThreshold)
        
    # Ex5.5
    def globalThresholding(self, threshold):
        print('Global thresholding gray image {} with threshold value of {}'.format(self.firstDecoder.name, threshold))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        maxValue = int(numpy.iinfo(image.dtype).max)
        minValue = int(numpy.iinfo(image.dtype).min)
        if threshold <= minValue or threshold >= maxValue:
            raise ValueError("Threshold has to be in range of ({},{})".format(minValue, maxValue))

        result = numpy.zeros((height, width), numpy.uint8)
        for h in range(height):
            for w in range(width):
                result[h, w] = maxValue if image[h, w] >= threshold else minValue


        ImageHelper.Save(result, self.imageType, 'global-threshold-image', False, self.firstDecoder, None, threshold)
        bins, histogram = Commons.CalculateGrayHistogram(result, height, width)
        ImageHelper.SaveGrayHistogram(bins, histogram, 'global-threshold', False, self.firstDecoder, None, threshold)