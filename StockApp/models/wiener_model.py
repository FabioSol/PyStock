from StockApp.models.base_models.model import Model
from StockApp.models.base_models.distribution import Distribution
import matplotlib.pyplot as plt


class WienerModel(Model):
    def __init__(self):
        func = Model.from_distribution(Distribution.normal(0, 1)).func
        super().__init__(func, 1)

    def process(self, n):
        for i in range(n):
            if i == 0:
                value = 0
            else:
                value = self.func(i)
                self.func = Model.from_distribution(Distribution.normal(value, 1)).func
            yield value
        self.func=Model.from_distribution(Distribution.normal(0, 1)).func

    def plot(self, start=0, stop=10, step=1):
        x = [i for i in range(start, stop, step)]
        y = list(self.process(len(x)))
        plt.plot(x, y)
        plt.show()


m=WienerModel()
m.plot(0,100)
