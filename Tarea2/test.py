from fixed_point_method import fixed_point_method
import os, sys
from punto_fijo import read
from validators import validate_input_file, validate_tolerance, validate_max_iterations
import unittest

class TestMethods(unittest.TestCase):

    def test_fixed_point_method1(self):
        # Test (x**2-6)/12 which should converge with x_0 = 1
        initial_point = 1
        tol = 1e-6
        num_iter = 100
        converges, iterations = fixed_point_method('(x**2-6)/12', initial_point, tol, num_iter)
        self.assertEqual(converges, True)
        self.assertEqual(len(iterations) < 100, True)
        self.assertEqual(iterations[-1]['error'] < tol, True)

    def test_fixed_point_method2(self):
        # Test x**3 which should converge with x_0 = 0.5
        initial_point = 0.5
        tol = 1e-6
        num_iter = 100
        converges, iterations = fixed_point_method('(x**3)', initial_point, tol, num_iter)
        self.assertEqual(converges, True)
        self.assertEqual(len(iterations) < 100, True)
        self.assertEqual(iterations[-1]['error'] < tol, True)


    def test_fixed_point_method3(self):
        # Test sin(x) which should diverge with x_0 = 1 in 100 iter.
        initial_point = 1
        tol = 1e-6
        num_iter = 100
        converges, iterations = fixed_point_method('(math.sin(x))', initial_point, tol, num_iter)
        self.assertEqual(converges, False)
        self.assertEqual(len(iterations) < 100, False)
        self.assertEqual(iterations[-1]['error'] < tol, False)

    def test_input_data(self):
        # Test input data matches expected format
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/tests/prueba1.txt'
        expected = [{'name': 'func1', 'expr': 'x**2', 'p0': 2.0}]  # match actual format
        self.assertEqual(read(dir_path), expected)

class TestValidators(unittest.TestCase):
    def setUp(self):
        # Create test files
        with open("test.txt", "w") as f:
            f.write("test")
    
    def tearDown(self):
        # Clean up test files
        if os.path.exists("test.txt"):
            os.remove("test.txt")

    def test_validate_input_file(self):
        with self.assertRaises(ValueError):
            validate_input_file("test.tex")
        with self.assertRaises(FileNotFoundError):
            validate_input_file("nonexistent.txt")
    
    def test_validate_tolerance(self):
        self.assertEqual(validate_tolerance("0.001"), 0.001)
        with self.assertRaises(ValueError):
            validate_tolerance("invalid")
        with self.assertRaises(ValueError):
            validate_tolerance("-1.0")
    
    def test_validate_max_iterations(self):
        self.assertEqual(validate_max_iterations("100"), 100)
        with self.assertRaises(ValueError):
            validate_max_iterations("invalid")
        with self.assertRaises(ValueError):
            validate_max_iterations("-10")

class TestConvergenceRate(unittest.TestCase):
    def test_calculate_convergence_rate(self):
        from punto_fijo import calculate_convergence_rate
        
        # Test with empty list
        self.assertEqual(calculate_convergence_rate([]), 0)
        
        # Test with one error
        self.assertEqual(calculate_convergence_rate([0.1]), 0)
        
        # Test with multiple errors
        errors = [0.1, 0.01, 0.001]
        rate = calculate_convergence_rate(errors)
        self.assertAlmostEqual(rate, 0.1, places=2)

if __name__ == '__main__':
    unittest.main()