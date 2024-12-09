import numpy as np

def cubic_spline(x, y):
    """
    Natural cubic spline interpolation.
    Implements the algorithm as described in Burden.
    """
    n = len(x) - 1
    
    # Step 1: Calculate h
    h = np.diff(x)
    
    # Step 2: Calculate alpha
    alpha = np.zeros(n+1)
    for i in range(1, n):
        alpha[i] = 3/h[i]*(y[i+1] - y[i]) - 3/h[i-1]*(y[i] - y[i-1])
    
    # Step 3: Initialize diagonal, mu, and z
    diagonal = np.zeros(n+1)
    mu = np.zeros(n+1)
    z = np.zeros(n+1)
    diagonal[0] = 1
    
    # Step 4: Calculate diagonal, mu, z
    for i in range(1, n):
        diagonal[i] = 2*(x[i+1] - x[i-1]) - h[i-1]*mu[i-1]
        mu[i] = h[i]/diagonal[i]
        z[i] = (alpha[i] - h[i-1]*z[i-1])/diagonal[i]
    
    # Step 5: Set final values
    diagonal[n] = 1
    z[n] = 0
    c = np.zeros(n+1)
    
    # Step 6: Back substitution
    for j in range(n-1, -1, -1):
        c[j] = z[j] - mu[j]*c[j+1]
        
    # Calculate b and d
    b = np.zeros(n)
    d = np.zeros(n)
    for j in range(n):
        b[j] = (y[j+1] - y[j])/h[j] - h[j]*(c[j+1] + 2*c[j])/3
        d[j] = (c[j+1] - c[j])/(3*h[j])
    
    return {
        'a': y[:-1],
        'b': b,
        'c': c[:-1],
        'd': d
    }

def evaluate_spline(x_eval, x, coeffs):
    """
    Evaluate the cubic spline at given points.
    """
    result = np.zeros_like(x_eval, dtype=float)
    
    for i, xi in enumerate(x_eval):
        # Find the appropriate interval
        idx = np.searchsorted(x, xi) - 1
        idx = max(0, min(idx, len(x)-2))
        
        # Calculate the difference
        dx = xi - x[idx]
        
        # Evaluate the cubic polynomial
        result[i] = (coeffs['a'][idx] + 
                    coeffs['b'][idx] * dx +
                    coeffs['c'][idx] * dx**2 +
                    coeffs['d'][idx] * dx**3)
    
    return result

def cubic_spline_derivative(coeffs):
    """
    Calculate coefficients for the derivative of a cubic spline.
    The derivative of a cubic polynomial ax^3 + bx^2 + cx + d
    is 3ax^2 + 2bx + c
    """
    return {
        'a': coeffs['b'],                  # New constant term
        'b': 2 * coeffs['c'],             # New linear term
        'c': 3 * coeffs['d'],             # New quadratic term
        'd': np.zeros_like(coeffs['d'])    # Cubic term becomes zero
    }

def evaluate_spline_derivative(x_eval, x, coeffs):
    """
    Evaluate the derivative of the cubic spline at given points.
    """
    result = np.zeros_like(x_eval, dtype=float)
    
    for i, xi in enumerate(x_eval):
        # Find the appropriate interval
        idx = np.searchsorted(x, xi) - 1
        idx = max(0, min(idx, len(x)-2))
        
        # Calculate the difference
        dx = xi - x[idx]
        
        # Evaluate the derivative polynomial
        result[i] = (coeffs['a'][idx] + 
                    coeffs['b'][idx] * dx +
                    coeffs['c'][idx] * dx**2)
    
    return result
