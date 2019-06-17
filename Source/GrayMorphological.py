import math
import numpy
import collections
from PIL import Image
from DjVuImageDecoder import DjVuImageDecoder

class GrayMorphological(object):
    def __init__(self, firstPath):
        self.decoder = DjVuImageDecoder(firstPath)

    # Ex8.1
    def erosion(self, seHeight, seWidth, seDepth):
        print('erosion start')
        image = self.decoder.getPixels()

        structuralElement = numpy.full((seHeight, seWidth), seDepth, numpy.uint8)
        result = self._erosionOperation(image, structuralElement, (4, 4))

        img = Image.fromarray(result, mode='L')
        img.save('Resources/morph-gray-erosion-strel{}x{}-{}.png'.format(str(seHeight), str(seWidth), str(seDepth)))
        print('erosion done')

    # Ex8.2
    def dilation(self):
        print('dilation start')
        image = self.decoder.getPixels()

        result = self._dilationOperation(image)

        img = Image.fromarray(result, mode='L')
        img.save('Resources/morph-gray-dilation.png')
        print('dilation done')

    #Ex8.3
    def opening(self):
        print('opening start')
        image = self.decoder.getPixels()

        result = self._erosionOperation(image)
        result = self._dilationOperation(result)

        img = Image.fromarray(result, mode='L')
        img.save('Resources/morph-gray-opening.png')
        print('opening done')

    #Ex8.4
    def closing(self):
        print('closing start')
        image = self.decoder.getPixels()

        result = self._dilationOperation(image)
        result = self._erosionOperation(result)

        img = Image.fromarray(result, mode='L')
        img.save('Resources/morph-gray-closing.png')
        print('closing done')
    
    def _dilationOperation(self, image):
        height, width = self.decoder.height, self.decoder.width
        result = numpy.zeros((height, width), numpy.uint8)

        return result

    def _erosionOperation(self, image, structuralElement, elementCenterIndices):
        image32 = image.copy().astype('int32')
        height, width = self.decoder.height, self.decoder.width
        result32 = numpy.zeros((height, width), numpy.int32)
        structuralElement32 = structuralElement.astype(numpy.int32)

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
        result8 = numpy.clip(result32, 0, 255).astype('uint8')
        return result8
