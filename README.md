# MagViz - Magnetic Field Visualization Library

A comprehensive Python library for visualizing magnetic field data and current distributions using multiple visualization backends.

## Features

- **Multiple Visualization Backends**: PyVista, Vedo, Plotly, and Matplotlib
- **Flexible Input Formats**: Handles various array shapes including (N, 1), (M, N), and (M, N, 3)
- **Vector Field Plots**: 3D arrows and 2D quiver plots
- **Scalar Field Plots**: Colormaps and heatmaps
- **Current Distribution Visualization**: 2D vector fields for current density
- **Easy-to-use API**: Generic functions and class-based interface

## Installation

### Basic Installation

```bash
pip install -r requirements.txt
```

### Install from source

```bash
git clone https://github.com/mikeonly/magviz.git
cd magviz
pip install -e .
```

### Dependencies

- numpy >= 1.20.0
- matplotlib >= 3.3.0
- plotly >= 5.0.0
- pyvista >= 0.37.0
- vedo >= 2023.4.0
- scipy >= 1.7.0

## Quick Start

### Basic Usage

```python
import numpy as np
from magviz import plot_magnetic_field, plot_current_distribution

# Create sample magnetic field data
grid_size = 20
x = np.linspace(-2, 2, grid_size)
y = np.linspace(-2, 2, grid_size)
X, Y = np.meshgrid(x, y)

B_x = -Y / (X**2 + Y**2 + 0.1)
B_y = X / (X**2 + Y**2 + 0.1)
B_z = np.zeros_like(B_x)

# Plot with matplotlib (2D)
plot_magnetic_field(B_x, B_y, B_z, 
                   backend='matplotlib', 
                   plot_type='vectors',
                   color_by='magnitude')
```

### Using Different Backends

#### Matplotlib (2D Visualization)

```python
from magviz import MagneticFieldVisualizer

viz = MagneticFieldVisualizer()

# Vector field plot
ax = viz.plot_matplotlib_2d_vectors(B_x, B_y, B_z, 
                                    color_by='magnitude',
                                    scale=30)

# Colormap plot
ax = viz.plot_matplotlib_2d_colormap(B_x, B_y, B_z,
                                     component='magnitude',
                                     cmap='viridis')
```

#### PyVista (3D Visualization)

```python
# 3D vector field with arrows
plotter = viz.plot_pyvista_vectors(B_x, B_y, B_z,
                                   scale=1.0,
                                   show_scalar=True,
                                   scalar_component='magnitude')
plotter.show()

# 3D scalar field
plotter = viz.plot_pyvista_scalar(B_x, B_y, B_z,
                                  component='magnitude',
                                  cmap='viridis')
plotter.show()
```

#### Plotly (Interactive 3D)

```python
# Interactive 3D visualization
fig = viz.plot_plotly_vectors(B_x, B_y, B_z,
                              scale=1.0,
                              color_by='magnitude')
fig.show()
```

#### Vedo (3D Visualization)

```python
# 3D arrows with Vedo
plotter = viz.plot_vedo_vectors(B_x, B_y, B_z,
                                scale=1.0,
                                color='blue')
```

### Current Distribution Visualization

```python
# Create current density data
J_x = -Y * np.exp(-(X**2 + Y**2))
J_y = X * np.exp(-(X**2 + Y**2))

# Plot current distribution
ax = plot_current_distribution(J_x, J_y,
                               color_by='magnitude',
                               scale=20,
                               cmap='plasma')
```

## Supported Input Formats

The library handles various input array shapes:

### 1D Arrays: (N, 1) or (N,)
```python
n = 100
B_x = np.random.randn(n, 1)
B_y = np.random.randn(n, 1)
B_z = np.random.randn(n, 1)
```

### 2D Grids: (M, N)
```python
m, n = 20, 20
x = np.linspace(0, 10, n)
y = np.linspace(0, 10, m)
X, Y = np.meshgrid(x, y)

B_x = np.sin(X) * np.cos(Y)
B_y = np.cos(X) * np.sin(Y)
B_z = np.zeros_like(B_x)
```

### Combined Format: (M, N, 3)
```python
m, n = 20, 20
B_combined = np.zeros((m, n, 3))
B_combined[:, :, 0] = B_x  # x-component
B_combined[:, :, 1] = B_y  # y-component
B_combined[:, :, 2] = B_z  # z-component

# Can pass as single array
plot_magnetic_field(B_combined, None, None, backend='matplotlib')
```

## API Reference

### Main Classes and Functions

#### `MagneticFieldVisualizer`

Main class providing visualization methods for different backends.

**Methods:**
- `plot_pyvista_vectors()` - 3D vector field with PyVista
- `plot_pyvista_scalar()` - 3D scalar field with PyVista
- `plot_vedo_vectors()` - 3D vector field with Vedo
- `plot_plotly_vectors()` - Interactive 3D vector field with Plotly
- `plot_matplotlib_2d_vectors()` - 2D vector field with Matplotlib
- `plot_matplotlib_2d_colormap()` - 2D colormap with Matplotlib
- `plot_current_distribution_2d()` - 2D current distribution

#### `plot_magnetic_field(B_x, B_y, B_z, ...)`

Generic convenience function for plotting magnetic fields.

**Parameters:**
- `B_x, B_y, B_z`: Magnetic field components (numpy arrays)
- `coordinates`: Optional position array (default: auto-generated grid)
- `backend`: 'pyvista', 'vedo', 'plotly', or 'matplotlib'
- `plot_type`: 'vectors', 'colormap', or 'scalar'
- `**kwargs`: Additional backend-specific arguments

#### `plot_current_distribution(J_x, J_y, ...)`

Generic function for plotting 2D current distributions.

**Parameters:**
- `J_x, J_y`: Current density components
- `coordinates`: Optional position array
- `color_by`: 'magnitude', 'x', 'y', or None
- `**kwargs`: Additional plotting arguments

## Examples

See the `examples/` directory for complete examples:

- `basic_usage.py` - Comprehensive examples of all features
- Demonstrates various input shapes
- Shows all visualization backends
- Includes current distribution visualization

Run examples:
```bash
python examples/basic_usage.py
```

## Use Cases

### 1. Electromagnetic Simulations
Visualize magnetic fields from finite element analysis or analytical solutions.

### 2. MRI/Medical Imaging
Display magnetic field distributions in medical imaging systems.

### 3. Magnetic Sensor Data
Plot measured magnetic field data from sensor arrays.

### 4. Education and Research
Create publication-quality visualizations for papers and presentations.

### 5. Current Flow Analysis
Visualize current distributions in conductors and circuits.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Citation

If you use this library in your research, please cite:

```
MagViz: A Python Library for Magnetic Field Visualization
Author: Mike
Year: 2024
URL: https://github.com/mikeonly/magviz
```

## Contact

For questions or issues, please open an issue on GitHub.
