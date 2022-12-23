from beam import Point, Beam

with open('input_parameters.txt', 'rt', encoding='utf-8') as file:
    lines = file.readlines()
    L, h = list(map(lambda x: float(x.split(":")[1]), lines[:2]))
    R, r = list(map(lambda x: float(x.split(":")[1]), lines[2:4]))
    E, G = list(map(lambda x: float(x.split(":")[1]), lines[4:6]))
    # список внешних сил
    forces_list = list(map(lambda x: float(x.split(":")[1]), file.readlines()))

with open('graph.txt', 'rt', encoding='utf-8') as file:
    # список смежностей
    adjacency_list = list(map(lambda x: list(map(int, x.split())), file.readlines()))
    points = [Point(L / 2, 0, h), Point(L / 3, 0, 2 * h / 3), Point(2 * L / 3, 0, 2 * h / 3)]
    points += [Point(L / 6, 0, h / 3), Point(5 * L / 6, 0, h / 3)]
    points += [Point(L / 6 * i, 0, 0) for i in range(7)]

list_of_beams = []

for i in range(len(points)):
    neighbors = adjacency_list[i]
    for neighbor in neighbors:
        new_beam = Beam(points[i], points[neighbor], E, G, R, r)
        if new_beam not in list_of_beams:
            list_of_beams.append(new_beam)

index_matrix = []
for s in open('matrix.txt', 'r').readlines():
    index_matrix.append([int(x) for x in s.split('\t')])
