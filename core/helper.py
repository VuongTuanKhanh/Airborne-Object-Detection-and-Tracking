import os
import sys
import random
from core.dataset import Dataset
from IPython.display import display


def initialize(random_seed=0):
    """Initialize the system paths and random seed value

    Args:
        random_seed (int, optional): The random seed value. Defaults to 0.
    """

    # Add current working directory to the root path
    sys.path.append(os.path.dirname(os.path.realpath(os.getcwd())))
    # Add core library to the root path
    sys.path.append(os.path.dirname(os.path.realpath(os.getcwd())) + "/core")
    # Initialize random value
    random.seed(random_seed)


def load_data(partial=True, prefixs=['/part1', '/part2', '/part3'], s3_path='s3://airborne-obj-detection-challenge-training'):
    """Loading the original dataset

    Args:
        partial (bool, optional): Loading the entire dataset or a part of it. Defaults to True.
        prefixs (list, optional): A list of dataset that need to be loaded. Defaults to ['/part1', '/part2', '/part3'].
        s3_path (str, optional): Aws online path to the dataset. Defaults to 's3://airborne-obj-detection-challenge-training'.

    Returns:
        dataset (object): An instance of the Dataset object
    """
    notebook_path = os.path.dirname(os.path.realpath("__file__")) + '/data'
    dataset = Dataset(partial)

    for prefix in prefixs:
        path = notebook_path + prefix
        dataset.add(path, s3_path + prefix, prefix)

    return dataset


def run_shell(cmd):
    """Execute a Shell command on Python

    Args:
        cmd (str): A specific Shell command that need to be execute in the Python enviroment
    """
    import subprocess
    # Create a sub process
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    # Get the output and error
    o, e = proc.communicate()
    # Print out the result
    print('Output: ' + o.decode('ascii'))
    print('Error: ' + e.decode('ascii'))
    print('code: ' + str(proc.returncode))


def random_frame(dataset, num_object=0):
    """Get a random frame from dataset

    Args:
        dataset (object): An instance of the Dataset object
        num_object (int, optional): Number of detected objects per frame. Defaults to 0.

    Returns:
        image_path (str): A string that represent the path to the image
        frame (object): An instance of the Frame object
    """

    # Get all of the flight ids
    all_flight_ids = dataset.get_flight_ids()

    from random import choice
    # Choose a random flight id
    flight_id = choice(all_flight_ids)

    # Get the random flight
    flight = dataset.get_flight_by_id(flight_id)

    # Verify the maximum number of detected_objects
    max_num_objects = len(flight.detected_objects.keys())

    # Update the number of detected objects
    if (num_object > max_num_objects):
        num_object = max_num_objects

    # Finding a suitable flight
    while(True):
        frame_id = choice(list(flight.frames.keys()))
        frame = flight.get_frame(frame_id)

        if (frame.num_detected_objects >= num_object):
            return frame.image_path(), frame


def image_and_annotation(frame):
    """Return a specific frame images and it's annotated version

    Args:
        frame (object): An instance of the Frame object

    Returns:
        frame_image (object): An instance of Frame image
        frame_image_annotated: An instance of Frame image with annotation
    """

    # Get the image
    frame_image = frame.image(type="cv2")
    # Get the annotated image
    frame_image_annotated = frame.image_annotated()

    # Return the two versions
    return frame_image, frame_image_annotated


def plot_image_and_annotation(image, annotated_image, figsize=(50, 65), dpi=80):
    """Plot the image and it's annotated version to the figure

    Args:
        image (object): The original version of the image
        annotated_image (object): The annotated version of the image
        figsize (tuple, optional): Width and height size for the image. Defaults to (50, 65).
        dpi (int, optional): DPI configuration for the figure. Defaults to 80.
    """

    import matplotlib.pyplot as plt

    # Define the figre instance
    fig = plt.figure(figsize=figsize, dpi=80)
    # Add the first subplot
    ax = fig.add_subplot(1, 2, 1)
    # Show the first image
    ax.imshow(image)
    # Add the second subplot
    ax = fig.add_subplot(1, 2, 2)
    # Show the second image
    ax.imshow(annotated_image)
    # Display the figure
    plt.show()


def mdprint(text):
    """Display the input text as in Markdown format

    Args:
        text (str): A text that need to be displayed in other formats

    """
    display({
        'text/markdown': text,
        'text/plain': text
    }, raw=True)
