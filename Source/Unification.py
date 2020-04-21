import numpy
import collections
from PIL import Image
from ImageDecoder import ImageDecoder

class Unification(object):
    def __init__(self, firstPath, secondPath, imageType):
        self.firstDecoder = ImageDecoder(firstPath, imageType)
        self.secondDecoder = ImageDecoder(secondPath, imageType)
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
            pixelsBuffer = self.firstDecoder.getGreyMatrix()
            for h in range (0, height):
                for w in range (0, width):
                    firstResult[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
            img = Image.fromarray(firstResult, mode='L')
            img.save('Resources/result/ggUnification_1.png')
            print(' first image done')
        
        width, height = self.secondDecoder.width, self.secondDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            # Create black background
            secondResult = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)
            # Copy smaller image to bigger
            startWidthIndex = int(round((self.maxWidth - width) / 2))
            startHeightIndex = int(round((self.maxHeight - height) / 2))
            pixelsBuffer = self.secondDecoder.getGreyMatrix()
            for h in range (0, height):
                for w in range (0, width):
                    secondResult[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
            img = Image.fromarray(secondResult, mode='L')
            img.save('Resources/result/ggUnification_2.png')
            print(' second image done')
        print('geometric gray unification done')

    # Ex1.2
    def rasterGray(self):
        print('raster gray unification start')
        self._scaleUpGray(self.firstDecoder, 'Resources/result/rgUnification_1.png')
        print(' first image done')
        self._scaleUpGray(self.secondDecoder, 'Resources/result/rgUnification_2.png')
        print(' second image done')
        print('raster gray unification done')
        
    def _scaleUpGray(self, decoder, outputPath):
        width, height = decoder.width, decoder.height
        scaleFactoryW = float(self.maxWidth) / width
        scaleFactoryH = float(self.maxHeight) / height
        if width < self.maxWidth or height < self.maxHeight:
            pixelsBuffer = decoder.getGreyMatrix()
            result = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)
            # Fill values
            for h in range(height):
                for w in range(width):
                    if w%2 == 0:
                        result[int(scaleFactoryH * h), int(round(scaleFactoryW * w)) + 1] = pixelsBuffer[h, w]
                    if w%2 == 1:
                        result[int(round(scaleFactoryH * h)) + 1, int(scaleFactoryW * w)] = pixelsBuffer[h, w]
            # Interpolate
            self._interpolateGray(result)
            img = Image.fromarray(result, mode='L')
            img.save(outputPath)
    
    def _interpolateGray(self, result):
        for h in range(self.maxHeight):
            for w in range(self.maxWidth):
                value = 0
                count = 0
                if result[h, w] == 0:
                    for hOff in range(-1, 2):
                        for wOff in range(-1, 2):
                            hSafe = h if ((h + hOff) > (self.maxHeight - 2)) | ((h + hOff) < 0) else (h + hOff)
                            wSafe = w if ((w + wOff) > (self.maxWidth - 2)) | ((w + wOff) < 0) else (w + wOff)
                            if result[hSafe, wSafe] != 0:
                                value += result[hSafe, wSafe]
                                count += 1
                    result[h, w] = value / count

    # Ex1.3
    def geometricColor(self):
        print('geometric color unificaiton start')
        width, height = self.firstDecoder.width, self.firstDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            result = self._paintInMiddleColor(self.firstDecoder)
            img = Image.fromarray(result, 'RGB')
            img.save('Resources/result/gcUnification_1.png')
            print(' first image done')

        width, height = self.secondDecoder.width, self.secondDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            result = self._paintInMiddleColor(self.secondDecoder)
            img = Image.fromarray(result, 'RGB')
            img.save('Resources/result/gcUnification_2.png')
            print(' second image done')
        print('geometric color unification done')

    def _paintInMiddleColor(self, decoder):
        # Create black background
        result = numpy.full((self.maxHeight, self.maxWidth, 3), 0, numpy.uint8)
        # Copy smaller image to bigger
        width, height = decoder.width, decoder.height
        startWidthIndex = int(round((self.maxWidth - width) / 2))
        startHeightIndex = int(round((self.maxHeight - height) / 2))
        pixelsBuffer = decoder.getRGBMatrix()
        for h in range (0, height):
            for w in range (0, width):
                result[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
        return result

    # Ex1.4
    def rasterColor(self):
        print('rastar color unification start')
        self._scaleUpColor(self.firstDecoder, 'Resources/result/rcUnification_1.png')
        print(' first image done')
        self._scaleUpColor(self.secondDecoder, 'Resources/result/rcUnification_2.png')
        print(' second image done')
        print('rastar color unification done')

    def _scaleUpColor(self, decoder, outputPath):
        width, height = decoder.width, decoder.height
        scaleFactoryW = float(self.maxWidth) / width
        scaleFactoryH = float(self.maxHeight) / height
        if width < self.maxWidth or height < self.maxHeight:
            pixelsBuffer = decoder.getRGBMatrix()
            result = numpy.full((self.maxHeight, self.maxWidth, 3), 1, numpy.uint8)
            # Fill values
            for h in range(height):
                for w in range(width):
                    if w%2 == 0:
                        result[int(scaleFactoryH * h), int(round(scaleFactoryW * w)) + 1] = pixelsBuffer[h, w]
                    if w%2 == 1:
                        result[int(round(scaleFactoryH * h)) + 1, int(scaleFactoryW * w)] = pixelsBuffer[h, w]
            # Interpolate
            self._interpolateColor(result)
            img = Image.fromarray(result, mode='RGB')
            img.save(outputPath)

    def _interpolateColor(self, result):
        for h in range(self.maxHeight):
            for w in range(self.maxWidth):
                r, g, b = 0, 0, 0
                n = 0
                if (result[h, w][0] == 1) & (result[h, w][1] == 1) & (result[h, w][2] == 1):
                    for hOff in range(-1, 2):
                        for wOff in range(-1, 2):
                            hSafe = h if ((h + hOff) > (self.maxHeight - 2)) | ((h + hOff) < 0) else (h + hOff)
                            wSafe = w if ((w + wOff) > (self.maxWidth - 2)) | ((w + wOff) < 0) else (w + wOff)
                            if (result[hSafe, wSafe][0] > 1) | (result[hSafe, wSafe][1] > 1) | (result[hSafe, wSafe][2] > 1):
                                r += result[hSafe, wSafe][0]
                                g += result[hSafe, wSafe][1]
                                b += result[hSafe, wSafe][2]
                                n += 1
                    result[h, w] = (r/n, g/n, b/n)