import argparse
import sys

from Unification import Unification
from Geometric import Geometric
from ArithmeticSumGray import ArithmeticSumGray
from ArithmeticSumColor import ArithmeticSumColor

def main():
    #unificationModule()
    #geometricModule()
    #grayArithmeticSumModule()
    colorArithmeticSumModule()

def unificationModule():
    unification = Unification('Resources/cat.png', 'Resources/photoman.png', "L")
    unification.geometricGray()
    unification.rasterGray()

    unification = Unification('Resources/coffee.png', 'Resources/phone.png', "RGB")
    unification.geometricColor()
    unification.rasterColor()

def geometricModule():
    geometric = Geometric('Resources/phone.png', "RGB")
    geometric.translate(100, -100)
    geometric.homogeneousScaling(2.0)
    geometric.nonUniformScaling(2.0, 1.0)
    geometric.rotation(45)
    geometric.axisSymmetry(True, True)
    geometric.customSymmetryX(356)
    geometric.customSymmetryY(356)
    point1, point2 = (50, 50), (100, 100)
    geometric.crop(point1, point2)
    point1, point2 = (50, 50), (100, 100)
    geometric.copy(point1, point2)

def grayArithmeticSumModule():
    gray = ArithmeticSumGray('Resources/photoman.png', 'Resources/lena.png', 'L')
    gray.sumWithConst(30)
    gray.sumWithConst(300)
    gray.sumImages()
    gray.multiplyWithConst(0.5)
    gray.multiplyWithConst(1.5)
    gray.multiplyImages()
    gray.blendImages(0.2)
    gray.blendImages(0.5)
    gray.blendImages(0.8)
    gray.powerFirstImage(0.5)
    gray.powerFirstImage(2)
    gray = ArithmeticSumGray('Resources/cat.png', 'Resources/photoman.png', 'L')
    gray.sumWithConst(30)
    gray.sumWithConst(300)
    gray.sumImages()
    gray.multiplyWithConst(0.5)
    gray.multiplyWithConst(1.5)
    gray.multiplyImages()
    gray.powerFirstImage(0.5)
    gray.powerFirstImage(2)
    gray = ArithmeticSumGray('Resources/cat.png', 'Resources/window-mask.png', 'L')
    gray.multiplyImages()
    gray = ArithmeticSumGray('Resources/cat.png', 'Resources/mask.png', 'L')
    gray.multiplyImages()

def colorArithmeticSumModule():
    color = ArithmeticSumColor('Resources/coffee.png', 'Resources/phone.png', 'RGB')
    #color.sumWithConst(30)
    #color.sumWithConst(200)
    #color.sumWithConst(300)
    #color.sumImages()
    #color.multiplyWithConst(0.5)
    #color.multiplyWithConst(1.5)
    #color.multiplyImages()
    #color.blendImages(0.2)
    #color.blendImages(0.5)
    #color.blendImages(0.8)
    color.powerFirstImage(0.5)
    color.powerFirstImage(2)
    color = ArithmeticSumColor('Resources/phone.png', 'Resources/sea.png', 'RGB')
    #color.sumWithConst(30)
    #color.sumWithConst(200)
    #color.sumWithConst(300)
    #color.sumImages()
    #color.multiplyWithConst(0.5)
    #color.multiplyWithConst(1.5)
    #color.multiplyImages()
    color.powerFirstImage(0.5)
    color.powerFirstImage(2)

if __name__ == '__main__':
    main()