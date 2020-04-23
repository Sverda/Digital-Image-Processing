import math
import numpy
import collections
from PIL import Image
from ImageDecoder import ImageDecoder

class ArithmeticSumGray(object):
    def __init__(self, firstPath, secondPath, imageType):
        self.firstDecoder = ImageDecoder(firstPath, imageType)
        self.secondDecoder = ImageDecoder(secondPath, imageType)

    # Ex2.1
    def sumWithConst(self, constValue):
        print('sum gray image {} with const {}'.format(self.firstDecoder.name, constValue))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        
        maxSum = float(numpy.amax(numpy.add(image.astype('uint32'), constValue)))
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