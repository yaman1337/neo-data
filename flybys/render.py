import pathlib
import sys
import pandas as pd
import numpy as np
import imageio
from tqdm import tqdm
import visvis as vv
from PyQt5.QtWidgets import QWidget, QHBoxLayout

# Define a class for the main window
class MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.fig = vv.backends.backend_pyqt5.Figure(self)
        self.sizer = QHBoxLayout(self)
        self.sizer.addWidget(self.fig._widget)
        self.setLayout(self.sizer)
        self.setWindowTitle("3D Shape Model Viewer")
        self.show()

# Define a function to download the shape model if it's not already present
def download_shape_model(dl_path, model_filename, model_url):
    """
    Downloads the shape model if it's not already present in the local path.

    Parameters
    ----------
    dl_path : str
        Local path to store the model file.
    model_filename : str
        Filename of the model (e.g., .OBJ if .BDS convert using dskexp.exe from SPICE).
    model_url : str
        URL from where the model will be downloaded.

    Raises
    ------
    PermissionError
        If there is a permission error while downloading the file.
    """
    if not pathlib.Path(f"{dl_path}/{model_filename}").is_file():
        data_fetch.download_file(dl_path, model_url)

# Define a function to load the shape model and extract vertices and faces
def load_shape_model(filepath):
    """
    Loads the shape model and extracts vertices and faces.

    Parameters
    ----------
    filepath : str
        Full file path of the shape model file.

    Returns
    -------
    tuple
        A tuple containing:
        - vertices (list of list of float): List of vertex coordinates.
        - faces (list of list of int): List of face indices.

    Raises
    ------
    FileNotFoundError
        If the file specified by `filepath` does not exist.
    ValueError
        If the file format is incorrect or cannot be parsed.
    """
    shape_model = pd.read_csv(filepath, delim_whitespace=True, names=["TYPE", "X1", "X2", "X3"])

    # Extract vertices and faces
    vertices = shape_model.loc[shape_model["TYPE"] == "v"][["X1", "X2", "X3"]].values.tolist()
    faces = shape_model.loc[shape_model["TYPE"] == "f"][["X1", "X2", "X3"]].values - 1  # Adjust indexing to start from 0
    faces = faces.astype(int).tolist()

    return vertices, faces

# Define a function to visualize the 3D shape model
def visualize_shape_model(vertices, faces, azimuth=120, elevation=25):
    """
    Visualizes the 3D shape model using visvis.

    Parameters
    ----------
    vertices : list of list of float
        List of vertex coordinates.
    faces : list of list of int
        List of face indices.
    azimuth : int, optional
        Initial azimuth angle. Defaults to 120.
    elevation : int, optional
        Initial elevation angle. Defaults to 25.

    Raises
    ------
    ValueError
        If vertices or faces are not in the correct format.
    """
    # Create visvis application
    app = vv.use()
    app.Create()

    # Create main window frame
    main_w = MainWindow()
    main_w.resize(500, 400)

    # Create the 3D shape model as a mesh
    vv.mesh(vertices=vertices, faces=faces, verticesPerFace=3)

    # Customize the axes settings
    axes = vv.gca()
    axes.bgcolor = "black"
    axes.axis.showGrid = False
    axes.axis.visible = False
    axes.camera = "3d"
    axes.camera.fov = 60
    axes.camera.azimuth = azimuth
    axes.camera.elevation = elevation

    # Run the application
    app.Run()

# Define a function to create an animation GIF of the model's rotation
def create_animation(vertices, faces, output_gif_name, steps=360, duration=0.04):
    """
    Creates an animated GIF of the 3D model rotating.

    Parameters
    ----------
    vertices : list of list of float
        List of vertex coordinates.
    faces : list of list of int
        List of face indices.
    output_gif_name : str
        Name of the output GIF file.
    steps : int, optional
        Number of rotation steps. Defaults to 360.
    duration : float, optional
        Duration of each frame in the GIF. Defaults to 0.04.

    Raises
    ------
    ValueError
        If vertices or faces are not in the correct format.
    IOError
        If there is an error saving the GIF file.
    """
    # Create visvis application
    app = vv.use()
    app.Create()

    # Create main window frame and set a resolution for the animation
    main_w = MainWindow()
    main_w.resize(500, 400)

    # Create the 3D shape model as a mesh
    shape_obj = vv.mesh(vertices=vertices, faces=faces, verticesPerFace=3)
    shape_obj.specular = 0.0
    shape_obj.diffuse = 0.9

    # Get figure and customize camera settings
    figure = vv.gcf()
    axes = vv.gca()
    axes.bgcolor = (0, 0, 0)
    axes.axis.showGrid = False
    axes.axis.visible = False
    axes.camera = "3d"
    axes.camera.fov = 60
    axes.camera.zoom = 0.1
    axes.light0.Off()
    light_obj = axes.lights[1]
    light_obj.On()
    light_obj.position = (5.0, 5.0, 5.0, 0.0)

    # Empty array that will store all images of the comet's rotation
    comet_images = []

    # Rotate camera and capture images
    for azm_angle in tqdm(range(steps)):
        axes.camera.azimuth = float(azm_angle)
        axes.Draw()
        figure.DrawNow()
        temp_image = vv.getframe(vv.gca())
        comet_images.append((temp_image * 255).astype(np.uint8))

    # Save the images as an animated GIF
    imageio.mimsave(output_gif_name, comet_images, duration=duration)

# Main reusable function to handle everything
def render_meteorite_model(dl_path, model_filename, model_url, output_gif_name, steps=360, duration=0.04):
    """
    Renders a 3D model of a meteorite and creates an animation GIF of its rotation.

    Parameters
    ----------
    dl_path : str
        Local path where the model will be downloaded.
    model_filename : str
        Filename of the 3D model.
    model_url : str
        URL of the 3D model.
    output_gif_name : str
        Name of the output GIF file.
    steps : int, optional
        Number of rotation steps for the animation. Defaults to 360.
    duration : float, optional
        Duration of each frame in the GIF. Defaults to 0.04.

    Raises
    ------
    FileNotFoundError
        If the model file cannot be downloaded or found.
    ValueError
        If the model file cannot be parsed correctly.
    IOError
        If there is an error saving the GIF file.
    """
    # Download the model if it's not present
    download_shape_model(dl_path, model_filename, model_url)

    # Load the shape model
    vertices, faces = load_shape_model(f"{dl_path}/{model_filename}")
    visualize_shape_model(vertices, faces)
    create_animation(vertices, faces, output_gif_name, steps, duration)


# reusable function
render_meteorite_model(
    dl_path="../kernels/dsk/",
    model_filename="PHOBOS_K275_DLR_V02.OBJ",
    model_url="https://naif.jpl.nasa.gov/pub/naif/ROSETTA/kernels/dsk/",
    output_gif_name=f"../render/phobo.gif"
)
