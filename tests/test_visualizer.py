"""
Unit tests for magviz magnetic field visualization library.

Run tests with:
    python -m unittest discover -s tests
    or
    python -m pytest tests/
"""

import unittest
import numpy as np

from magviz import MagneticFieldVisualizer, plot_magnetic_field, plot_current_distribution

# Configure matplotlib to use non-interactive backend
import matplotlib
matplotlib.use('Agg')


class TestMagneticFieldVisualizer(unittest.TestCase):
    """Test cases for MagneticFieldVisualizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.viz = MagneticFieldVisualizer()
        self.grid_size = 10
        x = np.linspace(-1, 1, self.grid_size)
        y = np.linspace(-1, 1, self.grid_size)
        X, Y = np.meshgrid(x, y)
        self.B_x = -Y / (X**2 + Y**2 + 0.1)
        self.B_y = X / (X**2 + Y**2 + 0.1)
        self.B_z = np.zeros_like(self.B_x)
    
    def test_parse_field_data_2d_grid(self):
        """Test parsing 2D grid field data."""
        coords, vectors = self.viz._parse_field_data(self.B_x, self.B_y, self.B_z)
        
        self.assertEqual(coords.shape[1], 3, "Coordinates must have 3 columns")
        self.assertEqual(vectors.shape[1], 3, "Vectors must have 3 columns")
        self.assertEqual(coords.shape[0], vectors.shape[0], "Must have same number of points")
        self.assertEqual(coords.shape[0], self.grid_size * self.grid_size)
    
    def test_parse_field_data_1d_array(self):
        """Test parsing 1D array field data."""
        n = 20
        B_x = np.random.randn(n)
        B_y = np.random.randn(n)
        B_z = np.random.randn(n)
        
        coords, vectors = self.viz._parse_field_data(B_x, B_y, B_z)
        
        self.assertEqual(coords.shape, (n, 3))
        self.assertEqual(vectors.shape, (n, 3))
    
    def test_parse_field_data_n1_shape(self):
        """Test parsing (N, 1) shaped arrays."""
        n = 15
        B_x = np.random.randn(n, 1)
        B_y = np.random.randn(n, 1)
        B_z = np.random.randn(n, 1)
        
        coords, vectors = self.viz._parse_field_data(B_x, B_y, B_z)
        
        self.assertEqual(coords.shape, (n, 3))
        self.assertEqual(vectors.shape, (n, 3))
    
    def test_parse_field_data_mn3_shape(self):
        """Test parsing (M, N, 3) combined array."""
        m, n = 8, 8
        B_combined = np.random.randn(m, n, 3)
        
        coords, vectors = self.viz._parse_field_data(B_combined, None, None)
        
        self.assertEqual(coords.shape, (m * n, 3))
        self.assertEqual(vectors.shape, (m * n, 3))
    
    def test_parse_field_data_with_coordinates(self):
        """Test parsing with custom coordinates."""
        n = 20
        B_x = np.random.randn(n)
        B_y = np.random.randn(n)
        B_z = np.random.randn(n)
        custom_coords = np.random.randn(n, 3)
        
        coords, vectors = self.viz._parse_field_data(B_x, B_y, B_z, custom_coords)
        
        np.testing.assert_array_equal(coords, custom_coords)
    
    def test_parse_field_data_mismatched_shapes(self):
        """Test that mismatched shapes raise ValueError."""
        B_x = np.random.randn(10)
        B_y = np.random.randn(15)  # Different size
        B_z = np.random.randn(10)
        
        with self.assertRaises(ValueError):
            self.viz._parse_field_data(B_x, B_y, B_z)
    
    def test_matplotlib_2d_vectors(self):
        """Test matplotlib 2D vector plot."""
        if not self.viz.has_matplotlib:
            self.skipTest("Matplotlib not available")
        
        ax = self.viz.plot_matplotlib_2d_vectors(self.B_x, self.B_y, self.B_z)
        self.assertIsNotNone(ax)
    
    def test_matplotlib_2d_colormap(self):
        """Test matplotlib 2D colormap plot."""
        if not self.viz.has_matplotlib:
            self.skipTest("Matplotlib not available")
        
        ax = self.viz.plot_matplotlib_2d_colormap(self.B_x, self.B_y, self.B_z)
        self.assertIsNotNone(ax)
    
    def test_matplotlib_colormap_components(self):
        """Test matplotlib colormap with different components."""
        if not self.viz.has_matplotlib:
            self.skipTest("Matplotlib not available")
        
        for component in ['magnitude', 'x', 'y', 'z']:
            with self.subTest(component=component):
                ax = self.viz.plot_matplotlib_2d_colormap(
                    self.B_x, self.B_y, self.B_z, component=component
                )
                self.assertIsNotNone(ax)
    
    def test_matplotlib_vectors_color_by(self):
        """Test matplotlib vector plot with different color_by options."""
        if not self.viz.has_matplotlib:
            self.skipTest("Matplotlib not available")
        
        for color_by in ['magnitude', 'x', 'y', None]:
            with self.subTest(color_by=color_by):
                ax = self.viz.plot_matplotlib_2d_vectors(
                    self.B_x, self.B_y, self.B_z, color_by=color_by
                )
                self.assertIsNotNone(ax)
    
    def test_current_distribution(self):
        """Test current distribution plot."""
        if not self.viz.has_matplotlib:
            self.skipTest("Matplotlib not available")
        
        J_x = np.random.randn(10, 10)
        J_y = np.random.randn(10, 10)
        
        ax = self.viz.plot_current_distribution_2d(J_x, J_y)
        self.assertIsNotNone(ax)
    
    def test_plotly_vectors(self):
        """Test Plotly 3D vector plot."""
        if not self.viz.has_plotly:
            self.skipTest("Plotly not available")
        
        fig = self.viz.plot_plotly_vectors(self.B_x, self.B_y, self.B_z)
        self.assertIsNotNone(fig)


class TestGenericFunctions(unittest.TestCase):
    """Test cases for generic convenience functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.grid_size = 10
        x = np.linspace(-1, 1, self.grid_size)
        y = np.linspace(-1, 1, self.grid_size)
        X, Y = np.meshgrid(x, y)
        self.B_x = -Y / (X**2 + Y**2 + 0.1)
        self.B_y = X / (X**2 + Y**2 + 0.1)
        self.B_z = np.zeros_like(self.B_x)
    
    def test_plot_magnetic_field_matplotlib_vectors(self):
        """Test generic plot_magnetic_field with matplotlib vectors."""
        result = plot_magnetic_field(
            self.B_x, self.B_y, self.B_z,
            backend='matplotlib',
            plot_type='vectors'
        )
        self.assertIsNotNone(result)
    
    def test_plot_magnetic_field_matplotlib_colormap(self):
        """Test generic plot_magnetic_field with matplotlib colormap."""
        result = plot_magnetic_field(
            self.B_x, self.B_y, self.B_z,
            backend='matplotlib',
            plot_type='colormap'
        )
        self.assertIsNotNone(result)
    
    def test_plot_magnetic_field_invalid_backend(self):
        """Test that invalid backend raises ValueError."""
        with self.assertRaises(ValueError):
            plot_magnetic_field(
                self.B_x, self.B_y, self.B_z,
                backend='invalid_backend'
            )
    
    def test_plot_magnetic_field_invalid_plot_type(self):
        """Test that invalid plot_type raises ValueError."""
        with self.assertRaises(ValueError):
            plot_magnetic_field(
                self.B_x, self.B_y, self.B_z,
                backend='matplotlib',
                plot_type='invalid_type'
            )
    
    def test_plot_current_distribution(self):
        """Test generic plot_current_distribution."""
        J_x = np.random.randn(10, 10)
        J_y = np.random.randn(10, 10)
        
        result = plot_current_distribution(J_x, J_y)
        self.assertIsNotNone(result)


class TestDataValidation(unittest.TestCase):
    """Test cases for data validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.viz = MagneticFieldVisualizer()
    
    def test_colormap_requires_2d(self):
        """Test that colormap plot requires 2D input."""
        if not self.viz.has_matplotlib:
            self.skipTest("Matplotlib not available")
        
        # 1D arrays should raise ValueError for colormap
        B_x = np.random.randn(20)
        B_y = np.random.randn(20)
        B_z = np.random.randn(20)
        
        with self.assertRaises(ValueError):
            self.viz.plot_matplotlib_2d_colormap(B_x, B_y, B_z)


if __name__ == '__main__':
    unittest.main()
