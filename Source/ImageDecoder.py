import numpy
from PIL import Image

class ImageDecoder(object):
    def __init__(self, name, pictureType):
        self.name = name
        self.im = Image.open(name).convert(pictureType)
        self.height = self.getHeight()
        self.width = self.getWidth()

    def getGreyMatrix(self):
        matrix = numpy.array(self.im)
        return matrix

    def getRGBMatrix(self):
        loadmatrix = numpy.array(self.im)
        return loadmatrix

    def getSize(self):
        return self.im.size

    def getWidth(self):
        size = self.im.size
        width = size[0]
        return width

    def getHeight(self):
        size = self.im.size
        length = size[1]
        return length