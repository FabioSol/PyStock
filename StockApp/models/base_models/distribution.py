import random
from typing import Callable, Union
from StockApp.models.base_models.decorators import handle_division,handle_rdivision, efficient_montecarlo_approximation, distribution_operation
from StockApp.models.base_models import N_START





class Distribution:
    DISTRIBUTION_FUNCTIONS = {
        'none': lambda: 0,
        'uniform_int': random.randint,
        'uniform_float': random.uniform,
        'normal': random.gauss,
        'exponential': random.expovariate,
        'beta': random.betavariate,
        'gamma': random.gammavariate,
        'triangular': random.triangular,
        'weibull': random.weibullvariate,
    }

    def __init__(self, name: str, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.operations = list()
        self.generator_f = self.make_generator_f()

    def bind(self, func: Callable[[Union[int, float, bool]], Union[int, float, bool]]) -> 'Distribution':
        new_dist = self.copy()
        new_dist.generator_f = lambda: func(self.generator_f())
        return new_dist

    def copy(self):
        new_variable = Distribution.none_dist()
        new_variable.name = self.name
        new_variable.args = self.args
        new_variable.kwargs = self.kwargs.copy()
        new_variable.operations = self.operations.copy()
        new_variable.generator_f = self.generator_f
        return new_variable

    def generator(self, n: int):
        if n > 0:
            for _ in range(n):
                yield self.generator_f()
        else:
            raise ValueError(f"Expected a positive integer, got {n} instead")

    def generate(self, n: int = 1) -> list:
        return [value for value in self.generator(n)]

    def make_generator_f(self) -> Callable[[], Union[int, float, bool]]:
        if self.name in Distribution.DISTRIBUTION_FUNCTIONS:
            random.seed = random.seed
            random_function = Distribution.DISTRIBUTION_FUNCTIONS[self.name]
            return lambda: random_function(*self.args, **self.kwargs)
        else:
            raise ValueError(f"Unsupported distribution: {self.name}")

    @classmethod
    def none_dist(cls) -> 'Distribution':
        return cls("none")

    @classmethod
    def uniform_int(cls, a: int, b: int) -> 'Distribution':
        return cls('uniform_int', a=a, b=b)

    @classmethod
    def uniform_float(cls, a: float, b: float) -> 'Distribution':
        return cls('uniform_float', a=a, b=b)

    @classmethod
    def normal(cls, mean: float, stddev: float) -> 'Distribution':
        return cls('normal', mu=mean, sigma=stddev)

    @classmethod
    def exponential(cls, param_lambda: float) -> 'Distribution':
        return cls('exponential', lambd=param_lambda)

    @classmethod
    def beta(cls, alpha: float, beta: float) -> 'Distribution':
        return cls('beta', alpha=alpha, beta=beta)

    @classmethod
    def gamma(cls, alpha: float, beta: float) -> 'Distribution':
        return cls('gamma', alpha=alpha, beta=beta)

    @classmethod
    def triangular(cls, low: float, high: float, mode: float) -> 'Distribution':
        return cls('triangular', low=low, high=high, mode=mode)

    @classmethod
    def weibull(cls, alpha: float, beta: float) -> 'Distribution':
        return cls('weibull', alpha=alpha, beta=beta)

    @classmethod
    def from_generator_f(cls, generator_f: Callable[[], Union[int, float, bool]],
                         name: str = "custom") -> 'Distribution':
        distribution = cls('none')
        distribution.name = name
        distribution.generator_f = generator_f
        return distribution

    @classmethod
    def constant(cls, value: Union[int, float]):
        return cls.from_generator_f(generator_f=lambda: value, name=f"Constant")

    def __repr__(self):
        return "Distribution"

    def __str__(self):
        return f"{self.__repr__()} \n Name: {self.name} \n  Parameters: {self.kwargs} \n  Operations: {self.operations}"

    @distribution_operation("+")
    def __add__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self + other

    @distribution_operation("+")
    def __radd__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return other + self

    @distribution_operation("-")
    def __sub__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self - other

    @distribution_operation("-r")
    def __rsub__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return other - self

    @distribution_operation("*")
    def __mul__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self * other

    @distribution_operation("*")
    def __rmul__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return other * self

    @distribution_operation("/")
    @handle_division
    def __truediv__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self / other

    @distribution_operation("/r")
    @handle_rdivision
    def __rtruediv__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return other / self

    @distribution_operation("//")
    @handle_division
    def __floordiv__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self // other

    @distribution_operation("//r")
    @handle_rdivision
    def __rfloordiv__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return other // self

    @distribution_operation("**")
    def __pow__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self ** other

    @distribution_operation("**r")
    def __rpow__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return other ** self

    @distribution_operation("%")
    def __mod__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self % other

    @distribution_operation("%r")
    def __rmod__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return other % self

    @distribution_operation("<")
    def __lt__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self < other

    @distribution_operation(">")
    def __gt__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self > other

    @distribution_operation("<=")
    def __le__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self <= other

    @distribution_operation(">=")
    def __ge__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self >= other

    @distribution_operation("!=")
    def __ne__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self != other

    @distribution_operation("==")
    def __eq__(self, other: Union[int, float, 'Distribution']) -> 'Distribution':
        return self == other

    @distribution_operation("|")
    def __or__(self, other: Union[bool, 'Distribution']) -> 'Distribution':
        return self | other

    @distribution_operation("|r")
    def __ror__(self, other: Union[bool, 'Distribution']) -> 'Distribution':
        return other | self

    @distribution_operation("&")
    def __and__(self, other: Union[bool, 'Distribution']):
        return self & other

    @distribution_operation("&r")
    def __rand__(self, other: Union[bool, 'Distribution']):
        return other & self

    @property
    @efficient_montecarlo_approximation
    def mean(self):
        def f1(values):
            return sum(values) / len(values)

        def f2(past_metric, past_mean, n):
            new_value = self.generator_f()
            new_mean = (past_mean * n + new_value) / (n + 1)
            new_metric = (past_metric * n + new_value) / (n + 1)
            return new_metric, new_mean

        return f1, f2

    @property
    @efficient_montecarlo_approximation
    def variance(self):
        def f1(values):
            mean = sum(values) / len(values)
            return sum([(val - mean) ** 2 for val in values]) / (len(values) - 1)

        def f2(past_metric, past_mean, n):
            new_value = self.generator_f()
            new_mean = (past_mean * n + new_value) / (n + 1)
            new_metric = (((((past_metric * (n - 1)) / n) ** (1 / 2) + past_mean - new_mean) ** 2 * n + (
                    new_value - new_mean) ** 2) / n)
            return new_metric, new_mean

        return f1, f2

    @property
    def std_dev(self):
        return self.variance ** (1 / 2)

    @efficient_montecarlo_approximation
    def p(self, q: float):
        def f1(values):
            return sum([val <= q for val in values]) / len(values)

        def f2(past_metric, past_mean, n):
            new_value = self.generator_f()
            new_mean = (past_mean * n + new_value) / (n + 1)
            new_metric = (past_metric * n + int(new_value <= q)) / (n + 1)
            return new_metric, new_mean

        return f1, f2

    def q(self, p: float):
        n = N_START
        values = self.generate(n)
        values.sort()
        return values[int(n * p)]


