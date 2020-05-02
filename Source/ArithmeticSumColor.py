import math
import numpy
import collections
from PIL import Image

from ImageDecoder import ImageDecoder
from Unification import Unification
from ImageHelper import ImageHelper
from Commons import Commons

class ArithmeticSumColor(object):
    def __init__(self, firstPath, secondPath, imageType):
        self.firstDecoder = ImageDecoder(firstPath, imageType)
        self.secondDecoder = ImageDecoder(secondPath, imageType)
        self.imageType = imageType

    # Ex3.1
    def sumWithConst(self, constValue):
        print('Sum color image {} with const {}'.format(self.firstDecoder.name, constValue))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()

        maxSum = float(numpy.amax(numpy.add(image.astype(numpy.uint32), constValue)))
        maxValue = float(numpy.iinfo(image.dtype).max)
        scaleFactor = (maxSum - maxValue) / maxValue if maxSum > maxValue else 0

        result = numpy.ones((height, width, 3), numpy.uint8)
        for h in range(height):
            for w in range(width):
                R = (image[h, w, 0] - (image[h, w, 0] * scaleFactor)) + (constValue - (constValue * scaleFactor))
                G = (image[h, w, 1] - (image[h, w, 1] * scaleFactor)) + (constValue - (constValue * scaleFactor))
                B = (image[h, w, 2] - (image[h, w, 2] * scaleFactor)) + (constValue - (constValue * scaleFactor))
                result[h, w] = [numpy.ceil(R), numpy.ceil(G), numpy.ceil(B)]

        ImageHelper.Save(result, self.imageType, 'sum-color-const', False, self.firstDecoder, None, constValue)
        result = Commons.Normalization(image, result)
        ImageHelper.Save(result, self.imageType, 'sum-color-const', True, self.firstDecoder, None, constValue)
        
    # Ex3.1
    def sumImages(self):
        print('Sum color image {} with image {}'.format(self.firstDecoder.name, self.secondDecoder.name))
        unification = Unification(self.firstDecoder.name, self.secondDecoder.name, self.imageType)
        firstImage, secondImage = unification.colorUnification()
        width, height = firstImage.shape[0], firstImage.shape[1]
        
        maxSum = float(
            numpy.amax(
                numpy.add(firstImage.astype(numpy.uint32), 
                          secondImage.astype(numpy.uint32))))
        maxValue = float(numpy.iinfo(firstImage.dtype).max)
        scaleFactor = (maxSum - maxValue) / maxValue if maxSum > maxValue else 0
        
        result = numpy.ones((height, width, 3), numpy.uint8)
        for h in range(height):
            for w in range(width):
                R = (firstImage[h, w, 0] - (firstImage[h, w, 0] * scaleFactor)) + (secondImage[h, w, 0] - (secondImage[h, w, 0] * scaleFactor))
                G = (firstImage[h, w, 1] - (firstImage[h, w, 1] * scaleFactor)) + (secondImage[h, w, 1] - (secondImage[h, w, 1] * scaleFactor))
                B = (firstImage[h, w, 2] - (firstImage[h, w, 2] * scaleFactor)) + (secondImage[h, w, 2] - (secondImage[h, w, 2] * scaleFactor))
                result[h, w] =  [numpy.ceil(R), numpy.ceil(G), numpy.ceil(B)]

        ImageHelper.Save(result, self.imageType, 'sum-color-images', False, self.firstDecoder, self.secondDecoder)
        result = Commons.Normalization(firstImage, result)
        ImageHelper.Save(result, self.imageType, 'sum-color-images', True, self.firstDecoder, self.secondDecoder)