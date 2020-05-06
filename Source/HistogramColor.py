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
        
    # Ex6.4
    def localSingleThresholding(self, contrastThreshold=15, windowSize=3):
        print('Local single thresholding color image {} with contrast threshold of {}'.format(self.firstDecoder.name, contrastThreshold))
        if windowSize % 2 == 0:
            raise ValueError("Window size can't be even")

        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        maxValue = int(numpy.iinfo(image.dtype).max)
        minValue = int(numpy.iinfo(image.dtype).min)
        if contrastThreshold <= minValue or contrastThreshold >= maxValue:
            raise ValueError("Contrast threshold has to be in range of ({},{})".format(minValue, maxValue))

        result = numpy.zeros((height, width, 3), numpy.uint8)
        overlap = int(math.ceil(windowSize/2))
        for h in range(height):
            for w in range(width):
                minH = 0 if h-overlap < 0 else h-overlap
                maxH = height if h+overlap+1 > height else h+overlap+1
                minW = 0 if w-overlap < 0 else w-overlap
                maxW = width if w+overlap+1 > width else w+overlap+1
                if minH >= maxH or minW >= maxW:
                    continue

                window = image[minH:maxH, minW:maxW]
                for color in range(3):
                    localMin = numpy.amin(window[:, :, color])
                    localMax = numpy.amax(window[:, :, color])
                    localContrast = localMax-localMin
                    midColor = (int(localMax)+int(localMin))/2
                    if localContrast < contrastThreshold:
                        if midColor >= maxValue/2:
                            result[minH:maxH, minW:maxW, color] = numpy.full((maxH-minH, maxW-minW), maxValue)
                        else:
                            result[minH:maxH, minW:maxW, color] = numpy.full((maxH-minH, maxW-minW), minValue)
                    else:
                        if image[h, w, color] >= midColor:
                            result[h, w, color] = maxValue
                        else:
                            result[h, w, color] = minValue


        ImageHelper.Save(result, self.imageType, 'single-local-threshold-image', False, self.firstDecoder, None, contrastThreshold)
        bins, histogram = Commons.CalculateColorHistogram(result, height, width)
        ImageHelper.SaveColorHistogram(bins, histogram, 'single-local-threshold', self.firstDecoder)
        
    # Ex6.5
    def localMultiThresholding(self, amountOfThresholds=4, windowSize=3):
        print('Local multi thresholding color image {} with amount of thresholds equals to {}'.format(self.firstDecoder.name, amountOfThresholds))
        if windowSize % 2 == 0:
            raise ValueError("Window size can't be even")

        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()

        result = numpy.zeros((height, width, 3), numpy.uint8)
        overlap = int(math.ceil(windowSize/2))
        for h in range(height):
            for w in range(width):
                minH = 0 if h-overlap < 0 else h-overlap
                maxH = height if h+overlap+1 > height else h+overlap+1
                minW = 0 if w-overlap < 0 else w-overlap
                maxW = width if w+overlap+1 > width else w+overlap+1
                if minH >= maxH or minW >= maxW:
                    continue

                window = image[minH:maxH, minW:maxW]
                for color in range(3):
                    localMax = float(numpy.amax(window[:, :, color]))
                    scale = localMax / (amountOfThresholds-1) if localMax != 0 else 1
                    result[h, w, color] = int(round(image[h, w, color] / scale)) * int(scale)


        ImageHelper.Save(result, self.imageType, 'multi-local-threshold-image', False, self.firstDecoder, None, amountOfThresholds)
        bins, histogram = Commons.CalculateColorHistogram(result, height, width)
        ImageHelper.SaveColorHistogram(bins, histogram, 'multi-local-threshold', self.firstDecoder, amountOfThresholds)
        
    # Ex6.6
    def globalSingleThresholding(self):
        print('Global single thresholding color image {}'.format(self.firstDecoder.name))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        maxValue = int(numpy.iinfo(image.dtype).max)
        minValue = int(numpy.iinfo(image.dtype).min)

        thresholdR = numpy.mean(image[:, :, 0])
        thresholdG = numpy.mean(image[:, :, 1])
        thresholdB = numpy.mean(image[:, :, 2])

        result = numpy.zeros((height, width, 3), numpy.uint8)
        for h in range(height):
            for w in range(width):
                result[h, w, 0] = maxValue if image[h, w, 0] >= thresholdR else minValue
                result[h, w, 1] = maxValue if image[h, w, 1] >= thresholdG else minValue
                result[h, w, 2] = maxValue if image[h, w, 2] >= thresholdB else minValue


        ImageHelper.Save(result, self.imageType, 'single-global-threshold-image', False, self.firstDecoder)
        bins, histogram = Commons.CalculateColorHistogram(result, height, width)
        ImageHelper.SaveColorHistogram(bins, histogram, 'single-global-threshold', self.firstDecoder)
        
    # Ex6.7
    def globalMultiThresholding(self, amountOfThresholds=4):
        print('Global multi thresholding color image {} with amount of thresholds equals to {}'.format(self.firstDecoder.name, amountOfThresholds))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()

        maxR = numpy.amax(image[:, :, 0])
        maxG = numpy.amax(image[:, :, 1])
        maxB = numpy.amax(image[:, :, 2])
        scaleR = maxR / (amountOfThresholds-1)
        scaleG = maxG / (amountOfThresholds-1)
        scaleB = maxB / (amountOfThresholds-1)

        result = numpy.zeros((height, width, 3), numpy.uint8)
        for h in range(height):
            for w in range(width):
                result[h, w, 0] = int(round(image[h, w, 0] / scaleR)) * int(scaleR)
                result[h, w, 1] = int(round(image[h, w, 1] / scaleG)) * int(scaleG)
                result[h, w, 2] = int(round(image[h, w, 2] / scaleB)) * int(scaleB)


        ImageHelper.Save(result, self.imageType, 'multi-global-threshold-image', False, self.firstDecoder, None, amountOfThresholds)
        bins, histogram = Commons.CalculateColorHistogram(result, height, width)
        ImageHelper.SaveColorHistogram(bins, histogram, 'multi-global-threshold', self.firstDecoder, amountOfThresholds)