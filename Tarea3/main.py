import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cubic_spline_interpolation import cubic_spline, evaluate_spline, cubic_spline_derivative, evaluate_spline_derivative

def read_data(filepath):
    """Read and validate CSV data."""
    try:
        df = pd.read_csv(filepath, sep=';')
        if len(df.columns) < 2:
            raise ValueError("File must have at least 2 columns")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filepath} not found")
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

def perform_linear_regression(x, y):
    """Calculate linear regression parameters."""
    A = np.vstack([x, np.ones(len(x))]).T
    m, b = np.linalg.lstsq(A, y, rcond=None)[0]
    return m, b

def get_interval_midpoint(x_range, m, b):
    """Calculate midpoint of regression line in interval."""
    x_mid = np.mean(x_range)
    y_mid = m * x_mid + b
    return x_mid, y_mid

def process_intervals(x, y, n):
    """Process data into n intervals."""
    x_min, x_max = x.min(), x.max()
    interval_size = (x_max - x_min) / n
    midpoints_x = []
    midpoints_y = []
    
    # Count points in each interval
    points_per_interval = []
    for i in range(n):
        interval_start = x_min + i * interval_size
        interval_end = interval_start + interval_size
        mask = (x >= interval_start) & (x <= interval_end)
        points_per_interval.append(np.sum(mask))
    
    # Check if any interval has less than 2 points
    if min(points_per_interval) < 2:
        raise ValueError("Se necesitan más puntos de muestra para poder llevar a cabo la regresión lineal (mínimo 2 por intervalo)")
    
    for i in range(n):
        interval_start = x_min + i * interval_size
        interval_end = interval_start + interval_size
        mask = (x >= interval_start) & (x <= interval_end)
        
        x_interval = x[mask]
        y_interval = y[mask]
        m, b = perform_linear_regression(x_interval, y_interval)
        x_mid, y_mid = get_interval_midpoint([interval_start, interval_end], m, b)
        midpoints_x.append(x_mid)
        midpoints_y.append(y_mid)
    
    return np.array(midpoints_x), np.array(midpoints_y)

def create_plot(x, y, n, column_name):
    """Create and save individual plot."""
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    
    # Process intervals
    x_min, x_max = x.min(), x.max()
    interval_size = (x_max - x_min) / n
    
    # Plot regression lines for each interval - updated plotting
    for i in range(n):
        interval_start = x_min + i * interval_size
        interval_end = interval_start + interval_size
        mask = (x >= interval_start) & (x <= interval_end)
        
        if np.sum(mask) > 1:
            x_interval = x[mask]
            y_interval = y[mask]
            m, b = perform_linear_regression(x_interval, y_interval)
            x_reg = np.array([interval_start, interval_end])
            y_reg = m * x_reg + b
            if i == 0:  # Only add label once for legend
                ax1.plot(x_reg, y_reg, 'b-', alpha=0.7, label='Líneas de Regresión')
            else:
                ax1.plot(x_reg, y_reg, 'b-', alpha=0.7)
    
    # Process data and calculate midpoints
    midpoints_x, midpoints_y = process_intervals(x, y, n)
    
    # Calculate spline interpolation
    coeffs = cubic_spline(midpoints_x, midpoints_y)
    x_smooth = np.linspace(x.min(), x.max(), 200)
    y_smooth = evaluate_spline(x_smooth, midpoints_x, coeffs)
    
    # Calculate derivative
    deriv_coeffs = cubic_spline_derivative(coeffs)
    y_deriv = evaluate_spline_derivative(x_smooth, midpoints_x, deriv_coeffs)
    
    # Plot original data
    ax1.scatter(x, y, alpha=0.5, label='Datos Originales')
    ax1.scatter(midpoints_x, midpoints_y, color='red', label='Puntos Medios')
    ax1.plot(x_smooth, y_smooth, 'g-', label='Interpolación Spline')
    
    # Plot derivative on secondary axis
    ax2.plot(x_smooth, y_deriv, 'r--', label='Derivada')
    
    # Configure plot
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax2.set_ylabel('dy/dx')
    
    # Create a single legend combining both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    all_lines = lines1 + lines2
    all_labels = labels1 + labels2
    
    # Add legend without title, positioned higher
    plt.legend(all_lines, all_labels, 
              loc='upper center',
              bbox_to_anchor=(0.5, 1.15),  # Changed from 1.1 to 1.15
              ncol=3,
              frameon=True)
    
    # Save plot with adjusted margin
    plt.savefig(f'{column_name}_{n}.png', 
                bbox_inches='tight',
                pad_inches=0.2)
    plt.close()
    
    return fig

def create_grid_visualization(df, n_range=(6, 11)):
    """Create grid of visualizations."""
    columns = df.columns[1:]  # Skip x column
    n_values = range(*n_range)
    
    fig, axes = plt.subplots(len(n_values), len(columns), 
                            figsize=(5*len(columns), 4*len(n_values)))
    
    for i, n in enumerate(n_values):
        for j, col in enumerate(columns):
            ax1 = axes[i, j] if len(n_values) > 1 else axes[j]
            ax2 = ax1.twinx()  # Create secondary axis for derivative
            x, y = df.iloc[:, 0], df[col]
            
            # Plot regression lines
            x_min, x_max = x.min(), x.max()
            interval_size = (x_max - x_min) / n
            for k in range(n):
                interval_start = x_min + k * interval_size
                interval_end = interval_start + interval_size
                mask = (x >= interval_start) & (x <= interval_end)
                if np.sum(mask) > 1:
                    x_interval = x[mask]
                    y_interval = y[mask]
                    m, b = perform_linear_regression(x_interval, y_interval)
                    x_reg = np.array([interval_start, interval_end])
                    y_reg = m * x_reg + b
                    ax1.plot(x_reg, y_reg, 'b-', alpha=0.7)
            
            # Process data and calculate all curves
            midpoints_x, midpoints_y = process_intervals(x, y, n)
            coeffs = cubic_spline(midpoints_x, midpoints_y)
            x_smooth = np.linspace(x.min(), x.max(), 200)
            y_smooth = evaluate_spline(x_smooth, midpoints_x, coeffs)
            
            # Calculate and plot derivative
            deriv_coeffs = cubic_spline_derivative(coeffs)
            y_deriv = evaluate_spline_derivative(x_smooth, midpoints_x, deriv_coeffs)
            ax2.plot(x_smooth, y_deriv, 'r--', alpha=0.5)
            
            # Plot all elements
            ax1.scatter(x, y, alpha=0.5, s=5, color='gray')  # Increased size and opacity
            ax1.scatter(midpoints_x, midpoints_y, color='red', s=20)
            ax1.plot(x_smooth, y_smooth, 'g-')
            
            # Configure axes
            if i == 0:
                ax1.set_title(col)
            if j == 0:
                ax1.set_ylabel(f'n={n}')
            if j == len(columns)-1:  # Only show derivative axis for last column
                ax2.set_ylabel('Derivada')
            else:
                ax2.set_ylabel('')
            
            # Remove ticks from secondary axis if not the last column
            if j != len(columns)-1:
                ax2.set_yticks([])
    
    plt.tight_layout()
    plt.savefig('grid_visualization.png')
    plt.close()

def main():
    try:
        # Read data
        df = read_data('data.csv')
        x = df.iloc[:, 0].values
        
        # Validate minimum number of rows
        if len(df) < 10:
            raise ValueError("Se necesitan más puntos de muestra para poder llevar a cabo la regresión lineal (mínimo 2 puntos por intervalo)")
        
        # Process each experiment for n values 6 to 10
        for column in df.columns[1:]:  # Skip x column
            y = df[column].values
            for n in range(6, 11):
                create_plot(x, y, n, column)
        
        # Create grid visualization
        create_grid_visualization(df, n_range=(6, 11))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
