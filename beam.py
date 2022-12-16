from math import sqrt, atan, cos, sin
import numpy as np


class Point:
    def __init__(self, _name, _x, _y, _z):
        self.name = _name
        self.x = _x
        self.z = _z

    def length(self, other_point):
        return sqrt((self.x - other_point.x) ** 2
                    + (self.z - other_point.z) ** 2)

    def __lt__(self, other):
        return self.x < other.x or self.z < other.z


class Beam:
    def __init__(self, _pnt_1, _pnt_2, _E, _A):
        self.pnt_1 = _pnt_1
        self.pnt_2 = _pnt_2
        self.l = _pnt_1.length(_pnt_2)
        self.E = _E
        self.J = 1
        self.A = _A
        self.local_matrix = np.array([[12 * self.E * self.J / self.l ** 3, -6 * self.E * self.J / self.l ** 2,
                                       -12 * self.E * self.J / self.l ** 3, -6 * self.E * self.J / self.l ** 2],
                                      [-6 * self.E * self.J / self.l ** 2, 4 * self.E * self.J / self.l ** 1,
                                       6 * self.E * self.J / self.l ** 2, 2 * self.E * self.J / self.l ** 1],
                                      [-12 * self.E * self.J / self.l ** 3, 6 * self.E * self.J / self.l ** 2,
                                       12 * self.E * self.J / self.l ** 3, 6 * self.E * self.J / self.l ** 2],
                                      [-6 * self.E * self.J / self.l ** 2, 2 * self.E * self.J / self.l ** 1,
                                       6 * self.E * self.J / self.l ** 2, 4 * self.E * self.J / self.l ** 1]
                                      ])
        self.global_matrix = self.make_with_global()
        self.fi = atan((_pnt_2.z - _pnt_1.z) / (_pnt_2.x - _pnt_1.x))

    def make_with_global(self):
        fi = self.fi
        rotation_matrix = np.array([[cos(fi), -sin(fi), 0, 0],
                                    [sin(fi), cos(fi), 0, 0],
                                    [0, 0, cos(fi), -sin(fi)],
                                    [0, 0, sin(fi), cos(fi)]]
                                   )
        T_Ke = np.dot(rotation_matrix, self.local_matrix)
        result = np.dot(T_Ke, np.transpose(rotation_matrix))
        return result

    def __eq__(self, other_beam):
        this = sorted([self.pnt_1, self.pnt_2])
        other = sorted([other_beam.pnt_1, other_beam.pnt_2])
        return this == other
