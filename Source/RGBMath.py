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
        # self.add_constant(120)
        # self.add_img_to_img()
        # self.multiply_img_by_constant(2)
        # self.multiply_img_by_img()
        # self.image_pow(1)
        # self.image_divide_constant(2)
        # self.image_divide_by_image()
        # self.sqrt_img(3)
        # self.image_log()
        # self.image_pow()
        # self.image_divide_constant(150)
        # self.image_divide_image()
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
        
        firstImg = numpy.zeros((self.maxHeight, self.maxWidth, 3), np.uint8)

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
    def image_pow(self, alfa = 1):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        pixelsBuffer = self.firstDecoder.getPixels24Bits()
        
        firstImg = numpy.zeros((self.maxHeight, self.maxWidth, 3), np.uint8)

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

                firstImg[h][w][0] = math.ceil(R)
                firstImg[h][w][1] = math.ceil(G)
                firstImg[h][w][2] = math.ceil(B)

        Image.fromarray(firstImg, mode='RGB').save('Resources/pow1.png')
    
    # Ex 3.5
    def image_divide_constant(self, const = 0):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels24Bits()
        
        result = np.empty((height, width, 3), dtype=np.uint8)

        f_min = 255
        f_max = 0
        Q = 0
        
        for h in range(height):
            for w in range(width):  

                R_S = int(image[h][w][0]) + int(const)
                G_S = int(image[h][w][1]) + int(const)
                B_S = int(image[h][w][2]) + int(const)

                # Poszukiwanie maksimum
                if Q < max([R_S, G_S, B_S]):
                    Q = max([R_S, G_S, B_S])

        for h in range(height):
            for w in range(width):  

                # Obliczanie sum
                R_S = int(image[h][w][0]) + int(const)
                G_S = int(image[h][w][1]) + int(const)
                B_S = int(image[h][w][2]) + int(const)

                Q_R = (R_S * 255)/Q
                Q_G = (G_S * 255)/Q
                Q_B = (B_S * 255)/Q
                    
                # Zaokroglenie do najblizszej wartosci calkowitej z gory
                # i przypisanie wartosci
                result[h][w][0] = math.ceil(Q_R)
                result[h][w][1] = math.ceil(Q_G)
                result[h][w][2] = math.ceil(Q_B)

                # Poszukiwanie minimum i maksimum                
                if f_min > min([Q_R, Q_G, Q_B]):
                    f_min = min([Q_R, Q_G, Q_B])
                if f_max < max([Q_R, Q_G, Q_B]):
                    f_max = max([Q_R, Q_G, Q_B])

        Image.fromarray(result, mode='RGB').save('Resources/div_const_rgb.png')

    # Ex 3.5
    def image_divide_image(self):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels24Bits()
        image2 = self.secondDecoder.getPixels24Bits()
        result = np.empty((height, width, 3), dtype=np.uint8)

        f_min = 255
        f_max = 0
        Q = 0
        
        for h in range(height):
            for w in range(width):  

                R_S = int(image[h][w][0]) + int(image2[h][w][0])
                G_S = int(image[h][w][1]) + int(image2[h][w][1])
                B_S = int(image[h][w][2]) + int(image2[h][w][2])

                # Poszukiwanie maksimum
                if Q < max([R_S, G_S, B_S]):
                    Q = max([R_S, G_S, B_S])

        for h in range(height):
            for w in range(width):  

                R_S = int(image[h][w][0]) + int(image2[h][w][0])
                G_S = int(image[h][w][1]) + int(image2[h][w][1])
                B_S = int(image[h][w][2]) + int(image2[h][w][2])

                Q_R = (R_S * 255)/Q
                Q_G = (G_S * 255)/Q
                Q_B = (B_S * 255)/Q
                    
                result[h][w][0] = math.ceil(Q_R)
                result[h][w][1] = math.ceil(Q_G)
                result[h][w][2] = math.ceil(Q_B)

                # Poszukiwanie minimum i maksimum                
                if f_min > min([Q_R, Q_G, Q_B]):
                    f_min = min([Q_R, Q_G, Q_B])
                if f_max < max([Q_R, Q_G, Q_B]):
                    f_max = max([Q_R, Q_G, Q_B])

        Image.fromarray(result, mode='RGB').save('Resources/div_img_by_img_rgb.png')        
    
    def image_sqrt(self, deg=1):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels24Bits()
        result = np.empty((height, width, 3), dtype=np.uint8)

        # Inicjalizacja zmiennych
        f_min = 255
        f_max = 0
        f_img_max = 0

        alfa = 1 / deg # Zamiana stopnia pierwiastka na ulamek

        for h in range(height):
            for w in range(width):  

                R = int(image[h][w][0])
                G = int(image[h][w][1])
                B = int(image[h][w][2])

                if f_img_max < max([R, G, B]):
                    f_img_max = max([R, G, B])

        for h in range(height):
            for w in range(width):  

                R = int(image[h][w][0])
                G = int(image[h][w][1])
                B = int(image[h][w][2])

                if R == 0:
                    R = 0
                else:
                    R = 255 * (math.pow(int(image[h][w][0]) / f_img_max, alfa))

                if G == 0:
                    G = 0
                else:
                    G = 255 * (math.pow(int(image[h][w][1]) / f_img_max, alfa))
                
                if B == 0:
                    B = 0
                else:
                    B = 255 * (math.pow(int(image[h][w][2]) / f_img_max, alfa))

                result[h][w][0] = math.ceil(R)
                result[h][w][1] = math.ceil(G)
                result[h][w][2] = math.ceil(B)

                # Poszukiwanie minimum i maksimum                
                if f_min > min([R, G, B]):
                    f_min = min([R, G, B])
                if f_max < max([R, G, B]):
                    f_max = max([R, G, B])

        # norm_result = np.empty((height, width, 3), dtype=np.uint8)
        # for h in range(height):
        #     for w in range(width):
        #         norm_result[h][w][0] = 255 * ((result[h][w][0] - f_min) / (f_max - f_min))
        #         norm_result[h][w][1] = 255 * ((result[h][w][1] - f_min) / (f_max - f_min))
        #         norm_result[h][w][2] = 255 * ((result[h][w][2] - f_min) / (f_max - f_min))
        
        Image.fromarray(norm_result, mode='RGB').save('Resources/sqrt_img_rgb.png')        

    def image_log(self):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        image = self.firstDecoder.getPixels24Bits()
        result = np.empty((height, width, 3), dtype=np.uint8)

        f_min = 255
        f_max = 0
        f_img_max = 0

        for h in range(height):
            for w in range(width):  
                
                R = int(image[h][w][0])
                G = int(image[h][w][1])
                B = int(image[h][w][2])

                # Poszukiwanie maksimum                
                if f_img_max < max([R, G, B]):
                    f_img_max = max([R, G, B])

        for h in range(height):
            for w in range(width):  
                
                R = int(image[h][w][0])
                G = int(image[h][w][1])
                B = int(image[h][w][2])

                if R == 0:
                    R = 0
                else:
                    R = math.log(1 + int(image[h][w][0])) / math.log(1 + int(f_img_max)) * 255

                if G == 0:
                    G = 0
                else:
                    G = math.log(1 + int(image[h][w][1])) / math.log(1 + int(f_img_max)) * 255
                
                if B == 0:
                    B = 0
                else:
                    B = math.log(1 + int(image[h][w][2])) / math.log(1 + int(f_img_max)) * 255

                result[h][w][0] = math.ceil(R)
                result[h][w][1] = math.ceil(G)
                result[h][w][2] = math.ceil(B)

                if f_min > min([R, G, B]):
                    f_min = min([R, G, B])
                if f_max < max([R, G, B]):
                    f_max = max([R, G, B])

        
        Image.fromarray(result, mode='RGB').save('Resources/log_img_rgb.png')        

    

    

    
