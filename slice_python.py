import argparse
import logging
import numpy as np
from scipy.interpolate import interpn

logging.basicConfig(filename='slice.log', level=logging.DEBUG, filemode="w")


class Cubefile:
    def __init__(self, filename):
        self.filename = filename
        header, natoms, origin, n1, vect1, n2, vect2, n3, vect3, geom, data = read_cube(filename)
        self.natoms = natoms
        self.origin = origin
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.vect1 = vect1
        self.vect2 = vect2
        self.vect3 = vect3
        self.geom = geom
        self.data = data

    def print(self):
        print("Filename : {}".format(self.filename))
        print("Npts     : {}".format(len(self.data)))
        print("Data Min : {}".format(np.amin(self.data)))
        print("Data Max : {}".format(np.amax(self.data)))

    def getgrid(self):
        x = np.array([])
        y = np.array([])
        z = np.array([])
        for ix in range(self.n1):
            for iy in range(self.n2):
                for iz in range(self.n3):
                    pt = self.origin + \
                         ix * self.vect1 + \
                         iy * self.vect2 + \
                         iz * self.vect3
                    x = np.append(x, [pt[0]])
                    y = np.append(y, [pt[1]])
                    z = np.append(z, [pt[2]])
        return x, y, z

    def getXvalues(self):
        """This function assumes that vect1 is along X, vect2 along Y and vect3 along Z"""
        return np.linspace(self.origin[0], self.origin[0] + self.vect1[0] * (self.n1 - 1), self.n1)

    def getYvalues(self):
        """This function assumes that vect1 is along X, vect2 along Y and vect3 along Z"""
        return np.linspace(self.origin[1], self.origin[1] + self.vect2[1] * (self.n2 - 1), self.n2)

    def getZvalues(self):
        """This function assumes that vect1 is along X, vect2 along Y and vect3 along Z"""
        return np.linspace(self.origin[2], self.origin[2] + self.vect3[2] * (self.n3 - 1), self.n3)


def read_cube(fn):
    f = open(fn, 'r')
    lines = f.readlines()
    header = lines[0:1]
    origin = np.empty(3)
    vect1 = np.empty(3)
    vect2 = np.empty(3)
    vect3 = np.empty(3)
    natoms, origin[0], origin[1], origin[2] = [float(l) for l in lines[2].split()]
    n1, vect1[0], vect1[1], vect1[2] = [float(l) for l in lines[3].split()]
    n2, vect2[0], vect2[1], vect2[2] = [float(l) for l in lines[4].split()]
    n3, vect3[0], vect3[1], vect3[2] = [float(l) for l in lines[5].split()]
    natoms = int(natoms)
    n1 = int(n1)
    n2 = int(n2)
    n3 = int(n3)
    geom = lines[6:6 + natoms]
    data = np.empty(n1 * n2 * n3)
    i = 0
    for l in lines[6 + natoms:]:
        data[i] = float(l)
        i = i + 1
    data = data.reshape(n1, n2, n3)
    return header, natoms, origin, n1, vect1, n2, vect2, n3, vect3, geom, data


def main():
    """
    Main routine
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file", default="data.cub")
    parser.add_argument("-p", "--point", help="One point of the plane", type=float, nargs=3, default=(0., 0., 0.))
    parser.add_argument("-n", "--normal", help="The normal of the plane", type=float, nargs=3, default=(1., 0., 0.))
    args = parser.parse_args()
    point_in_plane = np.array([args.point[0], args.point[1], args.point[2]])
    normal_to_plane = np.array([args.normal[0], args.normal[1], args.normal[2]])
    filename = args.input
    cubedata = Cubefile(filename)
    cubedata.print()
    print(cubedata.origin)
    print(cubedata.getgrid()[0])
    print(cubedata.data[0, 0, 0])
    Vi = interpn((cubedata.getXvalues(), cubedata.getYvalues(), cubedata.getZvalues()), cubedata.data,
                 np.array([[-17.5615, -12.8185, -6.83306 + i*0.759228] for i in range(19)]))
    for i in range(19):
        print("{:1.8f} {:1.12f}".format(-6.83306+i*0.759228, Vi[i]))
    Vi = interpn((cubedata.getXvalues(), cubedata.getYvalues(), cubedata.getZvalues()), cubedata.data,
                 np.array([[-17.5615, -12.8185, -6.83306 + i*0.075922] for i in range(179)]))
    for i in range(179):
        print("{:1.8f} {:1.12f}".format(-6.83306 + i * 0.075922, Vi[i]))


if __name__ == '__main__':
    main()
