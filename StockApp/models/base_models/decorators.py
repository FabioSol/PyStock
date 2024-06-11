from StockApp.models.base_models import ERR, N_MAX,N_MIN,N_START
from typing import Callable,Union

def variable_operation(func):
    def wrapper(item_1, item_2):
        def perform_operation(self, other,
                              operation_fun: Callable[[Union[int, float], Union[int, float]], Union[int, float]]):
            if isinstance(other, Union[int, float]):
                return self.bind(lambda x: operation_fun(x, other))
            elif isinstance(other, type(self)):
                return self.bind(lambda x: operation_fun(x, other.func(x)))
            else:
                raise TypeError(f"Unsupported operation for {type(self)} and {type(other)}")

        return perform_operation(self=item_1, other=item_2, operation_fun=func)

    return wrapper

def distribution_operation(op_symbol):
    def decorator(func):
        def wrapper(item_1, item_2):
            def perform_operation(self, other,
                                  operation_symbol: str,
                                  operation_fun: Callable[[Union[int, float, bool], Union[int, float, bool]],
                                  Union[int, float, bool]]):

                if isinstance(other, (int, float, bool)):
                    new_variable = self.copy()
                    new_variable.operations += [f"{operation_symbol}{other}"]
                    new_variable = new_variable.bind(lambda x: operation_fun(x, other))
                    return new_variable

                elif isinstance(other, type(self)):
                    new_variable = self.copy()
                    new_variable.kwargs = {f"{self.name}_1": self.kwargs, f"{other.name}_2": other.kwargs}
                    new_variable.operations = [self.operations, operation_symbol, other.operations]
                    new_variable.name = f"{self.name}_{operation_symbol}_{other.name}"
                    new_variable.generator_f = lambda: operation_fun(self.generator_f(), other.generator_f())
                    return new_variable

                else:
                    raise TypeError(f"Unsupported operation: {type(self)} {operation_symbol} {type(other)}")


            result = perform_operation(self=item_1, other=item_2, operation_symbol=op_symbol, operation_fun=func)

            return result

        return wrapper

    return decorator



def series_operation(func):
    def wrapper(item_1, item_2):
        def perform_operation(self, other, operation):
            if isinstance(other, (int, float)):
                new = self.copy()
                new.data = [operation(val, other) for val in self.data]
                return new.clean()
            elif isinstance(other, type(self)):
                new = self.copy()
                new.t = list(set(self.t) | set(other.t))
                new.data = [operation(self[i], other[i]) for i in new.t]
                return new.clean()
            else:
                raise TypeError(f"Unsupported operation for {type(self)} and {type(other)}")

        return perform_operation(item_1, item_2, func)

    return wrapper

def handle_none(func):
    def wrapper(self, other):
        if (other is None) | (self is None):
            return None
        else:
            return func(self, other)
    return wrapper

def handle_division(func):
    def wrapper(self, other):
        if other == 0:
            if self > 0:
                return float('inf')
            elif self < 0:
                return float('-inf')
            else:
                return None
        else:
            return func(self, other)

    return wrapper


def handle_rdivision(func):
    def wrapper(self, other):
        if self == 0:
            if other > 0:
                return float('inf')
            elif other < 0:
                return float('-inf')
            else:
                return None
        else:
            return func(self, other)

    return wrapper

def efficient_montecarlo_approximation(func, n_start: int = N_START):
    def wrapper(self, *args, **kwargs):
        n = n_start
        f1, f2 = func(self, *args, **kwargs)
        values = self.generate(n)
        metric = f1(values)
        mean = sum(values) / n
        n += 1
        values += self.generate(1)
        new_mean = sum(values) / n
        mse = (new_mean - mean) ** 2
        while ((mse > ERR) | (n < (n_start + N_MIN))) & (n < N_MAX):
            n += 1
            new_metric, new_mean = f2(metric, mean, n)
            mse = (mse * n + (new_mean - mean) ** 2) / (n + 1)
            metric, mean = new_metric, new_mean
        return metric

    return wrapper