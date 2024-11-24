import numpy as np
import math


def fixed_point_method(expr, p0, tol=1e-6, max_iter=100):
    """
    Implements the fixed-point iteration method to find a fixed point of the function g.
    Modified based on numerical analysis 2024-2 UNALmed course.

    Parameters:
    - expr: String expression of the function g(x)
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
            p_next = eval(expr, {"x": p, "math": math})
            error = abs(p_next - p)

            iterations.append({"n": n, "x": p, "error": error})

            if error < tol:
                return True, iterations
            p = p_next
        except (OverflowError, ValueError):
            return False, iterations

    return False, iterations
