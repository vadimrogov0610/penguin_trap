from typing import Set


class Ice:
    def __init__(self, x: int, y: int, z: int, color=True):
        m = min(x, y, z)
        self.x = x - m
        self.y = y - m
        self.z = z - m
        self.color = color

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    @property
    def neighborhood(self) -> set:
        ans = set()
        for t in NH:
            ans.add(Ice(self.x + t[0], self.y + t[1], self.z + t[2]))
        return ans

    @property
    def nx(self) -> set:
        return {Ice(self.x + 1, self.y, self.z), Ice(self.x, self.y + 1, self.z + 1)}

    @property
    def ny(self) -> set:
        return {Ice(self.x, self.y + 1, self.z), Ice(self.x + 1, self.y, self.z + 1)}

    @property
    def nz(self) -> set:
        return {Ice(self.x, self.y, self.z + 1), Ice(self.x + 1, self.y + 1, self.z)}


class CustomError(Exception):
    pass


NH = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
Field: Set[Ice] = {Ice(0, 0, 0)}
nh: Set[Ice] = set()
for _ in range(3):
    nh = set.union(*[a.neighborhood for a in Field])
    Field.update(nh)
Field.remove(Ice(0, 0, 3))
Field.remove(Ice(3, 3, 0))
Field.add(Ice(4, 0, 2))
Field.add(Ice(0, 4, 2))
All: Set[Ice] = set.union(*[a.neighborhood for a in Field])
'''
nh = {Ice(0, 0, 0)}
fall: Set[Ice] = set()
while nh:
    nh = set()
    for a in Field:
        if not (a.nx.issubset(All) or a.ny.issubset(All) or a.nz.issubset(All)):
            nh.add(a)
    Field -= nh
    All -= nh
    fall.update(nh)
for i in fall:
    print(i)
'''
