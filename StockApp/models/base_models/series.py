from types import NoneType
import math
from StockApp.models.base_models.decorators import handle_division, handle_rdivision, handle_none, series_operation


class Series:
    def __init__(self, data: list, t: list = None):
        if t is None:
            t = list(range(len(data)))

        sorted_data, sorted_t = zip(*sorted(zip(data, t), key=lambda x: x[1]))
        self.data = list(sorted_data)
        self.t = list(sorted_t)
        self.clean()

    def __str__(self):

        n = max([len(str(max(self.t))), max([len(str(i)) for i in self.data])]) + 4
        string = f"|{'t':^{n - 1}}|{'data':^{n}}| \n"
        for t, d in self:
            if d is None:
                d = 'None'
            string += f"| {t:<{n - 2}}|{d:{n}}|\n"
        return string

    def __repr__(self):
        return str(self.t) + "\n" + str(self.data)

    def __getitem__(self, index):
        try:
            t_index = self.t.index(index)  # Find the position of index in t
            return self.data[t_index]  # Access element in data using the position in t
        except ValueError:
            return self.interpolate(index)

    def __delitem__(self, index):
        try:
            t_index = self.t.index(index)  # Find the position of index in t
            del self.t[t_index]  # Remove index from self.t
            del self.data[t_index]  # Remove corresponding element from self.data
        except ValueError:
            pass

    def __iter__(self):
        return iter(zip(self.t, self.data))

    def __neg__(self):
        new = self.copy()
        new.data = [-val for val in self.data]
        return new

    @series_operation
    @handle_none
    def __add__(self, other):
        return self + other

    @series_operation
    @handle_none
    def __radd__(self, other):
        return other + self

    @series_operation
    @handle_none
    def __sub__(self, other):
        return self - other

    def __rsub__(self, other):
        return self.__neg__().__add__(other)

    @series_operation
    @handle_none
    def __mul__(self, other):
        return self * other

    def __rmul__(self, other):
        return self.__mul__(other)

    @series_operation
    @handle_division
    @handle_none
    def __truediv__(self, other):
        return self / other

    @series_operation
    @handle_rdivision
    @handle_none
    def __rtruediv__(self, other):
        return other / self

    @series_operation
    @handle_division
    @handle_none
    def __floordiv__(self, other):
        return self // other

    @series_operation
    @handle_rdivision
    @handle_none
    def __rfloordiv__(self, other):
        return other // self

    @series_operation
    @handle_none
    def __pow__(self, other):
        return self ** other

    @series_operation
    @handle_none
    def __rpow__(self, other):
        return other ** self

    @series_operation
    @handle_none
    def __mod__(self, other):
        return self % other

    @series_operation
    @handle_none
    def __rmod__(self, other):
        return other % self

    def copy(self):
        return Series(self.data.copy(), self.t.copy())

    def clean(self):
        t_to_del = []
        for t, val in self:
            if isinstance(val, NoneType):
                t_to_del += [t]
        for t in t_to_del[::-1]:
            del self[t]

        return self

    @classmethod
    def from_list(cls, values: list):
        if not isinstance(values, (list, tuple)):
            raise TypeError("Input should be a list or tuple.")
        if len(values) == 0:
            raise ValueError("Input list should have at least one element.")

        first_element = values[0]
        if isinstance(first_element, (int, float, bool)):
            data = values
            t = list(range(len(values)))
        elif isinstance(first_element, tuple) and len(first_element) == 2:
            t, data = zip(*values)
            if any(not isinstance(i, int) for i in t):
                raise TypeError("The elements in t (first in tuple) should be integers.")
            if len(set(t)) != len(t):
                raise ValueError("The elements of t should be unique.")
        else:
            raise TypeError("Unsupported type of elements in values or tuple length is not 2.")

        return cls(list(data), list(t))

    def interpolate_intervals(self):
        deltas_x = [self.t[i+1]-self.t[i] for i in range(len(self.t)-1)]
        if all(x == deltas_x[0] for x in deltas_x):
            return self
        else:
            def find_gcd(numbers):
                result = numbers[0]
                for num in numbers[1:]:
                    result = math.gcd(result, num)
                return result
            gdc = find_gcd(deltas_x)
            new_t = list(range(self.t[0], self.t[-1]+gdc, gdc))
            new_data = [self[i] for i in new_t]
            for i,(x,y) in enumerate(zip(new_t,new_data)):
                if y is None:
                    new_data[i] = self.interpolate(x)
            return Series.from_list(list(zip(new_t,new_data)))


    def interpolate(self, t):
        n = len(self.t)
        result = 0.0

        for i in range(n):
            term = self.data[i]
            for j in range(n):
                if j != i:
                    term = term * (t - self.t[j]) / (self.t[i] - self.t[j])
            result += term

        return result




"""

l = [1,2,3,4,5,6]
lt = [(2, 3), (4, 5), (8, 13),(12,55)]
s = Series.from_list(l)
st = Series.from_list(lt)
st1 = 1%st%s
print(st.interpolate_intervals())"""
