from fixed_point_method import fixed_point_method
import os, sys
from punto_fijo import read
import unittest

class TestMethods(unittest.TestCase):

    def test_fixed_point_method1(self):
        initial_point = 1
        tol = 1e-6
        num_iter = 100
        converges, iterations = fixed_point_method('(x**2-6)/12', initial_point, tol, num_iter)
        self.assertEqual(converges, True)
        self.assertEqual(len(iterations) < 100, True)
        self.assertEqual(iterations[-1]['error'] < tol, True)

    def test_fixed_point_method2(self):
        initial_point = 0.5
        tol = 1e-6
        num_iter = 100
        converges, iterations = fixed_point_method('(x**3)', initial_point, tol, num_iter)
        self.assertEqual(converges, True)
        self.assertEqual(len(iterations) < 100, True)
        self.assertEqual(iterations[-1]['error'] < tol, True)


    def test_fixed_point_method3(self):
        initial_point = 1
        tol = 1e-6
        num_iter = 100
        converges, iterations = fixed_point_method('(math.sin(x))', initial_point, tol, num_iter)
        self.assertEqual(converges, False)
        self.assertEqual(len(iterations) < 100, False)
        self.assertEqual(iterations[-1]['error'] < tol, False)

    def test_input_data(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/tests/prueba1.txt'
        self.assertEqual(read(dir_path), [{'expr': 'x**2', 'name': 'func1', 'p0': 2.0}])


if __name__ == '__main__':
    unittest.main()