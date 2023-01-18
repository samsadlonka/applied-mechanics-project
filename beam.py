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
        return self.x < other.x or self.z > other.z or self.y < other.y

    def __eq__(self, other):
        return abs(self.x - other.x) < 0.01 and abs(self.y - other.y) < 0.01 and abs(self.z - other.z) < 0.01

    def __repr__(self):
        return ' '.join([self.x, self.y, self.z])

    def update(self, u1, u2, u3):
        self.x += u1
        self.y += u2
        self.z += u3

    def get_coord(self):
        return self.x, self.y, self.z


class Beam:
    def __init__(self, _pnt_1, _pnt_2, _E, _G, R, r):
        R = R / 10 ** 3
        r = r / 10 ** 3
        self.pnt_1 = _pnt_1
        self.pnt_2 = _pnt_2
        self.l = _pnt_1.length(_pnt_2)
        self.E = _E * 10 ** 6
        self.G = _G * 10 ** 6
        self.Jz = self.Jy = pi * (2 * R) ** 4 * (1 - (r / R) ** 4) / 64
        self.Jx = self.Jz * 2
        self.A = pi * R ** 2 - pi * r ** 2
        self.local_matrix = self.make_local_matrix()
        self.global_matrix = self.make_with_global()

    def make_with_global(self):
        rotation_matrix = self.make_rotation_matrix()
        T_Ke = np.dot(rotation_matrix, self.local_matrix)
        result = np.dot(T_Ke, np.transpose(rotation_matrix))
        return result

    def get_points(self):
        return [self.pnt_1.get_coord(), self.pnt_2.get_coord()]

    def __eq__(self, other_beam):
        return (self.pnt_1 == other_beam.pnt_1 and self.pnt_2 == other_beam.pnt_2) \
               or (self.pnt_1 == other_beam.pnt_2 and self.pnt_2 == other_beam.pnt_1)

    def make_rotation_matrix(self):
        v1 = np.array([(self.pnt_2.x - self.pnt_1.x) / self.pnt_2.length(self.pnt_1), (self.pnt_2.y - self.pnt_1.y) /
                       self.pnt_2.length(self.pnt_1),
                       (self.pnt_2.z - self.pnt_1.z) / self.pnt_2.length(self.pnt_1)], dtype=float)
        v2 = np.array([(0 - self.pnt_1.x) / self.pnt_1.length(Point(0, 1, 0)),
                       (1 - self.pnt_1.y) / self.pnt_1.length(Point(0, 1, 0)),
                       (0 - self.pnt_1.z) / self.pnt_1.length(Point(0, 1, 0))], dtype=float)
        v3 = np.cross(v1, v2)
        v2 = np.cross(v1, v3)
        matrix = np.vstack((v1, v2, v3))
        matrix = np.transpose(matrix)
        null_matrix = np.array([[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0]], dtype=float)
        rotation_matrix = np.vstack((np.hstack((matrix, null_matrix, null_matrix, null_matrix)),
                                     np.hstack((null_matrix, matrix, null_matrix, null_matrix)),
                                     np.hstack((null_matrix, null_matrix, matrix, null_matrix)),
                                     np.hstack((null_matrix, null_matrix, null_matrix, matrix))
                                     ))
        return rotation_matrix

    def make_local_matrix(self):
        k11 = self.E * self.A / self.l
        k22 = 12 * self.E * self.Jz / self.l ** 3
        k33 = 12 * self.E * self.Jy / self.l ** 3
        k26 = 6 * self.E * self.Jz / self.l ** 2
        k35 = 6 * self.E * self.Jy / self.l ** 2
        k44 = self.G * self.Jx / self.l
        k55 = 4 * self.E * self.Jy / self.l
        k66 = 4 * self.E * self.Jz / self.l
        k511 = 2 * self.E * self.Jy / self.l
        k612 = 2 * self.E * self.Jz / self.l
        Kl = np.array([[k11, 0, 0, 0, 0, 0, -k11, 0, 0, 0, 0, 0],
                       [0, k22, 0, 0, 0, k26, 0, -k22, 0, 0, 0, k26],
                       [0, 0, k33, 0, -k35, 0, 0, 0, -k33, 0, -k35, 0],
                       [0, 0, 0, k44, 0, 0, 0, 0, 0, -k44, 0, 0],
                       [0, 0, -k35, 0, k55, 0, 0, 0, k35, 0, k511, 0],
                       [0, k26, 0, 0, 0, k66, 0, -k26, 0, 0, 0, k612],
                       [-k11, 0, 0, 0, 0, 0, k11, 0, 0, 0, 0, 0],
                       [0, -k22, 0, 0, 0, -k26, 0, k22, 0, 0, 0, -k26],
                       [0, 0, -k33, 0, k35, 0, 0, 0, k33, 0, k35, 0],
                       [0, 0, 0, -k44, 0, 0, 0, 0, 0, k44, 0, 0],
                       [0, 0, -k35, 0, k511, 0, 0, 0, k35, 0, k55, 0],
                       [0, k26, 0, 0, 0, k612, 0, -k26, 0, 0, 0, k66]]
                      )
        return Kl

    def __repr__(self):
        return ' '.join(map(str, [self.pnt_1.x, self.pnt_1.z, self.pnt_2.x, self.pnt_2.z]))
