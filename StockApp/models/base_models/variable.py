from typing import Union, Callable
from StockApp.models.base_models.decorators import handle_division, handle_rdivision, variable_operation


class Variable:
    def __init__(self, func):
        self.func = func

    def bind(self, func):
        return Variable(lambda x: func(self.func(x)))

    @variable_operation
    def __add__(self, other):
        return self + other

    @variable_operation
    def __radd__(self, other):
        return other + self

    @variable_operation
    def __sub__(self, other):
        return self - other

    @variable_operation
    def __rsub__(self, other):
        return other - self

    @variable_operation
    def __mul__(self, other):
        return self * other

    @variable_operation
    def __rmul__(self, other):
        return other * self

    @handle_division
    @variable_operation
    def __truediv__(self, other):
        return self / other

    @handle_rdivision
    @variable_operation
    def __rtruediv__(self, other):
        return other / self

    @handle_division
    @variable_operation
    def __floordiv__(self, other):
        return self // other

    @handle_rdivision
    @variable_operation
    def __rfloordiv__(self, other):
        return other // self

    @variable_operation
    def __pow__(self, other):
        return self ** other

    @variable_operation
    def __rpow__(self, other):
        return other ** self

    @variable_operation
    def __mod__(self, other):
        return self % other

    @variable_operation
    def __rmod__(self, other):
        return other % self

    def deriv(self):
        delta = 1e-6
        return Variable(lambda x: (self.func(x + delta) - self.func(x - delta)) / (2 * delta))

    def limit_integ(self, a: float = 0, b: float = 1, n: int = 1000):
        h = (b - a) / n
        integral = 0.5 * (self.func(a) + self.func(b))
        for i in range(1, n):
            integral += self.func(a + i * h)
        integral *= h
        return integral

    def integ(self):
        return Variable(lambda x: self.limit_integ(a=0, b=x))




"""v1 = Variable(lambda x: x ** 2)
v2 = v1.bind(lambda x: x ** (1 / 2)) + v1
print(v1.func(4))
v3 = v1.deriv().integ()
print(v2.func(4))
print(v3.func(-5))"""
