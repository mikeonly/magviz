"""
MagViz - Magnetic Field Visualization Library

A library for visualizing magnetic field data using PyVista, Vedo, Plotly, and Matplotlib.
"""

from .visualizer import (
    MagneticFieldVisualizer,
    plot_magnetic_field,
    plot_current_distribution
)

__version__ = "0.1.0"
__all__ = [
    "MagneticFieldVisualizer",
    "plot_magnetic_field",
    "plot_current_distribution"
]
