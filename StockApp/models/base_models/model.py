from StockApp.models.base_models.distribution import Distribution
from StockApp.models.base_models.variable import Variable
from StockApp.models.base_models.series import Series
from StockApp.models.base_models.decorators import handle_division, handle_rdivision
from typing import Union, Callable
from inspect import signature
import random
import matplotlib.pyplot as plt


def model_operation(func):
    def wrapper(item_1, item_2):
        def perform_operation(self, other,
                              operation_fun: Callable[[Union[int, float], Union[int, float]], Union[int, float]]):
            if isinstance(other, (int, float, bool)):
                return self.bind(lambda x: operation_fun(x, other))
            elif isinstance(other, Distribution):
                return self.bind(lambda x, y: operation_fun(x, other.generator_f()))
            elif isinstance(other, Variable):
                return self.bind(lambda x, y: operation_fun(x, other.func(y)))
            elif isinstance(other, Series):
                return self.bind(lambda x, y: operation_fun(x, other[y]))
            elif isinstance(other, Model):
                return Model(lambda *args: operation_fun(self.func(*args[:self.parameters]),
                                                         other.func(*args[-other.parameters:])),
                             self.parameters + other.parameters)
            else:
                raise TypeError(f"Unsupported operation for {type(self)} and {type(other)}")

        return perform_operation(self=item_1, other=item_2, operation_fun=func)

    return wrapper


class Model:
    def __init__(self, func = lambda x : 0, parameters: int = 0):
        self.func = func
        self.parameters = parameters

    def bind(self, func):
        return Model(lambda *args: func(self.func(*args[:self.parameters]), *args[self.parameters:]),
                     self.parameters+len(signature(func).parameters)-1)

    @model_operation
    def __add__(self, other):
        return self + other

    @model_operation
    def __radd__(self, other):
        return other + self

    @model_operation
    def __sub__(self, other):
        return self - other

    @model_operation
    def __rsub__(self, other):
        return other - self

    @model_operation
    def __mul__(self, other):
        return self * other

    @model_operation
    def __rmul__(self, other):
        return other * self


    @model_operation
    @handle_division
    def __truediv__(self, other):
        return self / other


    @model_operation
    @handle_rdivision
    def __rtruediv__(self, other):
        return other / self

    @model_operation
    @handle_division
    def __floordiv__(self, other):
        return self // other

    @model_operation
    @handle_rdivision
    def __rfloordiv__(self, other):
        return other // self

    @model_operation
    def __pow__(self, other):
        return self ** other

    @model_operation
    def __rpow__(self, other):
        return other ** self

    @model_operation
    def __mod__(self, other):
        return self % other

    @model_operation
    def __rmod__(self, other):
        return other % self

    @classmethod
    def from_variable(cls, variable: Variable):
        return Model(variable.func, 1)

    @classmethod
    def from_distribution(cls, distribution: Distribution):
        return Model(lambda x: distribution.generator_f(), 1)

    @classmethod
    def from_series(cls, series:Series):
        return Model(series.__getitem__, 1)

    def map(self, iterable):
        y = []
        if self.parameters > 1:
            for i in iterable:
                try:
                    y += [self.func(*i)]
                except TypeError:
                    pass
        elif self.parameters == 1:
            for i in iterable:
                try:
                    y += [self.func(i)]
                except TypeError:
                    pass
        elif self.parameters == 0:
            for i in iterable:
                try:
                    y += [self.func(*i)]
                except TypeError:
                    pass

        return y

    def to_one_var(self):
        return Model(lambda x: self.func(tuple([x for _ in range(self.parameters)])),1)

    def plot(self, start=0, stop=10, step=1):
        x = [i for i in range(start,stop,step)]
        y = [self.func(i) for i in x]
        plt.plot(x,y)
        plt.show()


