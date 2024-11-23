import sys
import argparse
from validators import (
    validate_input_file,
    validate_output_file,
    validate_tolerance,
    validate_max_iterations,
)
from fixed_point_method import fixed_point_method, default_g


def read(filename):
    with open(filename, "r") as infile:
        for line in infile:
            pass  # do something with line


def write(filename, somelist):
    with open(filename, "w") as outfile:
        for data in somelist:
            outfile.write(data + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fixed_point")
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Input file (.tex)"
    )
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file")
    parser.add_argument(
        "-tol", "--tolerance", type=str, required=True, help="Error tolerance"
    )
    parser.add_argument(
        "-maxiter",
        "--max-iterations",
        type=str,
        required=True,
        help="Max number of iterations",
    )
    args = parser.parse_args()

    try:
        # Validate all inputs
        validate_input_file(args.input)
        validate_output_file(args.output)
        tolerance = validate_tolerance(args.tolerance)
        max_iterations = validate_max_iterations(args.max_iterations)

        # Use the fixed-point method
        p0 = 1.5  # Initial value
        fixed_point = fixed_point_method(
            default_g, p0, tol=tolerance, max_iter=max_iterations
        )

        # Check results
        if fixed_point is not None:
            print("Approximate fixed point:", fixed_point)
            print("g(fixed point):", default_g(fixed_point))
            print("Absolute error:", abs(fixed_point - default_g(fixed_point)))
        else:
            print("No fixed point found.")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
