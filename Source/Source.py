import argparse
import sys

from Unification import Unification
from Geometric import Geometric

def main():
    #unificationModule()
    geometricModule()

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

if __name__ == '__main__':
    main()