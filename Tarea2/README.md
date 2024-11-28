# Fixed Point Method Implementation

## Description
This script implements the fixed-point iteration method to find fixed points of mathematical functions.

## Input File Format (datos.txt)
The input file must be a .txt file with the following format:

Each line contains:
- `function_name`: Identifier for the function
- `function_expression`: Valid Python mathematical expression (can use math module functions)
- `initial_value`: Starting point for iteration

### Example datos.txt:

func1;2*x-1;10  
func2;math.sin(x);1  
func3;(x**2-4)/5;0

## Usage
Run the script using:

```bash
python punto_fijo.py -i datos.txt -o resumen.txt -tol 0.00001 -maxiter 100
```

## Parameters
- `-i` or `--input`: Input .txt file containing functions
- `-o` or `--output`: Output text file for results
- `-tol` or `--tolerance`: Convergence tolerance
- `-maxiter` or `--max-iterations`: Maximum iterations

## Requirements
- Python 3.x

## Tests
Run the tests using:

```bash
python test.py
```