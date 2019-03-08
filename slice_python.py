import argparse
import logging
import numpy as np

logging.basicConfig(filename='slice.log', level=logging.DEBUG, filemode="w")

class Cubefile:
    def __init__(self, filename):
        self.filename=filename
        header, natoms, origin, n1, vect1, n2, vect2, n3, vect3, data = read_cube(filename)
        self.natoms = natoms
        self.origin = origin
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.vect1 = vect1
        self.vect2 = vect2
        self.vect3 = vect3
        self.data = data

def read_cube(fn)
    f = open(fn, 'r')
    lines=f.readlines()
    header = lines[0:1]
    origin = np.empty(3)
    vect1 = np.empty(3)
    vect2 = np.empty(3)
    vect3 = np.empty(3)
    natoms, origin[0], origin[1], origin[2] = lines[2].split()
    n1, vect1[0], vect1[1], vect1[2] = lines[3].split()
    n2, vect2[0], vect2[1], vect2[2] = lines[4].split()
    n3, vect3[0], vect3[1], vect3[2] = lines[5].split()
    data=np.empty(n1*n2*n3)
    for l in lines[3:]:
        np.append(np, l.split())
        data.reshape(n1,n2,n3)
    return header, natoms, origin, n1, vect1, n2, vect2, n3, vect3, data

def main():
    """
    Main routine
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file", default="data.cub")
    parser.add_argument("-p", "--point", help="One point of the plane", type=float, nargs=3, default="0 0 0")
    parser.add_argument("-n", "--normal", help="The normal of the plane", type=float, nargs=3, default="1 0 0")
    args = parser.parse_args()
    point_in_plane = np.array([args.point[0],args.point[1],args.point[2]])
    normal_to_plane = np.array([args.normal[0],args.normal[1],args.normal[2]])
    filename=args.input
    cubefile = Cubefile(filename)

if __name__== '__main__':
    main()
