from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Line(object):
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        # try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0'] * self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c / initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        # except Exception as e:
        #     if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
        #         self.basepoint = None
        #     else:
        #         raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i == initial_index)) + 'x_{}'.format(i + 1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    def isLineParallel(self, other):
        n1 = self.normal_vector
        n2 = other.normal_vector

        return n1.isParallel(n2);

    def isLineCoincedental(self, other):
        if not self.isLineParallel(other):
            return False

        x0 = self.basepoint
        y0 = other.basepoint

        basePointDiff = x0.minus(y0)

        n = self.normal_vector

        return basePointDiff.isOrthoganal(n)

    def intersection(self, other):
        try:
            A, B = self.normal_vector.coordinates
            C, D = other.normal_vector.coordinates
            k1 = self.constant_term
            k2 = other.constant_term

            x_coord = D * k1 - B * k2
            y_coord = C * k1 + A * k2

            one_over_denom = Decimal('1')(A * D - B * C)

            return Vector([x_coord, y_coord]).scalar_mult(one_over_denom)

        except ZeroDivisionError:
            if self == other:
                return self
            else:
                return None

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


l1 = Line(normal_vector=Vector(['4.046', '2.83']), constant_term='1.21')
l2 = Line(normal_vector=Vector(['10.115', '7.09']),  constant_term='3.025')

# l3 = Line(normal_vector=Vector([7.204, 3.182]),  constant_term='8.68')
# l4 = Line(normal_vector=Vector([8.172, 4.114]),  constant_term='9.883')
#
# l5 = Line(normal_vector=Vector([1.182, 5.562]),  constant_term='6.744')
# l6 = Line(normal_vector=Vector([1.773, 8.334]),  constant_term='9.525')

print(l1.intersection(l2))
# print(l3.intersection(l4))
# print(l5.intersection(l6))

