import unittest
from StockApp.models.base_models.distribution import Distribution
import random


class TestClassMethods(unittest.TestCase):
    def test_none_method(self):
        n = 5
        instance = Distribution.none_dist()
        result = instance.generate(n)
        self.assertEqual(result, [0]*n)

    def test_uniform_int_method(self):
        n=5
        instance = Distribution.uniform_int(1,1)
        result = instance.generate(n)
        self.assertEqual(result, [1] * n)
        self.assertIsInstance(result[0],int)

    def test_uniform_float_method(self):
        n=5
        instance = Distribution.uniform_float(1,1)
        result = instance.generate(n)
        self.assertEqual(result, [1.0] * n)
        self.assertIsInstance(result[0],float)

    def test_normal_method(self):
        n=5
        instance = Distribution.normal(1,0)
        result = instance.generate(n)
        self.assertEqual(result, [1] * n)

    def test_exponential_method(self):
        instance = Distribution.exponential(-100000)
        result = instance.generator_f()
        self.assertAlmostEquals(result, 0, 1)

    def test_beta_method(self):
        instance = Distribution.beta(.1,1000)
        result = instance.generator_f()
        self.assertAlmostEquals(result, 0, 1)

    def test_gamma_method(self):
        instance = Distribution.gamma(1, .00001)
        result = instance.generator_f()
        self.assertAlmostEquals(result, 0, 1)

    def test_triangular_method(self):
        instance = Distribution.triangular(1, 1, 1)
        result = instance.generator_f()
        self.assertEqual(result, 1, 1)

    def test_weibull_method(self):
        instance = Distribution.weibull(.00001, 1)
        result = instance.generator_f()
        self.assertAlmostEquals(result, 0, -1)

    def test_from_generator_method(self):
        instance = Distribution.from_generator_f(lambda: random.randint(1,1))
        result = instance.generator_f()
        self.assertEqual(result, 1, 1)

    def test_constant_class_method(self):
        value = 5
        n=5
        instance = Distribution.constant(value)
        result = instance.generate(n)
        self.assertEqual(result,[value]*n)


class TestBinaryOperators(unittest.TestCase):
    def test_add_same(self):
        instance_1 = Distribution.normal(1, 0)
        instance_2 = Distribution.normal(1, 0)
        instance = instance_1 + instance_2
        value = instance.generator_f()
        self.assertEqual(value, 2)

    def test_radd_int(self):
        instance_1 = Distribution.normal(1, 0)
        instance = 4 + instance_1
        value = instance.generator_f()
        self.assertEqual(value, 5)

    def test_sub_same(self):
        instance_1 = Distribution.normal(1, 0)
        instance_2 = Distribution.normal(1, 0)
        instance = instance_1 - instance_2
        value = instance.generator_f()
        self.assertEqual(value, 0)

    def test_rsub_int(self):
        instance_1 = Distribution.normal(1, 0)
        instance = 3-instance_1
        value = instance.generator_f()
        self.assertEqual(value, 2)

    def test_mul_same(self):
        instance_1 = Distribution.normal(1, 0)
        instance_2 = Distribution.normal(1, 0)
        instance = instance_1 * instance_2
        value = instance.generator_f()
        self.assertEqual(value, 1)

    def test_rmul_int(self):
        instance_1 = Distribution.normal(1, 0)
        instance = 3*instance_1
        value = instance.generator_f()
        self.assertEqual(value, 3)

    def test_div_same(self):
        instance_1 = Distribution.normal(8, 0)
        instance_2 = Distribution.normal(2, 0)
        instance = instance_1 / instance_2
        value = instance.generator_f()
        self.assertEqual(value, 4)

    def test_rdiv_int(self):
        instance_1 = Distribution.normal(2, 0)
        instance = 10/instance_1
        value = instance.generator_f()
        self.assertEqual(value, 5)

    def test_floor_div_same(self):
        instance_1 = Distribution.normal(8.5, 0)
        instance_2 = Distribution.normal(2, 0)
        instance = instance_1 // instance_2
        value = instance.generator_f()
        self.assertEqual(value, 4)

    def test_r_floor_div_int(self):
        instance_1 = Distribution.normal(2, 0)
        instance = 11 // instance_1
        value = instance.generator_f()
        self.assertEqual(value, 5)

    def test_mod_same(self):
        instance_1 = Distribution.normal(8.5, 0)
        instance_2 = Distribution.normal(2, 0)
        instance = instance_1 % instance_2
        value = instance.generator_f()
        self.assertEqual(value, .5)

    def test_r_mod_int(self):
        instance_1 = Distribution.normal(2, 0)
        instance = 11 % instance_1
        value = instance.generator_f()
        self.assertEqual(value, 1)

    def test_lt_same(self):
        instance_1 = Distribution.normal(2, 0)
        instance_2 = Distribution.normal(3, 0)
        instance = instance_1 < instance_2
        value = instance.generator_f()
        self.assertTrue(value)

    def test_r_lt_int(self):
        instance_1 = Distribution.normal(2, 0)
        instance = 1 < instance_1
        value = instance.generator_f()
        self.assertTrue(value)

    def test_gt_same(self):
        instance_1 = Distribution.normal(4, 0)
        instance_2 = Distribution.normal(3, 0)
        instance = instance_1 > instance_2
        value = instance.generator_f()
        self.assertTrue(value)

    def test_r_gt_int(self):
        instance_1 = Distribution.normal(0, 0)
        instance = 1 > instance_1
        value = instance.generator_f()
        self.assertTrue(value)

    def test_or_same(self):
        instance_1 = Distribution.normal(4, 0) < 4
        instance_2 = Distribution.normal(3, 0) <= 3
        instance = instance_1 | instance_2
        value = instance.generator_f()
        self.assertTrue(value)

    def test_and_same(self):
        instance_1 = Distribution.normal(4, 0) < 4
        instance_2 = Distribution.normal(3, 0) <= 3
        instance = instance_1 & instance_2
        value = instance.generator_f()
        self.assertFalse(value)


class TestMethods(unittest.TestCase):
    def test_mean(self):
        instance_1 = Distribution.normal(4, .1)
        instance_2 = Distribution.normal(3, .1)
        instance = instance_1 + instance_2
        value = instance.mean
        self.assertAlmostEquals(value, 7, 1)

    def test_sd(self):
        instance_1 = Distribution.normal(4, 4)
        instance_2 = Distribution.normal(3, 3)
        instance = instance_1 + instance_2
        value = instance.std_dev
        self.assertAlmostEquals(value, 5, 0)

    def test_p(self):
        instance = Distribution.normal(0, 1)
        value = instance.p(0)
        self.assertAlmostEquals(value, .5, 1)

    def test_q(self):
        instance = Distribution.normal(0, .1)
        value = instance.q(0.5)
        self.assertAlmostEquals(value, 0, 1)



