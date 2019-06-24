import argparse
import sys

from Unification import Unification
from Geometric import Geometric
from BinaryMorphological import BinaryMorphological
from GrayMorphological import GrayMorphological
from Filters import Filters

def main():
    #unificationModule()
    #geometricModule()
    #morphologicalModule()
    #grayMorphologicalModule()
    filteringModule()

def unificationModule():
    unification = Unification('Resources/cat.djvu', 'Resources/photoman.djvu')
    unification.geometricGray()
    unification.rasterGray()
    unification = Unification('Resources/coffee.djvu', 'Resources/phone.djvu')
    unification.geometricColor()
    unification.rasterColor()

def geometricModule():
    geometric = Geometric('Resources/phone.djvu')
    geometric.translate(100, -100)
    geometric.homogeneousScaling(2.0)
    geometric.nonUniformScaling(2.0, 1.0)
    geometric.rotation(45)
    geometric.axisSymmetry(True, True)
    geometric.customSymmetryX(356)
    geometric.customSymmetryY(356)
    point1, point2 = (50, 50), (300, 300)
    geometric.crop(point1, point2)
    point1, point2 = (50, 50), (300, 300)
    geometric.copy(point1, point2)

def morphologicalModule():
    morph = BinaryMorphological('Resources/binary.djvu')
    morph.erosion()
    morph.dilation()
    morph.opening()
    morph.closing()

def grayMorphologicalModule():
    morph = GrayMorphological('Resources/photoman.djvu')
    morph.erosion(10, 10, 0, (4, 4))
    morph.dilation(5, 5, 50, (2, 2))
    morph.opening(10, 10, 100, (4, 4))
    morph.closing(5, 5, 0, (2, 2))

def filteringModule():
    #filters = Filters('Resources/photoman.djvu')
    #filters.boxBlur((9, 9))
    #filters.boxBlur((27, 27))
    #filters.gaussianBlur(9, 546)
    #filters.gaussianBlur(9*2, 546*2)
    #filters = Filters('Resources/phone-noise.djvu')
    #filters.median(9)
    #filters.median(27)
    #filters = Filters('Resources/photoman.djvu')
    #filters.modalGray(9)
    #filters.modalGray(18)
    #filters.modalGray(27)
    #filters.kuwaharaGray(3)
    #filters.kuwaharaGray(9)
    #filters.kuwaharaGray(27)
    filters = Filters('Resources/phone.djvu')
    filters.kuwaharaColor(3)
    #filters.kuwaharaColor(9)
    #filters.kuwaharaColor(27)

if __name__ == '__main__':
    main()