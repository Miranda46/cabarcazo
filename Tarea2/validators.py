import os
import math


def validate_input_file(input_file):
    if not input_file.endswith(".tex"):
        raise ValueError("Input file must be a .tex file")
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found")


def validate_output_file(output_file):
    if not output_file:
        raise ValueError("Output filename cannot be empty")
    # Additional output file validations can be added here


def validate_tolerance(tolerance_str):
    try:
        tolerance = float(tolerance_str)
    except ValueError:
        raise ValueError("Tolerance must be a valid number in floating point format")
    if tolerance <= 0:
        raise ValueError("Tolerance must be a positive number")
    return tolerance


def validate_max_iterations(max_iter_str):
    try:
        max_iterations = int(max_iter_str)
    except ValueError:
        raise ValueError("Maximum iterations must be a valid integer")
    if max_iterations <= 0:
        raise ValueError("Maximum iterations must be a positive integer")
    return max_iterations


def validate_file_content(filename):
    """Validate the content format of the input file"""
    # Define safe math functions that can be used in expressions
    safe_dict = {
        name: getattr(math, name)
        for name in ["sin", "cos", "tan", "exp", "log", "sqrt"]
    }
    safe_dict.update({"abs": abs, "pow": pow})

    line_counter = 0
    with open(filename, "r") as file:
        for line in file:
            line_counter += 1
            line = line.strip()
            if not line:  # Skip empty lines
                continue

            parts = line.split(";")
            if len(parts) != 3:
                raise ValueError(
                    f"Invalid format in line {line_counter}. Expected 3 fields separated by semicolons"
                )

            name, expr, p0 = parts

            # Validate function name (any non-empty string is valid)
            if not name.strip():
                raise ValueError(f"Invalid function name in line {line_counter}")

            # Validate initial point
            try:
                float(p0)
            except ValueError:
                raise ValueError(f"Invalid initial point '{p0}' in line {line_counter}")

            # Validate expression by trying to evaluate it with x=1
            try:
                safe_dict["x"] = 1
                eval(expr, {"x": 1, "math": math})
            except (NameError, SyntaxError, TypeError) as e:
                raise ValueError(
                    f"Invalid expression '{expr}' in line {line_counter}: {str(e)}"
                )
