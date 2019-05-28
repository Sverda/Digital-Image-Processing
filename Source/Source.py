import argparse
import sys

from Unification import Unification

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('first_djvu_path')
    parser.add_argument('second_djvu_path')
    options = parser.parse_args()

    unification = Unification(options.first_djvu_path, options.second_djvu_path)
    unification.geometricGray()

if __name__ == '__main__':
    main()