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
        print('box blur with size {}x{} done'.format(kernelSize[0], kernelSize[1]))

    # Ex9.1 - Gaussian Blur
    def gaussianBlur(self, kernelSize=16, kernelFactory=256):
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
        print('gaussian blur with size {}x{} done'.format(kernelSize, kernelSize))

    def generateGaussianKernel(self, size=3, sigma=1):
        lim = size//2 + (size % 2)/2
        x = numpy.linspace(-lim, lim, size+1)
        kern1d = numpy.diff(st.norm.cdf(x))
        kern2d = numpy.outer(kern1d, kern1d)
        return kern2d/kern2d.sum()

    # Ex9.2
    def median(self, squareKernelSize=9):
        print('median filter with size {}x{} start'.format(squareKernelSize, squareKernelSize))
        height, width = self.decoder.height, self.decoder.width
        image = self.decoder.getPixels()

        result = numpy.empty((height, width), numpy.uint8)
        kernel = numpy.zeros((squareKernelSize, squareKernelSize), numpy.uint8)

        overlap = int(math.ceil(squareKernelSize/2))
        for y in range(height):
            for x in range(width):
                median = kernel.copy()
                for yOff in range(-overlap, overlap):
                    for xOff in range(-overlap, overlap):
                        ySafe = y if ((y + yOff) > (height - 1) or (y + yOff) < 0) else (y + yOff)
                        xSafe = x if ((x + xOff) > (width - 1) or (x + xOff) < 0) else (x + xOff)
                        median[yOff+overlap][xOff+overlap] = image[ySafe][xSafe]
                result[y, x] = numpy.median(median)

        img = Image.fromarray(result, mode='L')
        img.save('Resources/filter-median{}x{}.png'.format(squareKernelSize, squareKernelSize))
        print('median filter with size {}x{} done'.format(squareKernelSize, squareKernelSize))

    # Ex9.3
    def modalGray(self, squareKernelSize=9):
        print('modal filter with size {}x{} start'.format(squareKernelSize, squareKernelSize))
        height, width = self.decoder.height, self.decoder.width
        image = self.decoder.getPixels()

        result = numpy.empty((height, width), numpy.uint8)

        overlap = int(math.ceil(squareKernelSize/2))
        for y in range(height):
            for x in range(width):
                kernel = numpy.zeros((squareKernelSize, squareKernelSize), numpy.uint8)
                for yOff in range(-overlap, overlap):
                    for xOff in range(-overlap, overlap):
                        ySafe = y if ((y + yOff) > (height - 1) or (y + yOff) < 0) else (y + yOff)
                        xSafe = x if ((x + xOff) > (width - 1) or (x + xOff) < 0) else (x + xOff)
                        kernel[yOff+overlap][xOff+overlap] = image[ySafe][xSafe]
                result[y, x] = self.mostFrequent(kernel, kernel[overlap][overlap])

        img = Image.fromarray(result, mode='L')
        img.save('Resources/filter-modal{}x{}.png'.format(squareKernelSize, squareKernelSize))
        print('modal filter with size {}x{} done'.format(squareKernelSize, squareKernelSize))

    def mostFrequent(self, matrix, defaultValue):
        array1d = numpy.reshape(matrix, matrix.size)
        (values,counts) = numpy.unique(matrix, return_counts=True)
        if self.allEquals(counts):
            return defaultValue
        mostFrequentIndex = numpy.argmax(counts)
        return values[mostFrequentIndex]

    def allEquals(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == rest for rest in iterator)

    # Ex9.4
    def kuwahara(self, squareKernelSize=3):
        print('kuwahara filtering with size {}x{} start'.format(squareKernelSize, squareKernelSize))
        height, width = self.decoder.height, self.decoder.width
        image = self.decoder.getPixels()
        result = numpy.empty((height, width), numpy.uint8)

        commonAxis = int(math.ceil(squareKernelSize/2))
        for y in range(height):
            for x in range(width):
                kernel = numpy.zeros((squareKernelSize, squareKernelSize), numpy.uint8)
                for yOff in range(-commonAxis, commonAxis+1):
                    for xOff in range(-commonAxis, commonAxis+1):
                        ySafe = y if ((y + yOff) > (height - 1) or (y + yOff) < 0) else (y + yOff)
                        xSafe = x if ((x + xOff) > (width - 1) or (x + xOff) < 0) else (x + xOff)
                        kernel[yOff+commonAxis][xOff+commonAxis] = image[ySafe][xSafe]
                result[y, x] = self.findLowestRegionVariance(kernel, commonAxis)

        img = Image.fromarray(result, mode='L')
        img.save('Resources/filter-kuwahara{}x{}.png'.format(squareKernelSize, squareKernelSize))
        print('kuwahara filtering with size {}x{} done'.format(squareKernelSize, squareKernelSize))

    def findLowestRegionVariance(self, kernel, commonAxis):
        length = kernel.shape[0]
        upperLeftRegion = kernel[0:commonAxis+1, 0:commonAxis+1]
        upperRightRegion = kernel[commonAxis:length, 0:commonAxis+1]
        lowerLeftRegion = kernel[0:commonAxis+1, commonAxis:length]
        lowerRightRegion = kernel[commonAxis:length, commonAxis:length]
        variances = [numpy.var(upperLeftRegion), 
                     numpy.var(upperRightRegion), 
                     numpy.var(lowerLeftRegion), 
                     numpy.var(lowerRightRegion)]
        return numpy.min(variances)
