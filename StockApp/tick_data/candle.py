import pandas as pd
import matplotlib.pyplot as plt


class Candle:
    def __init__(self, data: list):
        self.open = data[0]
        self.high = max(data)
        self.low = min(data)
        self.close = data[-1]




