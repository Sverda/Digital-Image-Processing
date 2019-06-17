import matplotlib.pyplot as plt
from DjVuImageDecoder import DjVuImageDecoder
import numpy as np
from PIL import Image

class Histogram(object):
    def __init__(self, firstPath, secondPath):
        self.firstDecoder = DjVuImageDecoder(firstPath)
        self.secondDecoder = DjVuImageDecoder(secondPath)
        self.maxHeight, self.maxWidth = self._findMaxSize()

    def _findMaxSize(self):
        self.maxHeight = max([self.firstDecoder.height, self.secondDecoder.height])
        self.maxWidth = max([self.firstDecoder.width, self.secondDecoder.width])
        print('max size: ' + str(self.maxWidth) + 'x' + str(self.maxHeight))
        return self.maxHeight, self.maxWidth
    
    def run_all(self):
        # self.calc()
        # self.move_histogram(60)
        # self.distend_histogram()
        # self.local_threshold()
        self.global_threshold()
    
    # Ex 5.1
    def calc(self, image = False):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        if image is False:
            image = self.firstDecoder.getPixels()
        histogram = [0] * 256

        for h in range(height):
            for w in range(width):
                gray_arr = image[h, w]
                histogram[gray_arr] += 1

        plt.bar(np.arange(256), histogram, color="gray", width=0.8)
        plt.show()
    
    # Ex 5.2
    def move_histogram(self, const = 0):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels()

        result = np.empty((height, width), dtype=np.uint8)

        # przemieszczanie
        for h in range(height):
            for w in range(width):
                value = int(image[h, w]) + const
                if value < 0:
                    value = 0
                elif value > 255:
                    value = 255
                result[h, w] = value

        self.calc(image=result)
        Image.fromarray(result, mode='L').save('Resources/move_hist.png')
    
    # Ex 5.3
    def distend_histogram(self):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels()

        result = np.empty((height, width), dtype=np.uint8)

        for h in range(height):
            for w in range(width):
                result[h, w] = image[h, w]

        max_value = 0
        min_value = 255

        while max_value != 255:
            for h in range(height):
                for w in range(width):
                    pixel_val = result[h, w]
                    max_value = max(max_value, pixel_val)
                    min_value = min(min_value, pixel_val)

            for h in range(height):
                for w in range(width):
                    pixel = result[h, w]
                    result[h, w] = ((255 / (max_value - min_value)) * (pixel - min_value))

        self.calc(image=result)
        Image.fromarray(result, mode='L').save('Resources/dist_hist.png')
    
    # Ex 5.4
    def local_threshold(self, dim=3):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels()

        result = np.empty((height, width), dtype=np.uint8)
        
        l, r = -(int(round(dim / 2))), int(round(dim / 2) + 1)

        
        for h in range(height):
            for w in range(width):
                n = 0
                threshold = 0
                currPix = image[h, w]
                for i in range(l, r):
                    for j in range(l, r):
                        i_result = h if ((h + i) > (height + l)) else (h + i)
                        j_result = w if ((w + j) > (width + l)) else (w + j)
                        threshold += image[i_result, j_result]
                        n += 1
                threshold = int(round(threshold / n))
                result[h, w] = 0 if (currPix < threshold) else 255

        self.calc(image=result)
        Image.fromarray(result, mode='L').save('Resources/local_thr.png')
    
     # Ex 5.5
    def global_threshold(self):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels()

        result = np.empty((height, width), dtype=np.uint8)

        
        threshold, n = 0, 0

        for h in range(height):
            for w in range(width):
                threshold += image[h, w]
                n += 1
        threshold = int(round(threshold / n))

        
        for h in range(height):
            for w in range(width):
                result[h, w] = 0 if (image[h, w] < threshold) else 255

        self.calc(image=result)
        Image.fromarray(result, mode='L').save('Resources/global_thr.png')
