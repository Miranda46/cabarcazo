import numpy as np
from scipy.interpolate import CubicSpline
from cubic_spline_interpolation import cubic_spline, evaluate_spline, cubic_spline_derivative, evaluate_spline_derivative
import pytest

def test_simple_polynomial():
    # Test cubic polynomial x^3
    x = np.array([0, 0.5, 1])
    y = x**3
    
    # Our implementation
    coeffs = cubic_spline(x, y, bc_type='clamped')
    x_eval = np.linspace(0, 1, 100)
    our_result = evaluate_spline(x_eval, x, coeffs)
    
    # SciPy implementation
    cs = CubicSpline(x, y, bc_type='clamped')
    scipy_result = cs(x_eval)
    
    np.testing.assert_allclose(our_result, scipy_result, rtol=1e-7)

def test_sinusoidal():
    # Test sin(x) interpolation
    x = np.linspace(0, 2*np.pi, 10)
    y = np.sin(x)
    
    # Our implementation
    coeffs = cubic_spline(x, y, bc_type='natural')
    x_eval = np.linspace(0, 2*np.pi, 100)
    our_result = evaluate_spline(x_eval, x, coeffs)
    
    # SciPy implementation
    cs = CubicSpline(x, y, bc_type='natural')
    scipy_result = cs(x_eval)
    
    np.testing.assert_allclose(our_result, scipy_result, rtol=1e-7, atol=1e-10)

def test_boundary_conditions():
    # Test different boundary conditions
    x = np.linspace(0, 1, 5)
    y = x**2
    
    # Test natural boundary conditions
    coeffs_natural = cubic_spline(x, y, bc_type='natural')
    cs_natural = CubicSpline(x, y, bc_type='natural')
    
    x_eval = np.linspace(0, 1, 20)
    our_result = evaluate_spline(x_eval, x, coeffs_natural)
    scipy_result = cs_natural(x_eval)
    
    np.testing.assert_allclose(our_result, scipy_result, rtol=1e-7)

def test_interpolation_points():
    # Test if the interpolation exactly matches at data points
    x = np.array([0, 1, 2, 3, 4])
    y = np.array([0, 1, 4, 9, 16])  # y = x^2
    
    coeffs = cubic_spline(x, y)
    result = evaluate_spline(x, x, coeffs)
    
    np.testing.assert_allclose(result, y, rtol=1e-7)

def test_derivative():
    # Test derivative of cubic polynomial x^3
    x = np.array([0, 0.5, 1])
    y = x**3
    
    # Our implementation
    coeffs = cubic_spline(x, y, bc_type='clamped')
    deriv_coeffs = cubic_spline_derivative(coeffs)
    x_eval = np.linspace(0, 1, 100)
    our_derivative = evaluate_spline_derivative(x_eval, x, deriv_coeffs)
    
    # SciPy implementation
    cs = CubicSpline(x, y, bc_type='clamped')
    scipy_derivative = cs(x_eval, 1)  # nu=1 means first derivative
    
    np.testing.assert_allclose(our_derivative, scipy_derivative, rtol=1e-7)

def test_derivative_sinusoidal():
    # Test derivative of sin(x)
    x = np.linspace(0, 2*np.pi, 10)
    y = np.sin(x)
    
    coeffs = cubic_spline(x, y, bc_type='natural')
    deriv_coeffs = cubic_spline_derivative(coeffs)
    x_eval = np.linspace(0, 2*np.pi, 100)
    our_derivative = evaluate_spline_derivative(x_eval, x, deriv_coeffs)
    
    cs = CubicSpline(x, y, bc_type='natural')
    scipy_derivative = cs(x_eval, 1)
    
    np.testing.assert_allclose(our_derivative, scipy_derivative, rtol=1e-7)

if __name__ == '__main__':
    pytest.main([__file__])
