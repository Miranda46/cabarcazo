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
    - tuple: (converges, iterations) where:
        - converges: Boolean indicating if the method converged
        - iterations: List of dictionaries containing iteration data
    """
    p = p0
    iterations = []

    for n in range(1, max_iter + 1):
        try:
            p_next = g(p)
            error = abs(p_next - p)

            iterations.append({"n": n, "x": p, "error": error})

            if error < tol:
                return True, iterations
            p = p_next
        except OverflowError:
            return False, iterations

    return False, iterations
