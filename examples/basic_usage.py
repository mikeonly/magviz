"""
Example usage of MagViz library for magnetic field visualization.

This script demonstrates:
1. Creating synthetic magnetic field data in various formats
2. Using different visualization backends (PyVista, Vedo, Plotly, Matplotlib)
3. Plotting vector fields and colormaps
4. Visualizing current distributions
"""

import numpy as np
import sys
import os

# Add parent directory to path for importing magviz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from magviz import MagneticFieldVisualizer, plot_magnetic_field, plot_current_distribution


def create_dipole_field_2d(grid_size=20):
    """Create a simple 2D magnetic dipole field."""
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Dipole at origin
    r = np.sqrt(X**2 + Y**2) + 0.1  # Add small offset to avoid division by zero
    
    # Magnetic field components for a dipole
    B_x = (3 * X * Y) / r**5
    B_y = (3 * Y**2 - r**2) / r**5
    B_z = np.zeros_like(B_x)
    
    return B_x, B_y, B_z


def create_uniform_field_3d(n_points=10):
    """Create a uniform 3D magnetic field."""
    # Create 3D grid
    x = np.linspace(0, 5, n_points)
    y = np.linspace(0, 5, n_points)
    z = np.linspace(0, 5, n_points)
    
    X, Y, Z = np.meshgrid(x, y, z)
    
    # Uniform field pointing in z-direction with slight variation
    B_x = 0.1 * np.sin(X) * np.ones_like(X)
    B_y = 0.1 * np.cos(Y) * np.ones_like(Y)
    B_z = np.ones_like(Z)
    
    return B_x, B_y, B_z


def create_current_loop_field_2d(grid_size=30):
    """Create magnetic field from a current loop."""
    x = np.linspace(-3, 3, grid_size)
    y = np.linspace(-3, 3, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Current in circular loop creates tangential field
    r = np.sqrt(X**2 + Y**2) + 0.1
    theta = np.arctan2(Y, X)
    
    # Tangential field (simplified)
    B_x = -np.sin(theta) / r**2
    B_y = np.cos(theta) / r**2
    
    return B_x, B_y


def create_current_distribution(grid_size=20):
    """Create a 2D current distribution."""
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Spiral current pattern
    J_x = -Y * np.exp(-(X**2 + Y**2))
    J_y = X * np.exp(-(X**2 + Y**2))
    
    return J_x, J_y


def example_matplotlib_2d():
    """Example: 2D visualization with Matplotlib."""
    print("\n=== Matplotlib 2D Visualization ===")
    
    # Create field data
    B_x, B_y, B_z = create_dipole_field_2d(20)
    
    viz = MagneticFieldVisualizer()
    
    # Plot vector field
    print("Creating 2D vector plot...")
    ax = viz.plot_matplotlib_2d_vectors(
        B_x, B_y, B_z,
        color_by='magnitude',
        scale=30
    )
    
    import matplotlib.pyplot as plt
    plt.savefig('/tmp/magnetic_field_2d_vectors.png', dpi=150, bbox_inches='tight')
    print("Saved to /tmp/magnetic_field_2d_vectors.png")
    plt.close()
    
    # Plot colormap
    print("Creating 2D colormap...")
    ax = viz.plot_matplotlib_2d_colormap(
        B_x, B_y, B_z,
        component='magnitude'
    )
    plt.savefig('/tmp/magnetic_field_2d_colormap.png', dpi=150, bbox_inches='tight')
    print("Saved to /tmp/magnetic_field_2d_colormap.png")
    plt.close()


def example_current_distribution():
    """Example: 2D current distribution visualization."""
    print("\n=== Current Distribution Visualization ===")
    
    J_x, J_y = create_current_distribution(25)
    
    ax = plot_current_distribution(
        J_x, J_y,
        color_by='magnitude',
        scale=20,
        cmap='plasma'
    )
    
    import matplotlib.pyplot as plt
    plt.savefig('/tmp/current_distribution_2d.png', dpi=150, bbox_inches='tight')
    print("Saved to /tmp/current_distribution_2d.png")
    plt.close()


def example_various_shapes():
    """Example: Handling various input shapes."""
    print("\n=== Various Input Shapes ===")
    
    viz = MagneticFieldVisualizer()
    
    # Test 1: (N, 1) shape
    print("Test 1: (N, 1) shaped arrays")
    n = 50
    B_x = np.random.randn(n, 1) * 0.1
    B_y = np.random.randn(n, 1) * 0.1
    B_z = np.ones((n, 1))
    
    ax = viz.plot_matplotlib_2d_vectors(B_x, B_y, B_z, scale=10)
    import matplotlib.pyplot as plt
    plt.savefig('/tmp/test_shape_n1.png', dpi=150, bbox_inches='tight')
    print("Saved to /tmp/test_shape_n1.png")
    plt.close()
    
    # Test 2: (M, N) 2D grid shape
    print("Test 2: (M, N) 2D grid shaped arrays")
    m, n = 15, 15
    B_x = np.random.randn(m, n) * 0.1
    B_y = np.random.randn(m, n) * 0.1
    B_z = np.ones((m, n))
    
    ax = viz.plot_matplotlib_2d_colormap(B_x, B_y, B_z, component='magnitude')
    plt.savefig('/tmp/test_shape_mn.png', dpi=150, bbox_inches='tight')
    print("Saved to /tmp/test_shape_mn.png")
    plt.close()
    
    # Test 3: (M, N, 3) combined shape
    print("Test 3: (M, N, 3) combined array")
    m, n = 10, 10
    B_combined = np.zeros((m, n, 3))
    B_combined[:, :, 0] = np.random.randn(m, n) * 0.1  # B_x
    B_combined[:, :, 1] = np.random.randn(m, n) * 0.1  # B_y
    B_combined[:, :, 2] = np.ones((m, n))              # B_z
    
    ax = viz.plot_matplotlib_2d_vectors(B_combined, None, None, scale=10)
    plt.savefig('/tmp/test_shape_mn3.png', dpi=150, bbox_inches='tight')
    print("Saved to /tmp/test_shape_mn3.png")
    plt.close()


def example_plotly_3d():
    """Example: Interactive 3D visualization with Plotly."""
    print("\n=== Plotly 3D Visualization ===")
    
    try:
        # Create 3D field data (sparse for better visualization)
        B_x, B_y, B_z = create_uniform_field_3d(5)
        
        fig = plot_magnetic_field(
            B_x, B_y, B_z,
            backend='plotly',
            plot_type='vectors',
            scale=0.5
        )
        
        # Save as HTML
        fig.write_html('/tmp/magnetic_field_3d_plotly.html')
        print("Saved to /tmp/magnetic_field_3d_plotly.html")
        
    except ImportError as e:
        print(f"Skipping Plotly example: {e}")


def example_generic_function():
    """Example: Using the generic plot_magnetic_field function."""
    print("\n=== Generic Function Usage ===")
    
    B_x, B_y, B_z = create_current_loop_field_2d(25)
    B_z = np.zeros_like(B_x)  # Make it 2D
    
    # Use generic function with matplotlib backend
    ax = plot_magnetic_field(
        B_x, B_y, B_z,
        backend='matplotlib',
        plot_type='vectors',
        color_by='magnitude',
        scale=30
    )
    
    import matplotlib.pyplot as plt
    plt.savefig('/tmp/generic_function_example.png', dpi=150, bbox_inches='tight')
    print("Saved to /tmp/generic_function_example.png")
    plt.close()


def main():
    """Run all examples."""
    print("=" * 60)
    print("MagViz - Magnetic Field Visualization Examples")
    print("=" * 60)
    
    # Run examples that work with minimal dependencies
    example_matplotlib_2d()
    example_current_distribution()
    example_various_shapes()
    example_generic_function()
    
    # Try optional examples
    example_plotly_3d()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("Check /tmp/ directory for generated plots")
    print("=" * 60)


if __name__ == '__main__':
    main()
