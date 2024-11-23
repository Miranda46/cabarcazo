import numpy as np


def fixed_point_method(g, p0, tol=1e-6, max_iter=100):
    """
    Implements the fixed-point iteration method to find a fixed point of the function g.

    Parameters:
    - g: Function for which the fixed point is sought.
    - p0: Initial approximation.
    - tol: Tolerance for the convergence criterion.
    - max_iter: Maximum number of iterations allowed.

    Returns:
    - p: Approximation of the fixed point.
    - None: If it does not converge within the maximum number of iterations.
    """
    p = p0
    for n in range(1, max_iter + 1):
        p_next = g(p)
        if abs(p_next - p) < tol:
            print(f"Converged in {n} iterations.")
            return p_next
        p = p_next
    print(f"Did not converge after {max_iter} iterations.")
    return None


def default_g(x):
    return 0.5 * np.sqrt(10 - x**3)
