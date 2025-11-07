"""
Magnetic Field Visualizer

This module provides a generic function for visualizing magnetic field maps and current distributions
using PyVista, Vedo, Plotly, and Matplotlib.
"""

import numpy as np
from typing import Optional, Tuple, Union, Literal
import warnings


class MagneticFieldVisualizer:
    """
    A comprehensive visualizer for magnetic field data and current distributions.
    
    Supports multiple visualization backends:
    - PyVista: 3D vector fields, scalar fields, and glyphs
    - Vedo: 3D vector fields and arrows
    - Plotly: Interactive 3D plots
    - Matplotlib: 2D vector fields and colormaps
    """
    
    def __init__(self):
        """Initialize the visualizer."""
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check if visualization libraries are available."""
        self.has_pyvista = False
        self.has_vedo = False
        self.has_plotly = False
        self.has_matplotlib = False
        
        try:
            import pyvista
            self.has_pyvista = True
        except ImportError:
            warnings.warn("PyVista not available. Install with: pip install pyvista")
        
        try:
            import vedo
            self.has_vedo = True
        except ImportError:
            warnings.warn("Vedo not available. Install with: pip install vedo")
        
        try:
            import plotly
            self.has_plotly = True
        except ImportError:
            warnings.warn("Plotly not available. Install with: pip install plotly")
        
        try:
            import matplotlib
            self.has_matplotlib = True
        except ImportError:
            warnings.warn("Matplotlib not available. Install with: pip install matplotlib")
    
    def _parse_field_data(
        self, 
        B_x: np.ndarray, 
        B_y: np.ndarray, 
        B_z: np.ndarray,
        coordinates: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Parse and normalize magnetic field data into consistent format.
        
        Handles various input shapes:
        - (N, 1): 1D array of field values
        - (M, N): 2D grid of field values
        - (M, N, 3): 3D array where last dimension is [Bx, By, Bz]
        - (N,): 1D array (will be reshaped)
        
        Args:
            B_x: X-component of magnetic field
            B_y: Y-component of magnetic field
            B_z: Z-component of magnetic field
            coordinates: Optional coordinate array (N, 3) or will be generated
            
        Returns:
            Tuple of (coordinates, vectors) where:
            - coordinates: (N, 3) array of [x, y, z] positions
            - vectors: (N, 3) array of [Bx, By, Bz] field values
        """
        # Convert inputs to numpy arrays
        B_x = np.asarray(B_x)
        B_y = np.asarray(B_y)
        B_z = np.asarray(B_z)
        
        # Handle case where input is (M, N, 3) combined format
        if B_x.ndim == 3 and B_x.shape[-1] == 3:
            vectors = B_x.reshape(-1, 3)
            shape = B_x.shape[:2]
        else:
            # Ensure all components have the same shape
            if B_x.shape != B_y.shape or B_x.shape != B_z.shape:
                raise ValueError(
                    f"Field components must have same shape. Got Bx: {B_x.shape}, "
                    f"By: {B_y.shape}, Bz: {B_z.shape}"
                )
            
            # Flatten and combine into vectors
            B_x_flat = B_x.flatten()
            B_y_flat = B_y.flatten()
            B_z_flat = B_z.flatten()
            vectors = np.column_stack([B_x_flat, B_y_flat, B_z_flat])
            shape = B_x.shape
        
        # Generate or validate coordinates
        if coordinates is None:
            # Generate grid coordinates based on shape
            if len(shape) == 1:
                # 1D case
                n_points = shape[0]
                x = np.arange(n_points)
                y = np.zeros(n_points)
                z = np.zeros(n_points)
            elif len(shape) == 2:
                # 2D case
                x = np.arange(shape[1])
                y = np.arange(shape[0])
                X, Y = np.meshgrid(x, y)
                x = X.flatten()
                y = Y.flatten()
                z = np.zeros_like(x)
            else:
                # Fallback: linear coordinates
                n_points = len(vectors)
                x = np.arange(n_points)
                y = np.zeros(n_points)
                z = np.zeros(n_points)
            
            coordinates = np.column_stack([x, y, z])
        else:
            coordinates = np.asarray(coordinates)
            if coordinates.shape[0] != vectors.shape[0]:
                raise ValueError(
                    f"Number of coordinates ({coordinates.shape[0]}) must match "
                    f"number of field values ({vectors.shape[0]})"
                )
            # Ensure coordinates are (N, 3)
            if coordinates.ndim == 1:
                coordinates = coordinates.reshape(-1, 1)
            if coordinates.shape[1] < 3:
                # Pad with zeros if needed
                padding = np.zeros((coordinates.shape[0], 3 - coordinates.shape[1]))
                coordinates = np.column_stack([coordinates, padding])
        
        return coordinates, vectors
    
    def plot_pyvista_vectors(
        self,
        B_x: np.ndarray,
        B_y: np.ndarray,
        B_z: np.ndarray,
        coordinates: Optional[np.ndarray] = None,
        scale: float = 1.0,
        color: Optional[str] = None,
        show_scalar: bool = False,
        scalar_component: Literal['magnitude', 'x', 'y', 'z'] = 'magnitude',
        notebook: bool = False,
        **kwargs
    ):
        """
        Plot magnetic field as 3D vectors using PyVista.
        
        Args:
            B_x, B_y, B_z: Field components
            coordinates: Optional (N, 3) array of positions
            scale: Scale factor for arrows
            color: Color for arrows (if not showing scalars)
            show_scalar: Whether to color by scalar field
            scalar_component: Which component to use for coloring
            notebook: Whether to use notebook plotter
            **kwargs: Additional arguments for PyVista
        """
        if not self.has_pyvista:
            raise ImportError("PyVista is required for this visualization")
        
        import pyvista as pv
        
        coords, vectors = self._parse_field_data(B_x, B_y, B_z, coordinates)
        
        # Create point cloud
        cloud = pv.PolyData(coords)
        cloud['vectors'] = vectors
        
        # Calculate scalar field if requested
        if show_scalar:
            if scalar_component == 'magnitude':
                cloud['scalars'] = np.linalg.norm(vectors, axis=1)
            elif scalar_component == 'x':
                cloud['scalars'] = vectors[:, 0]
            elif scalar_component == 'y':
                cloud['scalars'] = vectors[:, 1]
            elif scalar_component == 'z':
                cloud['scalars'] = vectors[:, 2]
        
        # Create arrows
        arrows = cloud.glyph(orient='vectors', scale='vectors', factor=scale)
        
        # Plot
        plotter = pv.Plotter(notebook=notebook)
        if show_scalar:
            plotter.add_mesh(arrows, scalars='scalars', cmap='viridis', **kwargs)
        else:
            plotter.add_mesh(arrows, color=color or 'blue', **kwargs)
        
        plotter.add_axes()
        plotter.show_grid()
        
        return plotter
    
    def plot_pyvista_scalar(
        self,
        B_x: np.ndarray,
        B_y: np.ndarray,
        B_z: np.ndarray,
        coordinates: Optional[np.ndarray] = None,
        component: Literal['magnitude', 'x', 'y', 'z'] = 'magnitude',
        cmap: str = 'viridis',
        notebook: bool = False,
        **kwargs
    ):
        """
        Plot magnetic field as scalar colormap using PyVista.
        
        Args:
            B_x, B_y, B_z: Field components
            coordinates: Optional (N, 3) array of positions
            component: Which component to visualize
            cmap: Colormap name
            notebook: Whether to use notebook plotter
            **kwargs: Additional arguments for PyVista
        """
        if not self.has_pyvista:
            raise ImportError("PyVista is required for this visualization")
        
        import pyvista as pv
        
        coords, vectors = self._parse_field_data(B_x, B_y, B_z, coordinates)
        
        # Calculate scalar field
        if component == 'magnitude':
            scalars = np.linalg.norm(vectors, axis=1)
            label = '|B| [T]'
        elif component == 'x':
            scalars = vectors[:, 0]
            label = 'Bx [T]'
        elif component == 'y':
            scalars = vectors[:, 1]
            label = 'By [T]'
        elif component == 'z':
            scalars = vectors[:, 2]
            label = 'Bz [T]'
        
        # Create point cloud
        cloud = pv.PolyData(coords)
        cloud[label] = scalars
        
        # Plot
        plotter = pv.Plotter(notebook=notebook)
        plotter.add_mesh(cloud, scalars=label, cmap=cmap, point_size=10, render_points_as_spheres=True, **kwargs)
        plotter.add_axes()
        plotter.show_grid()
        
        return plotter
    
    def plot_vedo_vectors(
        self,
        B_x: np.ndarray,
        B_y: np.ndarray,
        B_z: np.ndarray,
        coordinates: Optional[np.ndarray] = None,
        scale: float = 1.0,
        color: str = 'blue',
        **kwargs
    ):
        """
        Plot magnetic field as 3D vectors using Vedo.
        
        Args:
            B_x, B_y, B_z: Field components
            coordinates: Optional (N, 3) array of positions
            scale: Scale factor for arrows
            color: Color for arrows
            **kwargs: Additional arguments for Vedo
        """
        if not self.has_vedo:
            raise ImportError("Vedo is required for this visualization")
        
        import vedo
        
        coords, vectors = self._parse_field_data(B_x, B_y, B_z, coordinates)
        
        # Create arrows
        arrows = vedo.Arrows(
            coords,
            coords + vectors * scale,
            c=color,
            **kwargs
        )
        
        # Create plotter
        plotter = vedo.Plotter()
        plotter.show(arrows, axes=1)
        
        return plotter
    
    def plot_plotly_vectors(
        self,
        B_x: np.ndarray,
        B_y: np.ndarray,
        B_z: np.ndarray,
        coordinates: Optional[np.ndarray] = None,
        scale: float = 1.0,
        color_by: Literal['magnitude', 'x', 'y', 'z', None] = 'magnitude',
        **kwargs
    ):
        """
        Plot magnetic field as interactive 3D vectors using Plotly.
        
        Args:
            B_x, B_y, B_z: Field components
            coordinates: Optional (N, 3) array of positions
            scale: Scale factor for arrows
            color_by: Which component to use for coloring
            **kwargs: Additional arguments for Plotly
        """
        if not self.has_plotly:
            raise ImportError("Plotly is required for this visualization")
        
        import plotly.graph_objects as go
        
        coords, vectors = self._parse_field_data(B_x, B_y, B_z, coordinates)
        
        # Normalize vectors for direction
        magnitudes = np.linalg.norm(vectors, axis=1)
        directions = vectors / (magnitudes[:, np.newaxis] + 1e-10)
        
        # Calculate colors
        if color_by == 'magnitude':
            colors = magnitudes
            colorbar_title = '|B| [T]'
        elif color_by == 'x':
            colors = vectors[:, 0]
            colorbar_title = 'Bx [T]'
        elif color_by == 'y':
            colors = vectors[:, 1]
            colorbar_title = 'By [T]'
        elif color_by == 'z':
            colors = vectors[:, 2]
            colorbar_title = 'Bz [T]'
        else:
            colors = None
            colorbar_title = None
        
        # Build cone parameters
        cone_params = dict(
            x=coords[:, 0],
            y=coords[:, 1],
            z=coords[:, 2],
            u=directions[:, 0] * scale,
            v=directions[:, 1] * scale,
            w=directions[:, 2] * scale,
            colorscale='Viridis',
            sizemode='absolute',
            sizeref=0.5,
        )
        
        # Add color parameters only if colors are specified
        if colors is not None:
            cone_params['cmin'] = colors.min()
            cone_params['cmax'] = colors.max()
            cone_params['colorbar'] = dict(title=colorbar_title)
            # Use magnitude-based sizing/coloring by setting u, v, w appropriately
            # Plotly Cone uses u, v, w magnitude for coloring by default
            cone_params['u'] = vectors[:, 0] * scale
            cone_params['v'] = vectors[:, 1] * scale
            cone_params['w'] = vectors[:, 2] * scale
        
        # Add any additional kwargs
        cone_params.update(kwargs)
        
        # Create cone plot for vectors
        fig = go.Figure(data=go.Cone(**cone_params))
        
        fig.update_layout(
            scene=dict(
                aspectmode='data',
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z'
            ),
            title='Magnetic Field Vectors'
        )
        
        return fig
    
    def plot_matplotlib_2d_vectors(
        self,
        B_x: np.ndarray,
        B_y: np.ndarray,
        B_z: Optional[np.ndarray] = None,
        coordinates: Optional[np.ndarray] = None,
        color_by: Literal['magnitude', 'x', 'y', None] = 'magnitude',
        cmap: str = 'viridis',
        scale: Optional[float] = None,
        ax=None,
        **kwargs
    ):
        """
        Plot 2D magnetic field vectors using Matplotlib.
        
        Args:
            B_x, B_y: 2D field components (required)
            B_z: Optional z-component (used for magnitude calculation)
            coordinates: Optional (N, 2) or (N, 3) array of positions
            color_by: Which component to use for coloring
            cmap: Colormap name
            scale: Scale factor for arrows
            ax: Matplotlib axis object
            **kwargs: Additional arguments for quiver plot
        """
        if not self.has_matplotlib:
            raise ImportError("Matplotlib is required for this visualization")
        
        import matplotlib.pyplot as plt
        
        # Parse data (use zeros for B_z if not provided)
        if B_z is None:
            B_z = np.zeros_like(B_x)
        
        coords, vectors = self._parse_field_data(B_x, B_y, B_z, coordinates)
        
        # Extract 2D components
        x = coords[:, 0]
        y = coords[:, 1]
        u = vectors[:, 0]
        v = vectors[:, 1]
        
        # Calculate colors
        if color_by == 'magnitude':
            colors = np.sqrt(u**2 + v**2)
            label = '|B| [T]'
        elif color_by == 'x':
            colors = u
            label = 'Bx [T]'
        elif color_by == 'y':
            colors = v
            label = 'By [T]'
        else:
            colors = None
            label = None
        
        # Create plot
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8))
        
        if colors is not None:
            quiver = ax.quiver(x, y, u, v, colors, cmap=cmap, scale=scale, **kwargs)
            plt.colorbar(quiver, ax=ax, label=label)
        else:
            quiver = ax.quiver(x, y, u, v, scale=scale, **kwargs)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('2D Magnetic Field')
        ax.set_aspect('equal')
        
        return ax
    
    def plot_matplotlib_2d_colormap(
        self,
        B_x: np.ndarray,
        B_y: np.ndarray,
        B_z: Optional[np.ndarray] = None,
        component: Literal['magnitude', 'x', 'y', 'z'] = 'magnitude',
        cmap: str = 'viridis',
        ax=None,
        **kwargs
    ):
        """
        Plot 2D magnetic field as colormap using Matplotlib.
        
        Args:
            B_x, B_y: 2D field components
            B_z: Optional z-component
            component: Which component to visualize
            cmap: Colormap name
            ax: Matplotlib axis object
            **kwargs: Additional arguments for imshow
        """
        if not self.has_matplotlib:
            raise ImportError("Matplotlib is required for this visualization")
        
        import matplotlib.pyplot as plt
        
        # Ensure inputs are 2D
        B_x = np.asarray(B_x)
        B_y = np.asarray(B_y)
        
        if B_x.ndim != 2 or B_y.ndim != 2:
            raise ValueError("For colormap plot, inputs must be 2D arrays")
        
        if B_z is None:
            B_z = np.zeros_like(B_x)
        else:
            B_z = np.asarray(B_z)
        
        # Calculate scalar field
        if component == 'magnitude':
            field = np.sqrt(B_x**2 + B_y**2 + B_z**2)
            label = '|B| [T]'
        elif component == 'x':
            field = B_x
            label = 'Bx [T]'
        elif component == 'y':
            field = B_y
            label = 'By [T]'
        elif component == 'z':
            field = B_z
            label = 'Bz [T]'
        
        # Create plot
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8))
        
        im = ax.imshow(field, cmap=cmap, origin='lower', aspect='auto', **kwargs)
        plt.colorbar(im, ax=ax, label=label)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'2D Magnetic Field - {label}')
        
        return ax
    
    def plot_current_distribution_2d(
        self,
        J_x: np.ndarray,
        J_y: np.ndarray,
        coordinates: Optional[np.ndarray] = None,
        color_by: Literal['magnitude', 'x', 'y', None] = 'magnitude',
        cmap: str = 'plasma',
        scale: Optional[float] = None,
        ax=None,
        **kwargs
    ):
        """
        Plot 2D current distribution vector field using Matplotlib.
        
        Args:
            J_x, J_y: Current density components
            coordinates: Optional (N, 2) array of positions
            color_by: Which component to use for coloring
            cmap: Colormap name
            scale: Scale factor for arrows
            ax: Matplotlib axis object
            **kwargs: Additional arguments for quiver plot
        """
        if not self.has_matplotlib:
            raise ImportError("Matplotlib is required for this visualization")
        
        import matplotlib.pyplot as plt
        
        # Convert to numpy arrays
        J_x = np.asarray(J_x)
        J_y = np.asarray(J_y)
        J_z = np.zeros_like(J_x)  # Dummy z-component
        
        coords, vectors = self._parse_field_data(J_x, J_y, J_z, coordinates)
        
        # Extract 2D components
        x = coords[:, 0]
        y = coords[:, 1]
        u = vectors[:, 0]
        v = vectors[:, 1]
        
        # Calculate colors
        if color_by == 'magnitude':
            colors = np.sqrt(u**2 + v**2)
            label = '|J| [A/m²]'
        elif color_by == 'x':
            colors = u
            label = 'Jx [A/m²]'
        elif color_by == 'y':
            colors = v
            label = 'Jy [A/m²]'
        else:
            colors = None
            label = None
        
        # Create plot
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8))
        
        if colors is not None:
            quiver = ax.quiver(x, y, u, v, colors, cmap=cmap, scale=scale, **kwargs)
            plt.colorbar(quiver, ax=ax, label=label)
        else:
            quiver = ax.quiver(x, y, u, v, scale=scale, **kwargs)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('2D Current Distribution')
        ax.set_aspect('equal')
        
        return ax


def plot_magnetic_field(
    B_x: np.ndarray,
    B_y: np.ndarray,
    B_z: np.ndarray,
    coordinates: Optional[np.ndarray] = None,
    backend: Literal['pyvista', 'vedo', 'plotly', 'matplotlib'] = 'matplotlib',
    plot_type: Literal['vectors', 'colormap', 'scalar'] = 'vectors',
    **kwargs
):
    """
    Generic function to plot magnetic field data.
    
    This is a convenience function that automatically selects the appropriate
    plotting method based on the backend and plot_type.
    
    Args:
        B_x, B_y, B_z: Magnetic field components
        coordinates: Optional coordinate array
        backend: Visualization backend to use
        plot_type: Type of visualization
        **kwargs: Additional arguments passed to the specific plotting function
        
    Returns:
        The plotter or figure object from the selected backend
        
    Examples:
        # 3D vector plot with PyVista
        >>> plot_magnetic_field(Bx, By, Bz, backend='pyvista', plot_type='vectors')
        
        # 2D colormap with Matplotlib
        >>> plot_magnetic_field(Bx, By, Bz, backend='matplotlib', plot_type='colormap')
        
        # Interactive 3D with Plotly
        >>> fig = plot_magnetic_field(Bx, By, Bz, backend='plotly', plot_type='vectors')
        >>> fig.show()
    """
    viz = MagneticFieldVisualizer()
    
    if backend == 'pyvista':
        if plot_type == 'vectors':
            return viz.plot_pyvista_vectors(B_x, B_y, B_z, coordinates, **kwargs)
        elif plot_type in ['colormap', 'scalar']:
            return viz.plot_pyvista_scalar(B_x, B_y, B_z, coordinates, **kwargs)
        else:
            raise ValueError(f"Unknown plot_type '{plot_type}' for PyVista")
    
    elif backend == 'vedo':
        if plot_type == 'vectors':
            return viz.plot_vedo_vectors(B_x, B_y, B_z, coordinates, **kwargs)
        else:
            raise ValueError(f"Vedo only supports 'vectors' plot type")
    
    elif backend == 'plotly':
        if plot_type == 'vectors':
            return viz.plot_plotly_vectors(B_x, B_y, B_z, coordinates, **kwargs)
        else:
            raise ValueError(f"Plotly only supports 'vectors' plot type currently")
    
    elif backend == 'matplotlib':
        if plot_type == 'vectors':
            return viz.plot_matplotlib_2d_vectors(B_x, B_y, B_z, coordinates, **kwargs)
        elif plot_type == 'colormap':
            return viz.plot_matplotlib_2d_colormap(B_x, B_y, **kwargs)
        else:
            raise ValueError(f"Unknown plot_type '{plot_type}' for Matplotlib")
    
    else:
        raise ValueError(f"Unknown backend '{backend}'")


def plot_current_distribution(
    J_x: np.ndarray,
    J_y: np.ndarray,
    coordinates: Optional[np.ndarray] = None,
    **kwargs
):
    """
    Generic function to plot 2D current distribution.
    
    Args:
        J_x, J_y: Current density components
        coordinates: Optional coordinate array
        **kwargs: Additional arguments passed to the plotting function
        
    Returns:
        Matplotlib axis object
        
    Example:
        >>> plot_current_distribution(Jx, Jy, color_by='magnitude')
    """
    viz = MagneticFieldVisualizer()
    return viz.plot_current_distribution_2d(J_x, J_y, coordinates, **kwargs)
