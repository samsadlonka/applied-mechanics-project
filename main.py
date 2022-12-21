from beam import Point, Beam

L = int(input("Введите значение L для фермы"))
h = int(input("Введите значение h для фермы"))
with open("graph.txt", 'rt', encoding='utf-8') as file:
    # список смежностей
    adjacency_list = list(map(lambda x: list(map(int, x.split())), file.readlines()))
    points = [Point(L / 2, 0, h), Point(L / 3, 0, 2 * h / 3), Point(2 * L / 3, 0, 2 * h / 3)]
    points += [Point(L / 6, 0, h / 3), Point(5 * L / 6, 0, h / 3)]
    points += [Point(L / 6 * i, 0, 0) for i in range(7)]

with open("forces.txt", 'rt', encoding='utf-8') as file:
    # список внешних сил
    forces_list=list(map(lambda x: float(x.split(":")[1]), file.readlines()))


list_of_beams = []

for i in range(len(points)):
    neighbors = adjacency_list[i]
    for neighbor in neighbors:
        new_beam = Beam(points[i], neighbor, 1, 1)
        if new_beam not in list_of_beams:
            list_of_beams.append(new_beam)

index_matrix = [[] for _ in range(5)] * 12

