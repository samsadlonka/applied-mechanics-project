"""
Топология конструкции задается через список смежностей graph.txt,
где нумерация вершин имеет следующий вид и первая строка соответствует
описанию соседей для 0 вершины, вторая для 1 и т.д.
            0
        1       2
    3               4
5   6   7   8   9   10  11
"""


class Point:
    def __init__(self, x, z):
        self.x = x
        self.z = z


L = int(input("Введите значение L для фермы"))
h = int(input("Введите значение h для фермы"))
f = open("graph.txt", 'rt', encoding='utf-8')
# список смежностей
adjacency_list = list(map(lambda x: list(map(int, x.split())), f.readlines()))
points = [Point(L / 2, h), Point(L / 3, 2 * h / 3), Point(2 * L / 3, 2 * h / 3)]
points += [Point(L / 6, h / 3), Point(5 * L / 6, h / 3)]
points += [Point(L / 6 * i, 0) for i in range(7)]

