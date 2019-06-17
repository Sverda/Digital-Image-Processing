import matplotlib.pyplot as plt
from DjVuImageDecoder import DjVuImageDecoder
import numpy as np
from PIL import Image

class HistogramRGB(object):
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
        self.distend_histogram()
        # self.local_threshold()
        # self.global_threshold()
    
    # Ex 5.1
    def calc(self, image = False):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        
        if image is False:
            image = self.firstDecoder.getPixels24Bits()

        histogram = [0] * 3              # histogram RGB
        histogram[0] = [0] * 256         # histogram R
        histogram[1] = [0] * 256         # histogram G
        histogram[2] = [0] * 256         # histogram B

        for h in range(height):
            for w in range(width):
                bin = image[h, w]
                for k in range(3):
                    histogram[k][bin[k]] += 1

        fig = plt.figure()
        plt.subplot(2, 2, 1)
        plt.bar(np.arange(256) - 0.33, histogram[0], color="red", width=0.33)
        plt.title("red")
        plt.ylabel("number of accurences")

        plt.subplot(2, 2, 2)
        plt.bar(np.arange(256), histogram[1], color="green", width=0.33)
        plt.title("green")

        plt.subplot(2, 2, 3)
        plt.bar(np.arange(256) + 0.33, histogram[2], color="blue", width=0.33)
        plt.xlabel("blue")
        plt.ylabel("number of accurences")

        plt.subplot(2, 2, 4)
        plt.bar(np.arange(256)- 0.33, histogram[0], color="red", width=0.33)
        plt.bar(np.arange(256), histogram[1], color="green", width=0.33)
        plt.bar(np.arange(256) + 0.33, histogram[2], color="blue", width=0.33)
        plt.xlabel("RGB")
        plt.show()
    
    # Ex 5.2
    def move_histogram(self, const = 0):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels24Bits()

        result = np.empty((height, width, 3), dtype=np.uint8)

        for h in range(height):
            for w in range(width):
                value = image[h, w]
                for current in range(len(value)):
                    v = value[current]
                    v += const
                    if v < 0:
                        v = 0
                    elif v > 255:
                        v = 255
                    value[current] = v
                result[h, w] = value

        self.calc(image=result)
        Image.fromarray(result, mode='RGB').save('Resources/move_hist_RGB.png')
    
    # Ex 5.3
    def distend_histogram(self):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels24Bits()

        result = np.empty((height, width, 3), dtype=np.uint8)

        for h in range(height):
            for w in range(width):
                result[h, w] = image[h, w]

        max_value = [0] * 3
        min_value = [255] * 3 

        while (max_value != 255) and (max_value[1] != 255) and (max_value[2] != 255):
            for h in range(height):
                for w in range(width):
                    current = result[h, w]
                    for k in range(3):
                        max_value[k] = max(max_value[k], current[k])
                        min_value[k] = min(min_value[k], current[k])

            for h in range(height):
                for w in range(width):
                    current = result[h, w]
                    for k in range(3):
                        current[k] = ((255 / (max_value[k] - min_value[k])) * (current[k] - min_value[k]))
                    result[h, w] = current

        self.calc(image=result)
        Image.fromarray(result, mode='RGB').save('Resources/dist_hist_RGB.png')
    
    # # Ex 5.4
    # def local_threshold(self, dim=3):
    #     width, height = self.firstDecoder.width, self.firstDecoder.height
    #     image = self.firstDecoder.getPixels()

    #     result = np.empty((height, width), dtype=np.uint8)
        
    #     l, r = -(int(round(dim / 2))), int(round(dim / 2) + 1)

        
    #     for h in range(height):
    #         for w in range(width):
    #             n = 0
    #             threshold = 0
    #             currPix = image[h, w]
    #             for i in range(l, r):
    #                 for j in range(l, r):
    #                     i_result = h if ((h + i) > (height + l)) else (h + i)
    #                     j_result = w if ((w + j) > (width + l)) else (w + j)
    #                     threshold += image[i_result, j_result]
    #                     n += 1
    #             threshold = int(round(threshold / n))
    #             result[h, w] = 0 if (currPix < threshold) else 255

    #     self.calc(image=result)
    #     Image.fromarray(result, mode='L').save('Resources/local_thr.png')
    
    #  # Ex 5.5
    # def global_threshold(self):
    #     width, height = self.firstDecoder.width, self.firstDecoder.height
    #     image = self.firstDecoder.getPixels()

    #     result = np.empty((height, width), dtype=np.uint8)

        
    #     threshold, n = 0, 0

    #     for h in range(height):
    #         for w in range(width):
    #             threshold += image[h, w]
    #             n += 1
    #     threshold = int(round(threshold / n))

        
    #     for h in range(height):
    #         for w in range(width):
    #             result[h, w] = 0 if (image[h, w] < threshold) else 255

    #     self.calc(image=result)
    #     Image.fromarray(result, mode='L').save('Resources/global_thr.png')
