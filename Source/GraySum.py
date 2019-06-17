import numpy
import collections
import math
import numpy as np
from PIL import Image, ImageMath, ImageChops, ImageOps
from DjVuImageDecoder import DjVuImageDecoder

class GraySum(object):
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
        self.add_constant(20)
        self.add_img_to_img()
        self.multiply_img_by_constant(2)
        self.multiply_img_by_img()
        self.image_pow(2)
        self.image_divide_constant(2)
        self.image_divide_by_image()
        self.sqrt_img()
        self.image_log()
    
    # Ex 2.1
    def add_constant(self, constant):
        print("Add constant start")
        im1 = self.firstDecoder.getPixels()
        im1 = Image.fromarray(im1)

        im2 = self.secondDecoder.getPixels()
        im2 = Image.fromarray(im2)
        width, height = self.firstDecoder.width, self.firstDecoder.height
        
        const_array = np.full((height, width), constant, dtype=np.uint8)
        const_img = Image.fromarray(const_array)

        ImageChops.add(im1, const_img).save('Resources/const1.png')
 
    
    def add_img_to_img(self):
        print('Add image to image start')
        im1 = self.firstDecoder.getPixels()
        im1 = Image.fromarray(im1, mode='L')

        im2 = self.secondDecoder.getPixels()
        im2 = Image.fromarray(im2, mode='L')

        ImageChops.add(im1, im2).save('Resources/add_img_to_img.png')
    
    # Ex 2.2
    def multiply_img_by_constant(self, constant):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        pixelsBuffer = self.firstDecoder.getPixels()
        
        firstImg = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)

        for h in range(0, height):
            for w in range(0, width):
                firstImg[h, w] = pixelsBuffer[h, w] * constant 
        
        img = Image.fromarray(firstImg, mode='L')
        img.save('Resources/mul_const.png')

    def multiply_img_by_img(self):
        im1 = self.firstDecoder.getPixels()
        im1 = Image.fromarray(im1, mode='L')

        im2 = self.secondDecoder.getPixels()
        im2 = Image.fromarray(im2, mode='L')

        ImageChops.multiply(im1, im2).save('Resources/mul_im_by_im.png')
    
    # Ex 2.4
    def image_pow(self, alfa):
        im1 = self.firstDecoder.getPixels()
        im1 = Image.fromarray(im1, mode='L')

        im2 = self.secondDecoder.getPixels()
        im2 = Image.fromarray(im2, mode='L')

        out = ImageMath.eval("pow(a, alfa)", a=im1, alfa=alfa)
        out2 = ImageMath.eval("pow(a, alfa)", a=im2, alfa=alfa)

        out.save("Resources/pow1.png")
        out2.save("Resources/pow2.png")

    # Ex 2.5
    def image_divide_constant(self, constant):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        pixelsBuffer = self.firstDecoder.getPixels()
        
        firstImg = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)

        for h in range(0, height):
            for w in range(0, width):
                firstImg[h, w] = pixelsBuffer[h, w] / constant
        
        img = Image.fromarray(firstImg, mode='L')
        img.save('Resources/div_const.png')
    
    def image_divide_by_image(self):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        pixelsBuffer = self.firstDecoder.getPixels()
        pixelsBuffer2 = self.secondDecoder.getPixels()
        
        firstImg = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)

        for h in range(0, height):
            for w in range(0, width):
                firstImg[h, w] = int(pixelsBuffer[h, w] / pixelsBuffer2[h, w]) * 255
        
        img = Image.fromarray(firstImg, mode='L')
        img.save('Resources/div_img_by_img.png')
    
    # Ex 2.6
    def sqrt_img(self):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        pixelsBuffer = self.firstDecoder.getPixels()
        
        firstImg = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)

        alfa = 1 # Zamiana stopnia pierwiastka na ulamek
        f_img_max = 0
        f_img_min = 0

        for h in range(height):
            for w in range(width):  
                
                L = int(pixelsBuffer[h][w])

                # Poszukiwanie maksimum
                if f_img_max < L:
                    f_img_max = L

        for h in range(height):
            for w in range(width):  
                
                L = int(pixelsBuffer[h][w])
                if L == 255:
                    L = 255
                elif L == 0:
                    L = 0
                else:
                    L = math.pow(int(pixelsBuffer[h][w]) / f_img_max, alfa) * 255

                # Zaokroglenie do najblizszej wartosci calkowitej z gory
                # i przypisanie wartosci
                firstImg[h][w] = math.ceil(L)

        img = Image.fromarray(firstImg, mode='L')
        img.save('Resources/sqrt_img.png')

    # Ex 2.7
    def image_log(self):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        pixelsBuffer = self.firstDecoder.getPixels()
        
        firstImg = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)

        img_max = 0

        for h in range(0, height):
            for w in range(0, width):
                if pixelsBuffer[h, w] > img_max:
                    img_max = pixelsBuffer[h, w]
        for h in range(0, height):
            for w in range(0, width):
                firstImg[h, w] = (math.log(1 + pixelsBuffer[h, w]) / math.log(1 + img_max)) * 255
        
        img = Image.fromarray(firstImg, mode='L')
        img.save('Resources/log_img.png')
