import argparse
import sys

from Unification import Unification
from Geometric import Geometric
from BinaryMorphological import BinaryMorphological
from GrayMorphological import GrayMorphological

def main():
    #unificationModule()
    #geometricModule()
    #morphologicalModule()
    grayMorphologicalModule()

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
    morph.erosion(10, 10, 0)
    #morph.dilation()
    #morph.opening()
    #morph.closing()

if __name__ == '__main__':
    main()