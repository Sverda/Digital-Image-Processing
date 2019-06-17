import numpy
import collections
import math
import numpy as np
from PIL import Image, ImageMath, ImageChops
from DjVuImageDecoder import DjVuImageDecoder

class RGBMAth(object):
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
        self.add_constant(120)
        self.add_img_to_img()
        self.multiply_img_by_constant(2)
        self.multiply_img_by_img()
        self.image_pow(1)
        self.image_divide_constant(2)
        self.image_divide_by_image()
        self.sqrt_img(3)
        self.image_log()
    
    # Ex 3.1
    def add_constant(self, constant):
        print("Add constant start")
        im1 = self.firstDecoder.getPixels24Bits()
        im1 = Image.fromarray(im1)

        im2 = self.secondDecoder.getPixels24Bits()
        im2 = Image.fromarray(im2)
        width, height = self.firstDecoder.width, self.firstDecoder.height
        
        const_array = np.full((self.maxHeight, self.maxWidth, 3), constant, np.uint8)
        const_img = Image.fromarray(const_array)

        ImageChops.add(im1, const_img).save('Resources/const1.png', mode='RGB')
 
    
    def add_img_to_img(self):
        print('Add image to image start')
        im1 = self.firstDecoder.getPixels24Bits()
        im1 = Image.fromarray(im1, mode='RGB')

        im2 = self.secondDecoder.getPixels24Bits()
        im2 = Image.fromarray(im2, mode='RGB')

        ImageChops.add(im1, im2).save('Resources/add_img_to_img.png')
    
    # Ex 3.2
    def multiply_img_by_constant(self, constant):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        pixelsBuffer = self.firstDecoder.getPixels24Bits()
        
        firstImg = numpy.zeros((self.maxHeight, self.maxWidth, 3), numpy.uint8)

        for h in range(0, height):
            for w in range(0, width):
                firstImg[h, w] = pixelsBuffer[h, w] * constant
        
        img = Image.fromarray(firstImg, mode='RGB')
        img.save('Resources/mul_const.png')

    def multiply_img_by_img(self):
        im1 = self.firstDecoder.getPixels24Bits()
        im1 = Image.fromarray(im1, mode='RGB')

        im2 = self.secondDecoder.getPixels24Bits()
        im2 = Image.fromarray(im2, mode='RGB')

        ImageChops.multiply(im1, im2).save('Resources/mul_im_by_im.png')
    
    # Ex 3.4
    def image_pow(self, alfa):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        pixelsBuffer = self.firstDecoder.getPixels24Bits()
        
        firstImg = numpy.zeros((self.maxHeight, self.maxWidth, 3), 0, numpy.uint8)

        for h in range(0, height):
            for w in range(0, width):
                
                R = int(pixelsBuffer[h][w][0])
                G = int(pixelsBuffer[h][w][1])
                B = int(pixelsBuffer[h][w][2])

                if R == 0:
                    R = 0
                else:
                    R = 255 * (math.pow(int(pixelsBuffer[h][w][0]), alfa))

                if G == 0:
                    G = 0
                else:
                    G = 255 * (math.pow(int(pixelsBuffer[h][w][1]), alfa))
                
                if B == 0:
                    B = 0
                else:
                    B = 255 * (math.pow(int(pixelsBuffer[h][w][2]), alfa))

                # Zaokroglenie do najblizszej wartosci calkowitej z gory
                # i przypisanie wartosci
                firstImg[h][w][0] = math.ceil(R)
                firstImg[h][w][1] = math.ceil(G)
                firstImg[h][w][2] = math.ceil(B)

        Image.fromarray(firstImg, mode='RGB').save('Resources/pow1.png')
        

    
