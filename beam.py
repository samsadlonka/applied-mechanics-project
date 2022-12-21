from math import sqrt, pi
import numpy as np


class Point:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z

    def length(self, other_point):
        return sqrt((self.x - other_point.x) ** 2
                    + (self.y - other_point.y) ** 2 + (self.z - other_point.z) ** 2)

    def __lt__(self, other):
        return self.x < other.x or self.y < other.y or self.z < other.z


class Beam:
    def __init__(self, _pnt_1, _pnt_2, _E, _G, R, r):
        self.pnt_1 = _pnt_1
        self.pnt_2 = _pnt_2
        self.l = _pnt_1.length(_pnt_2)
        self.E = _E
        self.G = _G
        self.J = 1
        self.A = pi * R ** 2 - pi * r ** 2
        self.local_matrix = self.make_local_matrix()
        self.global_matrix = self.make_with_global()

    def make_with_global(self):
        v1 = np.array([(self.pnt_2.x - self.pnt_1.x) / self.pnt_2.length(self.pnt_1), (self.pnt_2.y - self.pnt_1.y) /
                       self.pnt_2.length(self.pnt_1),
                       (self.pnt_2.z - self.pnt_1.z) / self.pnt_2.length(self.pnt_1)])
        v2 = np.array([(0 - self.pnt_1.x) / self.pnt_1.length(Point(0, 1, 0)),
                       (1 - self.pnt_1.y) / self.pnt_1.length(Point(0, 1, 0)),
                       (0 - self.pnt_1.z) / self.pnt_1.length(Point(0, 1, 0))])
        v3 = np.cross(v1, v2)
        v2 = np.cross(v1, v3)
        rotation_matrix = np.array(v1, v2, v3)
        rotation_matrix = np.transpose(rotation_matrix)
        T_Ke = np.dot(rotation_matrix, self.local_matrix)
        result = np.dot(T_Ke, np.transpose(rotation_matrix))
        return result

    def __eq__(self, other_beam):
        this = sorted([self.pnt_1, self.pnt_2])
        other = sorted([other_beam.pnt_1, other_beam.pnt_2])
        return this == other

    def make_local_matrix(self):
        k11 = np.array([[12 * self.E * self.J / self.l ** 3, 0, 0, 0, 6 * self.E * self.J / self.l ** 2, 0],
                        [0, 12 * self.E * self.J / self.l ** 3, 0, -6 * self.E * self.J / self.l ** 2, 0, 0],
                        [0, 0, self.E * self.A / self.l, 0, 0, 0],
                        [0, -6 * self.E * self.J / self.l ** 2, 0, 4 * self.E * self.J / self.l, 0, 0],
                        [6 * self.E * self.J / self.l ** 2, 0, 0, 0, 4 * self.E * self.J / self.l, 0],
                        [0, 0, 0, 0, 0, self.G * self.J / self.l]])
        k12 = np.array([[-12 * self.E * self.J / self.l ** 3, 0, 0, 0, 6 * self.E * self.J / self.l ** 2, 0],
                        [0, -12 * self.E * self.J / self.l ** 3, 0, -6 * self.E * self.J / self.l ** 2, 0, 0],
                        [0, 0, -self.E * self.A / self.l, 0, 0, 0],
                        [0, 6 * self.E * self.J / self.l ** 2, 0, 0, 0],
                        [-6 * self.E * self.J / self.l ** 2, 0, 0, 0, 2 * self.E * self.J / self.l],
                        [0, 0, 0, 0, 0, -self.G * self.J / self.l]])
        k21 = np.transpose(k12)
        C = np.array([[-1, 0, 0, 0, 0, 0],
                      [0, -1, 0, 0, 0, 0],
                      [0, 0, -1, 0, 0, 0],
                      [0, -self.l, 0, -1, 0, 0],
                      [self.l, 0, 0, 0, -1, 0],
                      [0, 0, 0, 0, 0, -1]])
        k22 = np.dot(C, k12)
        Kl = np.array([k11, k12],
                      [k21, k22])
        return Kl
