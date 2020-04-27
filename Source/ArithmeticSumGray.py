import math
import numpy
import collections
from PIL import Image

from ImageDecoder import ImageDecoder
from Unification import Unification
from ImageHelper import ImageHelper

class ArithmeticSumGray(object):
    def __init__(self, firstPath, secondPath, imageType):
        self.firstDecoder = ImageDecoder(firstPath, imageType)
        self.secondDecoder = ImageDecoder(secondPath, imageType)
        self.imageType = imageType

    # Ex2.1
    def sumWithConst(self, constValue):
        print('Sum gray image {} with const {}'.format(self.firstDecoder.name, constValue))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        
        maxSum = float(numpy.amax(numpy.add(image.astype(numpy.uint32), constValue)))
        maxValue = float(numpy.iinfo(image.dtype).max)
        scaleFactor = (maxSum - maxValue) / maxValue if maxSum > maxValue else 0
        
        result = numpy.ones((height, width), numpy.uint8)
        for h in range(height):
            for w in range(width):
                pom = (image[h, w] - (image[h, w] * scaleFactor)) + (constValue - (constValue * scaleFactor))
                result[h, w] = numpy.ceil(pom)

        ImageHelper.Save(result, self.imageType, 'sum-gray-const', False, self.firstDecoder, None, constValue)

        maxValue = numpy.iinfo(image.dtype).max
        fmin = numpy.amin(result)
        fmax = numpy.amax(result)
        result = result.astype(numpy.float32)
        result = maxValue * ((result - fmin) / (fmax - fmin))
        result = result.astype(numpy.uint8)
        
        ImageHelper.Save(result, self.imageType, 'sum-gray-const', True, self.firstDecoder, None, constValue)
        
    # Ex2.1
    def sumImages(self):
        print('Sum gray image {} with image {}'.format(self.firstDecoder.name, self.secondDecoder.name))
        unification = Unification(self.firstDecoder.name, self.secondDecoder.name, 'L')
        firstImage, secondImage = unification.grayUnification()
        width, height = firstImage.shape[0], firstImage.shape[1]
        
        maxSum = float(
            numpy.amax(
                numpy.add(firstImage.astype(numpy.uint32), 
                          secondImage.astype(numpy.uint32))))
        maxValue = float(numpy.iinfo(firstImage.dtype).max)
        scaleFactor = (maxSum - maxValue) / maxValue if maxSum > maxValue else 0
        
        result = numpy.ones((height, width), numpy.uint8)
        for h in range(height):
            for w in range(width):
                pom = (firstImage[h, w] - (firstImage[h, w] * scaleFactor)) + (secondImage[h, w] - (secondImage[h, w] * scaleFactor))
                result[h, w] = numpy.ceil(pom)

        ImageHelper.Save(result, self.imageType, 'sum-gray-images', False, self.firstDecoder, self.secondDecoder)

        maxValue = numpy.iinfo(firstImage.dtype).max
        fmin = numpy.amin(result)
        fmax = numpy.amax(result)
        result = result.astype(numpy.float32)
        result = maxValue * ((result - fmin) / (fmax - fmin))
        result = result.astype(numpy.uint8)
        
        ImageHelper.Save(result, self.imageType, 'sum-gray-images', True, self.firstDecoder, self.secondDecoder)


    # Ex2.2
    def multiplyWithConst(self, constValue):
        print('Multiply gray image {} with const {}'.format(self.firstDecoder.name, constValue))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        maxValue = numpy.iinfo(image.dtype).max
        result = numpy.ones((height, width), numpy.uint8)
        
        for h in range(height):
            for w in range(width):
                pom = image[h, w] * constValue
                result[h, w] = pom if pom <= maxValue else maxValue

        ImageHelper.Save(result, self.imageType, 'multiply-gray-const', False, self.firstDecoder, None, constValue)

        maxValue = numpy.iinfo(image.dtype).max
        fmin = numpy.amin(result)
        fmax = numpy.amax(result)
        result = result.astype(numpy.float32)
        result = maxValue * ((result - fmin) / (fmax - fmin))
        result = result.astype(numpy.uint8)
        
        ImageHelper.Save(result, self.imageType, 'multiply-gray-const', True, self.firstDecoder, None, constValue)

    # Ex2.2
    def multiplyImages(self):
        print('Multiply gray image {} with image {}'.format(self.firstDecoder.name, self.secondDecoder.name))
        unification = Unification(self.firstDecoder.name, self.secondDecoder.name, 'L')
        firstImage, secondImage = unification.grayUnification()
        width, height = firstImage.shape[0], firstImage.shape[1]
        
        maxValue = float(numpy.iinfo(firstImage.dtype).max)
        result = numpy.ones((height, width), numpy.uint8)
        for h in range(height):
            for w in range(width):
                pom = int(firstImage[h, w]) * int(secondImage[h, w]) / maxValue
                result[h, w] = pom

        ImageHelper.Save(result, self.imageType, 'multiply-gray-images', False, self.firstDecoder, self.secondDecoder)

        maxValue = numpy.iinfo(firstImage.dtype).max
        fmin = numpy.amin(result)
        fmax = numpy.amax(result)
        result = result.astype(numpy.float32)
        result = maxValue * ((result - fmin) / (fmax - fmin))
        result = result.astype(numpy.uint8)
        
        ImageHelper.Save(result, self.imageType, 'multiply-gray-images', True, self.firstDecoder, self.secondDecoder)

    # Ex2.3
    def blendImages(self, ratio):
        print('Blending gray image {} with image {} and ratio {}'.format(self.firstDecoder.name, self.secondDecoder.name, ratio))
        if ratio < 0 or ratio > 1.0:
            raise ValueError('ratio is wrong')

        unification = Unification(self.firstDecoder.name, self.secondDecoder.name, 'L')
        firstImage = unification.scaleUpGray(self.firstDecoder)
        secondImage = unification.scaleUpGray(self.secondDecoder)
        width, height = firstImage.shape[0], firstImage.shape[1]
        
        result = numpy.ones((height, width), numpy.uint8)
        for h in range(height):
            for w in range(width):
                pom = ratio * firstImage[h, w] + (1 - ratio) * secondImage[h, w]
                result[h, w] = pom

        ImageHelper.Save(result, self.imageType, 'blend-gray-images', False, self.firstDecoder, None, ratio)

    # Ex2.4
    def powerFirstImage(self, powerIndex):
        print('Power gray image {} with image {} and index {}'.format(self.firstDecoder.name, self.secondDecoder.name, powerIndex))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        
        maxValue = float(numpy.iinfo(image.dtype).max)
        result = numpy.ones((height, width), numpy.uint32)
        for h in range(height):
            for w in range(width):
                result[h, w] = image[h, w]**powerIndex

        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'power-gray', False, self.firstDecoder, None, powerIndex)

        maxValue = numpy.iinfo(image.dtype).max
        fmin = numpy.amin(result)
        fmax = numpy.amax(result)
        result = result.astype(numpy.float32)
        result = maxValue * ((result - fmin) / (fmax - fmin))
        result = result.astype(numpy.uint8)
        
        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'power-gray', True, self.firstDecoder, None, powerIndex)