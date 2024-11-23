import os


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
        raise ValueError("Tolerance must be a valid number")
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
