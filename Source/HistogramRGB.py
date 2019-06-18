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
        # self.distend_histogram()
        # self.single_threshold()
        # self.multi_threshold()
        self.local_threshold(21)
        # self.global_threshold()

    # Ex 6.1
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
    
    # Ex 6.2
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
    
    # Ex 6.3
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
    
    # Ex 6.4
    def single_threshold(self):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels24Bits()

        result = np.empty((height, width, 3), dtype=np.uint8)

        R, G, B = 0, 0, 0

        newR, newG, newB = 0, 0, 0

        for h in range(height):
            for w in range(width):
                R += image[h, w][0]
                newR += 1
                G += image[h, w][1]
                newG += 1
                B += image[h, w][2]
                newB += 1
        R = int(round(R / newR))
        G = int(round(G / newG))
        B = int(round(B / newB))

        for h in range(height):
            for w in range(width):
                result[h, w] = (0 if (image[h, w][0] < R) else 255, 0 if (image[h, w][1] < G) else 255, 0 if (image[h, w][2] < B) else 255)


        self.calc(image=result)
        Image.fromarray(result, mode='RGB').save('Resources/single_thr_RGB.png')
    
     # Ex 6.5
    def multi_threshold(self, bins=3):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels24Bits()

        result = np.empty((height, width, 3), dtype=np.uint8)

        max_value = [0] * 3
        min_value = [255] * 3

        for h in range(height):
            for w in range(width):
                current = image[h, w]
                for k in range(3):
                    max_value[k] = max(max_value[k], current[k])
                    min_value[k] = min(min_value[k], current[k])

        scale = [0] * 3
        for k in range(3):
            scale[k] = max_value[k] / (bins - 1)

        for h in range(height):
            for w in range(width):
                pixel = image[h, w]
                for k in range(3):
                    pixel[k] = int(round(pixel[k] / scale[k])) * scale[k]
                result[h, w] = pixel

        self.calc(image=result)
        Image.fromarray(result, mode='RGB').save('Resources/multi_thr_RGB.png')
    
    # Ex 6.6
    def local_threshold(self, dim=3):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels24Bits()

        result = np.empty((height, width, 3), dtype=np.uint8)
        low, up = -(int(dim / 2)), (int(dim / 2) + 1)

        for h in range(height):
            for w in range(width):
                n = 0
                r, g, b = 0, 0, 0
                current = image[h, w]
                for i in range(low, up):
                    for j in range(low, up):
                        i_result = h if ((h + i) > (height + low)) | ((h + i) < 0) else (h + i)
                        j_result = w if ((w + j) > (width + low)) | ((w + j) < 0) else (w + j)
                        r += int(image[i_result, j_result][0])
                        g += int(image[i_result, j_result][1])
                        b += int(image[i_result, j_result][2])
                        n += 1
                r = int(round(r / n))
                g = int(round(g / n))
                b = int(round(b / n))
                result[h, w] = (0 if (current[0] < r) else 255, 0 if (current[1] < g) else 255, 0 if (current[2] < b) else 255)
        
        self.calc(image=result)
        Image.fromarray(result, mode='RGB').save('Resources/local_thr_RGB.png')
    
    # Ex 6.7
    def global_threshold(self, dim=3, bins=4):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels24Bits()

        result = np.empty((height, width, 3), dtype=np.uint8)
        low, up = -(int(dim / 2)), (int(dim / 2) + 1)

        for h in range(height):
            for w in range(width):
                n, r, g, b = 0, 0, 0, 0
                current = image[h, w]
                max_value = [0] * 3
                min_value = [255] * 3
                for i in range(low, up):
                    for j in range(low, up):
                        i_result = h if ((h + i) > (height + low)) | ((h + i) < 0) else (h + i)
                        j_result = w if ((w + j) > (width + low)) | ((w + j) < 0) else (w + j)
                        current = image[i_result, j_result]
                        for k in range(3):
                            max_value[k] = max(max_value[k], current[k])
                            min_value[k] = min(min_value[k], current[k])
                scale = [0] * 3
                for k in range(3):
                    scale[k] = max_value[k] / (bins - 1)
                    if scale[k] == 0:
                        scale[k] = 1
                for k in range(3):
                    v = int(round(current[k] / scale[k])) * scale[k]
                    current[k] = v
                result[h, w] = current
        
        self.calc(image=result)
        Image.fromarray(result, mode='RGB').save('Resources/global_thr_RGB.png')
    
    
