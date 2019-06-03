import numpy
import collections
from PIL import Image
from DjVuImageDecoder import DjVuImageDecoder

class Unification(object):
    def __init__(self, firstPath, secondPath):
        self.firstDecoder = DjVuImageDecoder(firstPath)
        self.secondDecoder = DjVuImageDecoder(secondPath)
        self.maxHeight, self.maxWidth = self._findMaxSize()
        
    def _findMaxSize(self):
        self.maxHeight = max([self.firstDecoder.height, self.secondDecoder.height])
        self.maxWidth = max([self.firstDecoder.width, self.secondDecoder.width])
        print('max size: ' + str(self.maxWidth) + 'x' + str(self.maxHeight))
        return self.maxHeight, self.maxWidth

    # Ex1.1
    def geometricGray(self):
        print('geometric gray unificaiton start')
        width, height = self.firstDecoder.width, self.firstDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            # Create black background
            firstResult = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)
            # Copy smaller image to bigger
            startWidthIndex = int(round((self.maxWidth - width) / 2))
            startHeightIndex = int(round((self.maxHeight - height) / 2))
            pixelsBuffer = self.firstDecoder.getPixels()
            for h in range (0, height):
                for w in range (0, width):
                    firstResult[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
            img = Image.fromarray(firstResult, mode='L')
            img.save('Resources/ggUnification_1.png')
            print('first image done')
        
        width, height = self.secondDecoder.width, self.secondDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            # Create black background
            secondResult = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)
            # Copy smaller image to bigger
            startWidthIndex = int(round((self.maxWidth - width) / 2))
            startHeightIndex = int(round((self.maxHeight - height) / 2))
            pixelsBuffer = self.secondDecoder.getPixels()
            for h in range (0, height):
                for w in range (0, width):
                    secondResult[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
            img = Image.fromarray(secondResult, mode='L')
            img.save('Resources/ggUnification_2.png')
            print('second image done')
        print('geometric gray unification done')

    # Ex1.2
    def rasterGray(self):
        print('raster gray unification start')
        self._scaleUp(self.firstDecoder, 'Resources/rgUnification_1.png')
        print('first image done')
        self._scaleUp(self.secondDecoder, 'Resources/rgUnification_2.png')
        print('second image done')
        print('raster gray unification done')
        
    def _scaleUp(self, decoder, outputPath):
        width, height = decoder.width, decoder.height
        scaleFactoryW = float(self.maxWidth) / width
        scaleFactoryH = float(self.maxHeight) / height
        if width < self.maxWidth or height < self.maxHeight:
            pixelsBuffer = decoder.getPixels()
            result = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)
            # Fill values
            for h in range(height):
                for w in range(width):
                    if w%2 == 0:
                        result[int(scaleFactoryH * h), int(round(scaleFactoryW * w)) + 1] = pixelsBuffer[h, w]
                    if w%2 == 1:
                        result[int(round(scaleFactoryH * h)) + 1, int(scaleFactoryW * w)] = pixelsBuffer[h, w]
            # Interpolate
            self._interpolate(result)
            img = Image.fromarray(result, mode='L')
            img.save(outputPath)

    def _interpolate(self, result):
        for h in range(self.maxHeight):
            for w in range(self.maxWidth):
                value = 0
                count = 0
                if result[h, w] == 0:
                    for iOff in range(-1, 2):
                        for jOff in range(-1, 2):
                            iSafe = h if ((h + iOff) > (self.maxHeight - 2)) | ((h + iOff) < 0) else (h + iOff)
                            jSafe = w if ((w + jOff) > (self.maxWidth - 2)) | ((w + jOff) < 0) else (w + jOff)
                            if result[iSafe, jSafe] != 0:
                                value += result[iSafe, jSafe]
                                count += 1
                    result[h, w] = value / count

    # Ex1.3
    def geometricColor(self):
        print('geometric color unificaiton start')
        self.firstDecoder.setColor()
        width, height = self.firstDecoder.width, self.firstDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            result = self._paintInMiddleColor(firstDecoder)
            img = Image.fromarray(secondResult, 'RGB')
            img.save('Resources/gcUnification_1.png')
            print('first image done')

        self.secondDecoder.setColor()
        width, height = self.secondDecoder.width, self.secondDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            secondResult = self._paintInMiddleColor(secondDecoder)
            img = Image.fromarray(secondResult, 'RGB')
            img.save('Resources/gcUnification_2.png')
            print('second image done')
        print('geometric color unification done')

    def _paintInMiddleColor(self, decoder):
        # Create black background
        result = numpy.full((self.maxHeight, self.maxWidth, 3), 0, numpy.uint8)
        # Copy smaller image to bigger
        width, height = decoder.width, decoder.height
        startWidthIndex = int(round((self.maxWidth - width) / 2))
        startHeightIndex = int(round((self.maxHeight - height) / 2))
        pixelsBuffer = decoder.getPixels24Bits()
        for h in range (0, height):
            for w in range (0, width):
                result[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
        return result