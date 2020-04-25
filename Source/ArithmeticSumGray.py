import math
import numpy
import collections
from PIL import Image

from ImageDecoder import ImageDecoder
from Unification import Unification

class ArithmeticSumGray(object):
    def __init__(self, firstPath, secondPath, imageType):
        self.firstDecoder = ImageDecoder(firstPath, imageType)
        self.secondDecoder = ImageDecoder(secondPath, imageType)

    # Ex2.1
    def sumWithConst(self, constValue):
        print('sum gray image {} with const {}'.format(self.firstDecoder.name, constValue))
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

        img = Image.fromarray(result, mode='L')
        img.save('Resources/result/sum-gray-const-{}.png'.format(constValue))

        maxValue = numpy.iinfo(image.dtype).max
        fmin = numpy.amin(result)
        fmax = numpy.amax(result)
        result = result.astype(numpy.float32)
        result = maxValue * ((result - fmin) / (fmax - fmin))
        result = result.astype(numpy.uint8)
        
        img = Image.fromarray(result, mode='L')
        img.save('Resources/result/sum-gray-const-{}-norm.png'.format(constValue))
        
    # Ex2.1
    def sumImages(self):
        print('sum gray image {} with image {}'.format(self.firstDecoder.name, self.secondDecoder.name))
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

        img = Image.fromarray(result, mode='L')
        img.save('Resources/result/sum-gray-images.png')

        maxValue = numpy.iinfo(firstImage.dtype).max
        fmin = numpy.amin(result)
        fmax = numpy.amax(result)
        result = result.astype(numpy.float32)
        result = maxValue * ((result - fmin) / (fmax - fmin))
        result = result.astype(numpy.uint8)
        
        img = Image.fromarray(result, mode='L')
        img.save('Resources/result/sum-gray-images-norm.png')

    # Ex2.2
    def multiplyWithConst(self, constValue):
        print('multiply gray image {} with const {}'.format(self.firstDecoder.name, constValue))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        maxValue = numpy.iinfo(image.dtype).max
        result = numpy.ones((height, width), numpy.uint8)
        
        for h in range(height):
            for w in range(width):
                pom = image[h, w] * constValue
                result[h, w] = pom if pom <= maxValue else maxValue

        img = Image.fromarray(result, mode='L')
        img.save('Resources/result/multiply-gray-const-{}.png'.format(constValue))

        maxValue = numpy.iinfo(image.dtype).max
        fmin = numpy.amin(result)
        fmax = numpy.amax(result)
        result = result.astype(numpy.float32)
        result = maxValue * ((result - fmin) / (fmax - fmin))
        result = result.astype(numpy.uint8)
        
        img = Image.fromarray(result, mode='L')
        img.save('Resources/result/multiply-gray-const-{}-norm.png'.format(constValue))

    # Ex2.2
    def multiplyImages(self):
        print('multiply gray image {} with image {}'.format(self.firstDecoder.name, self.secondDecoder.name))
        unification = Unification(self.firstDecoder.name, self.secondDecoder.name, 'L')
        firstImage, secondImage = unification.grayUnification()
        width, height = firstImage.shape[0], firstImage.shape[1]
        
        maxValue = float(numpy.iinfo(firstImage.dtype).max)
        result = numpy.ones((height, width), numpy.uint8)
        for h in range(height):
            for w in range(width):
                pom = int(firstImage[h, w]) * int(secondImage[h, w]) / maxValue
                result[h, w] = pom

        img = Image.fromarray(result, mode='L')
        img.save('Resources/result/multiply-gray-images.png')

        maxValue = numpy.iinfo(firstImage.dtype).max
        fmin = numpy.amin(result)
        fmax = numpy.amax(result)
        result = result.astype(numpy.float32)
        result = maxValue * ((result - fmin) / (fmax - fmin))
        result = result.astype(numpy.uint8)
        
        img = Image.fromarray(result, mode='L')
        img.save('Resources/result/multiply-gray-images-norm.png')