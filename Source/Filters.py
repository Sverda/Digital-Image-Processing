import math
import numpy
import collections
import scipy.stats as st
from PIL import Image
from DjVuImageDecoder import DjVuImageDecoder

class Filters(object):
    def __init__(self, firstPath):
        self.decoder = DjVuImageDecoder(firstPath)

    # Ex9.1 - Box Blur
    def boxBlur(self, kernelSize=(9,9)):
        print('box blur with size {}x{} start'.format(kernelSize[0], kernelSize[1]))
        height, width = self.decoder.height, self.decoder.width
        image = self.decoder.getPixels()

        result = numpy.empty((height, width), numpy.uint8)
        kernel = numpy.ones(kernelSize)

        kernelHeight, kernelWidth = kernel.shape
        overlapHeight, overlapWidth = int(math.ceil(kernelHeight/2)), int(math.ceil(kernelWidth/2))
        for y in range(height):
            for x in range(width):
                average, hitsCount = 0, 0
                for yOff in range(-overlapHeight, overlapHeight):
                    for xOff in range(-overlapWidth, overlapWidth):
                        ySafe = y if ((y + yOff) > (height - 1) or (y + yOff) < 0) else (y + yOff)
                        xSafe = x if ((x + xOff) > (width - 1) or (x + xOff) < 0) else (x + xOff)
                        average += image[ySafe, xSafe] * kernel[yOff + 1, xOff + 1]
                        hitsCount += kernel[yOff + 1, xOff + 1]
                average = int(round(average/hitsCount))
                result[y, x] = average

        img = Image.fromarray(result, mode='L')
        img.save('Resources/filter-boxblur{}x{}.png'.format(kernelSize[0], kernelSize[1]))
        print('box blur with size {}x{} start'.format(kernelSize[0], kernelSize[1]))

    # Ex9.1 - Gaussian Blur
    def gaussianBlur(self, kernelSize=9*2, kernelFactory=546*2):
        print('gaussian blur with size {}x{} start'.format(kernelSize, kernelSize))
        height, width = self.decoder.height, self.decoder.width
        image = self.decoder.getPixels()

        result = numpy.empty((height, width), numpy.uint8)
        kernel = (self.generateGaussianKernel(kernelSize, 1)*kernelFactory).astype(numpy.int32)

        overlap = int(math.ceil(kernelSize/2))
        for y in range(height):
            for x in range(width):
                average, kernelHitsValue = 0, 0
                for yOff in range(-overlap, overlap):
                    for xOff in range(-overlap, overlap):
                        ySafe = y if ((y + yOff) > (height - 1) or (y + yOff) < 0) else (y + yOff)
                        xSafe = x if ((x + xOff) > (width - 1) or (x + xOff) < 0) else (x + xOff)
                        average += image[ySafe, xSafe] * kernel[yOff + 1, xOff + 1]
                        kernelHitsValue += kernel[yOff + 1, xOff + 1]
                average = int(round(average/kernelHitsValue))
                result[y, x] = average

        img = Image.fromarray(result, mode='L')
        img.save('Resources/filter-gaussianblur{}x{}f{}.png'.format(kernelSize, kernelSize, kernelFactory))
        print('gaussian blur with size {}x{} start'.format(kernelSize, kernelSize))

    def generateGaussianKernel(self, size=3, sigma=1):
        lim = size//2 + (size % 2)/2
        x = numpy.linspace(-lim, lim, size+1)
        kern1d = numpy.diff(st.norm.cdf(x))
        kern2d = numpy.outer(kern1d, kern1d)
        return kern2d/kern2d.sum()