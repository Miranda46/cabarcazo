import sys
import argparse
from validators import (
    validate_input_file,
    validate_output_file,
    validate_tolerance,
    validate_max_iterations,
    validate_file_content,
)
from fixed_point_method import fixed_point_method
import math


def read(filename):
    validate_file_content(filename)
    functions = []
    with open(filename, "r") as infile:
        for line in infile:
            if line.strip():  # Skip empty lines
                name, expr, p0 = line.strip().split(";")
                functions.append(
                    {
                        "name": name,
                        "expr": expr,
                        "p0": float(p0),
                    }
                )
    return functions


def calculate_convergence_rate(errors):
    if len(errors) < 2:
        return 0
    # Calculate average convergence rate using consecutive errors
    rates = []
    for i in range(1, len(errors)):
        if errors[i - 1] == 0:  # Avoid division by zero
            continue
        rate = abs(errors[i] / errors[i - 1])
        rates.append(rate)
    return sum(rates) / len(rates) if rates else 0


def write(filename, results):
    # Write individual files for each function
    for result in results:
        function_name = result["name"]
        iterations = result["iterations"]

        # Write detailed iterations to function-specific file
        with open(f"{function_name}.txt", "w") as f:
            # Header with fixed column widths
            f.write(f"{'n':>4} {'x':>25} {'error':>25}\n")
            f.write("-" * 55 + "\n")  # Add separator line
            for iter_data in iterations:
                # Format numbers using scientific notation for large values
                x_val = iter_data["x"]
                error_val = iter_data["error"]

                # Use scientific notation if number is too large or too small
                x_str = (
                    f"{x_val:25.6e}"
                    if abs(x_val) > 1e6 or abs(x_val) < 1e-6
                    else f"{x_val:25.6f}"
                )
                error_str = (
                    f"{error_val:25.6e}"
                    if abs(error_val) > 1e6 or abs(error_val) < 1e-6
                    else f"{error_val:25.6f}"
                )

                f.write(f"{iter_data['n']:4d} {x_str} {error_str}\n")

    # Write summary file
    with open(filename, "w") as f:
        # Headers with appropriate spacing
        headers = [
            "nombre_funcion",
            "expresion_funcion",
            "punto_inicial",
            "converge",
            "velocidad",
        ]
        f.write(
            f"{headers[0]:<20}\t{headers[1]:<30}\t{headers[2]:>12}\t{headers[3]:>8}\t{headers[4]:>12}\n"
        )

        for result in results:
            function_name = result["name"]
            converged = result["converged"]
            iterations = result["iterations"]

            # Calculate convergence rate only if the function converged
            velocity = "--"
            if converged:
                errors = [iter_data["error"] for iter_data in iterations]
                velocity = calculate_convergence_rate(errors)
                velocity = f"{velocity:>12.6f}"
            else:
                velocity = f"{velocity:>12}"

            # Get original function expression and initial point
            func_data = next(f for f in functions if f["name"] == function_name)

            # Format each field with fixed width
            f.write(
                f"{function_name:<20}\t"
                f"{func_data['expr']:<30}\t"
                f"{func_data['p0']:>12.6f}\t"
                f"{str(converged):>8}\t"
                f"{velocity}\n"
            )


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

        # Read functions from input file
        functions = read(args.input)

        # Process each function
        results = []
        for func in functions:
            converged, iterations = fixed_point_method(
                func["expr"], func["p0"], tol=tolerance, max_iter=max_iterations
            )
            results.append(
                {"name": func["name"], "converged": converged, "iterations": iterations}
            )

        # Write results to output file
        write(args.output, results)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
