from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):
    def __init__(self, coordinates):

        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):

        return self.coordinates == v.coordinates

    def __add__(self, other):

        new_coordinates = [x + y for x, y in zip(self.coordinates, other.coordinates)]
        return Vector(new_coordinates)


    def minus(self, v):

        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)


    def scalar_mult(self, scalar):
        new_coord = [Decimal(scalar) * x for x in self.coordinates]

        return Vector(new_coord)

    def magnitude(self):

        magnitude = 0

        for i in self.coordinates:
            magnitude += i * i

        return Decimal(sqrt(magnitude))

    def direction(self):

        return self.scalar_mult(1 / self.magnitude())

    def dot_product(self, other):

        return sum([x * y for x, y in zip(self.coordinates, other.coordinates)])

    def normalize(self):

        try:
            magnitude = self.magnitude()
            return self.scalar_mult(Decimal('1.0') / magnitude)
        except ZeroDivisionError:
            raise Exception("Cannot normalize zero vero vector")

    def angle(self, other, degrees=False):

        pr1 = self.normalize()
        pr2 = other.normalize()

        theta = acos(pr1.dot_product(pr2))

        if degrees:
            return theta * (180. / pi)
        else:
            return theta

    def isOrthoganal(self, other):

        return abs(self.dot_product(other)) < 1e-10

    def isParallel(self, other):

        return (self.is_zero()
                or other.is_zero()
                or self.angle(other) == 0
                or abs(self.angle(other) - pi) < 0.01)  # HACK could not get exact pi

    def is_zero(self, tolerance=1e-10):

        return self.magnitude() < tolerance

# v=Vector([8.218, -9.341])
# w=Vector([-1.129, 2.111])
# print v.__add__(w)
#
# a=Vector([7.119, 8.215])
# b=Vector([-8.223, 0.878])
# print a.minus(b)
#
# d= Vector([1.672, -1.012, -0.3318])
# print d.scalar_mult(7.41)
#
#
# v1= Vector([-0.221, 7.437])
# v2= Vector([8.813, -1.331, -6.247])
# v3= Vector([5.581, -2.136])
# v4= Vector([1.996, 3.108, -4.554])
#
# print v1.magnitute()
# print v2.magnitute()
# print v3.direction()
# print v4.direction()
#
# a = Vector([7.887, 4.138])
# b = Vector([-8.802, 6.776])
# print a.dot_product(b)
#
# c = Vector([-5.955, -4.904, -1.874])
# d = Vector([-4.496, -8.755, 7.103])
# print c.dot_product(d)
#
# e = Vector([3.183, -7.627])
# f = Vector([-2.668, 5.319])
# print e.angle(f, False)
#
# g = Vector([7.35, 0.221, 5.188])
#
# h = Vector([2.751, 8.259, 3.985])
# print g.angle(h, True)

vectors_a = [
    Vector([-7.579, -7.88]),
    Vector([-2.029, 9.97, 4.172]),
    Vector([-2.328, -7.284, -1.214])
]
vectors_b = [
    Vector([22.373, 23.64]),
    Vector([-9.231, -6.639, -7.245]),
    Vector([-1.821, 1.072, -2.94])
]

print vectors_a[0].isParallel(vectors_b[0]), vectors_a[0].isOrthoganal(vectors_b[0])
print vectors_a[1].isParallel(vectors_b[1]), vectors_a[1].isOrthoganal(vectors_b[1])
print vectors_a[2].isParallel(vectors_b[2]), vectors_a[2].isOrthoganal(vectors_b[2])