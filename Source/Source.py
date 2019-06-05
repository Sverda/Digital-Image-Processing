import argparse
import sys

from Unification import Unification
from Geometric import Geometric

def main():
    geometricModule()

def unificationModule():
    unification = Unification('Resources/cat.djvu', 'Resources/photoman.djvu')
    #unification.geometricGray()
    unification.rasterGray()
    #unification = Unification('Resources/coffee.djvu', 'Resources/phone.djvu')
    #unification.geometricColor()
    #unification.rasterColor()

def geometricModule():
    geometric = Geometric('Resources/coffee.djvu')
    #geometric.translate(100, -100)
    geometric.homogeneousScaling(2.0)

if __name__ == '__main__':
    main()