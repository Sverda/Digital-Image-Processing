import math
import numpy
import collections
from PIL import Image
from DjVuImageDecoder import DjVuImageDecoder

class GrayMorphological(object):
    def __init__(self, firstPath):
        self.decoder = DjVuImageDecoder(firstPath)

    # Ex8.1
    def erosion(self, seHeight, seWidth, seDepth, seCenter=(0, 0)):
        print('erosion start')
        image = self.decoder.getPixels()

        structuralElement = numpy.full((seHeight, seWidth), seDepth, numpy.uint8)
        result = self._erosionOperation(image, structuralElement, seCenter)

        img = Image.fromarray(result, mode='L')
        img.save('Resources/morph-gray-erosion-strel{}x{}-{}.png'.format(str(seHeight), str(seWidth), str(seDepth)))
        print('erosion done')

    # Ex8.2
    def dilation(self, seHeight, seWidth, seDepth, seCenter=(0, 0)):
        print('dilation start')
        image = self.decoder.getPixels()

        structuralElement = numpy.full((seHeight, seWidth), seDepth, numpy.uint8)
        result = self._dilationOperation(image, structuralElement, seCenter)

        img = Image.fromarray(result, mode='L')
        img.save('Resources/morph-gray-dilation-strel{}x{}-{}.png'.format(str(seHeight), str(seWidth), str(seDepth)))
        print('dilation done')

    #Ex8.3
    def opening(self, seHeight, seWidth, seDepth, seCenter=(0, 0)):
        print('opening start')
        image = self.decoder.getPixels()
        
        structuralElement = numpy.full((seHeight, seWidth), seDepth, numpy.uint8)
        result = self._erosionOperation(image, structuralElement, seCenter)
        result = self._dilationOperation(result, structuralElement, seCenter)

        img = Image.fromarray(result, mode='L')
        img.save('Resources/morph-gray-opening-strel{}x{}-{}.png'.format(str(seHeight), str(seWidth), str(seDepth)))
        print('opening done')

    #Ex8.4
    def closing(self, seHeight, seWidth, seDepth, seCenter=(0, 0)):
        print('closing start')
        image = self.decoder.getPixels()

        structuralElement = numpy.full((seHeight, seWidth), seDepth, numpy.uint8)
        result = self._dilationOperation(image, structuralElement, seCenter)
        result = self._erosionOperation(result, structuralElement, seCenter)

        img = Image.fromarray(result, mode='L')
        img.save('Resources/morph-gray-closing-strel{}x{}-{}.png'.format(str(seHeight), str(seWidth), str(seDepth)))
        print('closing done')
    
    def _dilationOperation(self, image, structuralElement, elementCenterIndices=(0, 0)):
        image32 = image.copy().astype(numpy.int32)
        height, width = self.decoder.height, self.decoder.width
        result32 = numpy.zeros((height, width), numpy.int32)
        structuralElement32 = structuralElement.copy().astype(numpy.int32)

        seHeight, seWidth = structuralElement32.shape
        seHalfY, seHalfX = seHeight-1-elementCenterIndices[0], seWidth-1-elementCenterIndices[1]
        minY, minX = seHalfY, seHalfX
        maxY, maxX = height-(seHeight-minY), width-(seWidth-minX)
        for y in range(minY, maxY):
            for x in range(minX, maxX):
                neighbourPixels = structuralElement32.copy()
                for seY in range(-seHalfY, seHalfY):
                    for seX in range(-seHalfX, seHalfX):
                        neighbourPixels[seY][seX] = image32[y+seY][x+seX] + structuralElement32[seY][seX]
                result32[y][x] = numpy.amax(neighbourPixels)
        result8 = numpy.clip(result32, 0, 255).astype(numpy.uint8)
        return result8

    def _erosionOperation(self, image, structuralElement, elementCenterIndices=(0, 0)):
        image32 = image.copy().astype(numpy.int32)
        height, width = self.decoder.height, self.decoder.width
        result32 = numpy.zeros((height, width), numpy.int32)
        structuralElement32 = structuralElement.copy().astype(numpy.int32)

        seHeight, seWidth = structuralElement32.shape
        seHalfY, seHalfX = seHeight-1-elementCenterIndices[0], seWidth-1-elementCenterIndices[1]
        minY, minX = seHalfY, seHalfX
        maxY, maxX = height-(seHeight-minY), width-(seWidth-minX)
        for y in range(minY, maxY):
            for x in range(minX, maxX):
                neighbourPixels = structuralElement32.copy()
                for seY in range(-seHalfY, seHalfY):
                    for seX in range(-seHalfX, seHalfX):
                        neighbourPixels[seY][seX] = image32[y+seY][x+seX] - structuralElement32[seY][seX]
                result32[y][x] = numpy.amin(neighbourPixels)
        result8 = numpy.clip(result32, 0, 255).astype(numpy.uint8)
        return result8
