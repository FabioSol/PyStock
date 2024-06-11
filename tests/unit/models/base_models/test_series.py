import unittest
from StockApp.models.base_models.series import Series

class TestClassMethods(unittest.TestCase):
    def test_from_list(self):
        list_a = [i*2 for i in range(10)] + [None]
        instance_b = Series.from_list(list_a)

        list_b = [(i, i*2) for i in range(10)]
        instance_a = Series.from_list(list_b)
        self.assertEqual(instance_a.data, instance_b.data)
        self.assertEqual(instance_a.t, instance_b.t)

