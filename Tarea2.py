import numpy as np  # Import the numpy library for numerical operations
import sys
from math import exp
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='fixed_point')
    parser.add_argument('-i', '--input', help='Input archive')
    parser.add_argument('-o', '--output', help='Output archive')
    parser.add_argument('-tol', '--tolerance', help='Error tolerance')
    parser.add_argument('-maxiter', '--max-iterations', help='Max number of iterations')
    args = parser.parse_args() #initialize argument parser and store in args

    try:
        h = float(sys.argv[1])
    except IndexError:
        print('No command line argument for h!')
        sys.exit(1)  # abort execution
    except ValueError:
        print(f'h must be a pure number, not {sys.argv[1]}')
        exit()




def read(filename):
    with open(filename, 'r') as infile:   # open file
             for line in infile:
                  pass# do something with line

def write(filename, somelist):
    with open(filename, 'w') as outfile:  # 'w' for writing
                for data in somelist:
                    outfile.write(data + '\n')


# Definition of the fixed-point method
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
        # Check if the difference is less than the tolerance
        if abs(p_next - p) < tol:
            print(f"Converged in {n} iterations.")
            return p_next
        p = p_next
    # If it does not converge within the maximum number of iterations
    print(f"Did not converge after {max_iter} iterations.")
    return None

# Define the function for which the fixed point will be sought
def g(x):
    return 0.5 * np.sqrt(10 - x**3)

# Appropriate initial value based on the analysis
p0 = 1.5

# Call the fixed-point method
fixed_point = fixed_point_method(g, p0, tol=1e-6, max_iter=100)

# Check if a fixed point was found and display the results
if fixed_point is not None:
    print("Approximate fixed point:", fixed_point)
    print("g(fixed point):", g(fixed_point))
    print("Absolute error:", abs(fixed_point - g(fixed_point)))
else:
    print("No fixed point found.")