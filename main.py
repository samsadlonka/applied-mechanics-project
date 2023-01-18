from beam import Point, Beam
import numpy as np
from numpy.linalg import det
from drawing import *


def make_construction(adj_list, pnts):
    beams = []
    for i in range(len(points)):
        neighbors = adj_list[i]
        for neighbor in neighbors:
            p = sorted([pnts[i], pnts[neighbor]])
            new_beam = Beam(p[0], p[1], E, G, R, r)
            if new_beam not in beams:
                beams.append(new_beam)
    return beams


with open('input_parameters.txt', 'rt', encoding='utf-8') as file:
    lines = file.readlines()
    L, h = list(map(lambda x: float(x.split(":")[1]), lines[:2]))
    R, r = list(map(lambda x: float(x.split(":")[1]), lines[2:4]))
    E, G = list(map(lambda x: float(x.split(":")[1]), lines[4:6]))
    # список внешних сил
    forces_list = list(map(lambda x: -float(x.split(":")[1]), lines[6:]))

with open('graph.txt', 'rt', encoding='utf-8') as file:
    # список смежностей
    adjacency_list = list(map(lambda x: list(map(int, x.split())), file.readlines()))
    points = [Point(L / 2, 0, h), Point(L / 3, 0, 2 * h / 3), Point(2 * L / 3, 0, 2 * h / 3)]
    points += [Point(L / 6, 0, h / 3), Point(5 * L / 6, 0, h / 3)]
    points += [Point(L / 6 * i, 0, 0) for i in range(7)]

list_of_beams = make_construction(adjacency_list, points)

for i in range(len(points)):
    neighbors = adjacency_list[i]
    for neighbor in neighbors:
        p = sorted([points[i], points[neighbor]])
        new_beam = Beam(p[0], p[1], E, G, R, r)
        if new_beam not in list_of_beams:
            list_of_beams.append(new_beam)

index_matrix = []
for s in open('matrix.txt', 'r').readlines():
    index_matrix.append([int(x) for x in s.split('\t')])

Kg = [[0] * 72 for _ in range(72)]

vec = [1, 2, 17, 16, 15, 3, 18, 19, 4, 5, 13, 14, 20, 21, 6, 7, 8, 9, 10, 11, 12]

for i in range(len(list_of_beams)):
    for j in range(len(index_matrix[i])):
        for m in range(len(index_matrix[i])):
            Kg[index_matrix[vec[i] - 1][j] - 1][index_matrix[vec[i] - 1][m] - 1] += \
                list_of_beams[i].global_matrix[j][m]
F = [0.] * 72
draw(list_of_beams)
for i in range(12):
    F[i * 6 + 2] = forces_list[i]
F = np.array(F)
Kg = np.array(Kg)

lst = [index_matrix[4][:6], index_matrix[11][6:]]
for elem in lst:
    for i in elem:
        for j in range(72):
            Kg[i - 1][j] = 0
            Kg[j][i - 1] = 0
        Kg[i - 1][i - 1] = 1
U = np.linalg.solve(Kg, F)
for i in lst:
    for j in i:
        U[j - 1] = 0
for i in range(12):
    if U[i * 6 + 1] > 1 ** -10 or U[i * 6 + 4] > 1 ** -10 or U[i * 6 + 5] > 1 ** -10 or U[i * 6 + 2] > 0:
        print("blin", U[i * 6:i * 7])

for i in range(len(points)):
    points[i].update(U[i * 6], U[i * 6 + 1], U[i * 6 + 2])

new_list_of_beams = make_construction(adjacency_list, points)

tension_list = []
for i in range(len(list_of_beams)):
    eps = abs(list_of_beams[i].l - new_list_of_beams[i].l) / list_of_beams[i].l
    tension_list.append(list_of_beams[i].E * eps)


draw(new_list_of_beams)
draw(new_list_of_beams, tension_list)
