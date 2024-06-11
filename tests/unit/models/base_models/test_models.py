import unittest
from StockApp.models.base_models.model import Model
from StockApp.models.base_models.series import Series
from StockApp.models.base_models.distribution import Distribution
from StockApp.models.base_models.variable import Variable

class TestClassMethods(unittest.TestCase):
    def test_from_variable(self):
        variable = Variable(lambda x: x)
        model = Model.from_variable(variable)
        result = model.func(1)
        self.assertEqual(result, 1)

    def test_from_distribution(self):
        distribution = Distribution.normal(1,0)
        model = Model.from_distribution(distribution)
        result = model.func(1)
        self.assertEqual(result, 1)

    def test_from_series(self):
        series = Series.from_list([i**2 for i in range (10)])
        model = Model.from_series(series)
        result = model.func(3)
        self.assertEqual(result, 9)

class TestInteractions(unittest.TestCase):
    def test_var_model_add(self):
        variable = Variable(lambda x: x)
        model_1 = Model.from_variable(variable)
        distribution = Distribution.normal(2,0)
        series = Series.from_list([i*3 for i in range (10)])
        model_2 = 13 + model_1 + distribution + series
        model_a = model_1 + model_2

        model_3 = 13 + model_1 + distribution + series
        model_b = model_1 + model_3

        result_a = model_a.func(1, 1, 2, 8 / 3)
        result_b = model_b.func(1, 1, 2, 8 / 3)
        self.assertEqual(result_a, result_b)

    def test_var_model_sub(self):
        variable = Variable(lambda x: x)
        model_1 = Model.from_variable(variable)
        distribution = Distribution.normal(2,0)
        series = Series.from_list([i*3 for i in range (10)])
        model_2 = 13 - model_1 - distribution - series
        model_a = model_1 - model_2

        model_3 = 13 - model_1 -distribution- series
        model_b = model_1 - model_3

        result_a = model_a.func(1, 1, 2, 8 / 3)
        result_b = model_b.func(1, 1, 2, 8 / 3)
        self.assertEqual(result_a, result_b)

    def test_var_model_mul(self):
        variable = Variable(lambda x: x)
        model_1 = Model.from_variable(variable)
        distribution = Distribution.normal(2,0)
        series = Series.from_list([i*3 for i in range (10)])
        model_2 = 13 * model_1 * distribution * series
        model_a = model_1 * model_2

        model_3 = 13 *  model_1 *distribution * series
        model_b = model_1 * model_3

        result_a = model_a.func(1, 1, 2, 8 / 3)
        result_b = model_b.func(1, 1, 2, 8 / 3)
        self.assertEqual(result_a, result_b)

    def test_var_model_div(self):
        variable = Variable(lambda x: x)
        model_1 = Model.from_variable(variable)
        distribution = Distribution.normal(2,0)
        series = Series.from_list([i*3 for i in range (10)])
        model_2 = 13 / model_1 / distribution / series
        model_a = model_1 / model_2

        model_3 = 13 / model_1 / distribution / series
        model_b = model_1 / model_3

        result_a = model_a.func(1, 1, 2, 8 / 3)
        result_b = model_b.func(1, 1, 2, 8 / 3)
        self.assertEqual(result_a, result_b)

