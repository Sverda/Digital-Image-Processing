import numpy
from PIL import Image
from DjVuImageDecoder import DjVuImageDecoder

class Unification(object):
    def __init__(self, firstPath, secondPath):
        self.firstDecoder = DjVuImageDecoder(firstPath)
        self.secondDecoder = DjVuImageDecoder(secondPath)

    def geometricGray(self):
        max_width = max([self.firstDecoder.width, self.secondDecoder.width])
        max_height = max([self.firstDecoder.height, self.secondDecoder.height])
        print('max size: ' + str(max_width) + 'x' + str(max_height))
        
        width, height = self.firstDecoder.width, self.firstDecoder.height
        if width < max_width or height < max_height:
            # Create black background
            firstResult = numpy.zeros((max_height, max_width), numpy.uint8)
            # Copy smaller image to bigger
            startWidthIndex = int(round((max_width - width) / 2))
            startHeightIndex = int(round((max_height - height) / 2))
            pixelsBuffer = self.firstDecoder.getPixels()
            for h in range (0, height):
                for w in range (0, width):
                    firstResult[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
            img = Image.fromarray(firstResult, mode='L')
            img.save('Resources/output_1.png')
            print('first image done')
        
        width, height = self.secondDecoder.width, self.secondDecoder.height
        if width < max_width or height < max_height:
            # Create black background
            secondResult = numpy.zeros((max_height, max_width), numpy.uint8)
            # Copy smaller image to bigger
            startWidthIndex = int(round((max_width - width) / 2))
            startHeightIndex = int(round((max_height - height) / 2))
            pixelsBuffer = self.secondDecoder.getPixels()
            for h in range (0, height):
                for w in range (0, width):
                    secondResult[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
            img = Image.fromarray(secondResult, mode='L')
            img.save('Resources/output_2.png')
            print('second image done')
        print('unification done')