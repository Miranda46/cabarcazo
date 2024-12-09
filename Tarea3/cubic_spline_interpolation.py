import numpy as np

def cubic_spline(x, y, bc_type='natural'):
    n = len(x) - 1
    h = np.diff(x)  # h[j] = x[j+1] - x[j]
    
    # Set up the tridiagonal system for c coefficients (equation 3.21)
    A = np.zeros((n+1, n+1))
    b = np.zeros(n+1)
    
    # Interior points (j = 1 to n-1)
    for j in range(1, n):
        A[j, j-1] = h[j-1]
        A[j, j] = 2 * (h[j-1] + h[j])
        A[j, j+1] = h[j]
        b[j] = 3 * ((y[j+1] - y[j])/h[j] - (y[j] - y[j-1])/h[j-1])
    
    # Boundary conditions
    if bc_type == 'natural':
        # Second derivatives = 0 at endpoints
        A[0, 0] = 1
        A[-1, -1] = 1
        b[0] = 0
        b[-1] = 0
    elif bc_type == 'clamped':
        # First derivatives specified at endpoints
        A[0, 0] = 2*h[0]
        A[0, 1] = h[0]
        A[-1, -1] = 2*h[-1]
        A[-1, -2] = h[-1]
        
        # For demonstration, using f'(a)=0 and f'(b)=0
        f_prime_a = 0
        f_prime_b = 0
        b[0] = 3*((y[1] - y[0])/h[0] - f_prime_a)
        b[-1] = 3*(f_prime_b - (y[-1] - y[-2])/h[-1])
    
    # Solve for c coefficients
    c = np.linalg.solve(A, b)
    
    # Calculate b coefficients using equation (3.20)
    b = np.zeros(n)
    for j in range(n):
        b[j] = (y[j+1] - y[j])/h[j] - h[j]*(2*c[j] + c[j+1])/3
    
    # Calculate d coefficients using equation (3.17)
    d = np.zeros(n)
    for j in range(n):
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
