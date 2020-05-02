import numpy
from PIL import Image
from matplotlib import pyplot

from ImageDecoder import ImageDecoder

class ImageHelper(object):
    @staticmethod
    def Save(result, imageType, operationName, isNorm, firstDecoder, secondDecoder = None, idValue = None):
        imageName = ImageHelper._composeName(operationName, isNorm, firstDecoder, secondDecoder, idValue)
        img = Image.fromarray(result, mode = imageType)
        img.save('Resources/result/' + imageName + '.png')
        
    @staticmethod
    def SaveHistogram(bins, histogram, operationName, isNorm, firstDecoder, secondDecoder = None, idValue = None):
        fig = pyplot.figure(figsize=[9, 7])
        pyplot.bar(bins[:-1], histogram, width=0.8, color='#606060')
        pyplot.xlim(min(bins), max(bins))
        pyplot.xlabel('Value', fontsize=15)
        pyplot.xticks(fontsize=15)
        pyplot.grid(axis='y', alpha=0.75)
        pyplot.ylabel('Frequency', fontsize=15)
        pyplot.yticks(fontsize=15)
        pyplot.ylabel('Frequency', fontsize=15)

        imageName = ImageHelper._composeName(operationName, isNorm, firstDecoder, secondDecoder, idValue)
        pyplot.savefig('Resources/result/' + imageName + '.png')

    @staticmethod
    def _composeName(operationName, isNorm, firstDecoder, secondDecoder = None, idValue = None):
        imageName = operationName + '-'
        imageName += firstDecoder.name.split('/')[1].split('.')[0]
        if secondDecoder != None:
            imageName += '-'
            imageName += secondDecoder.name.split('/')[1].split('.')[0]

        if idValue != None:
            imageName += '-'
            if isinstance(idValue, float):
                imageName += str(int(idValue*10))
            else:
                imageName += str(idValue)

        if isNorm:
            imageName += '-norm'

        return imageName