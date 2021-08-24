import os
from shutil import copy
from IPython.display import display

def run_shell(cmd):
    import subprocess
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    o, e = proc.communicate()

    print('Output: ' + o.decode('ascii'))
    print('Error: '  + e.decode('ascii'))
    print('code: ' + str(proc.returncode))

def random_frame(dataset, num_object=0):
    all_flight_ids = dataset.get_flight_ids()

    from random import choice
    flight_id = choice(all_flight_ids)

    flight = dataset.get_flight_by_id(flight_id)

    max_num_objects = len(flight.detected_objects.keys())

    if (num_object > max_num_objects):
        num_object = max_num_objects

    while(True):
        frame_id = choice(list(flight.frames.keys()))
        frame = flight.get_frame(frame_id)

        if (frame.num_detected_objects >= num_object):
            return frame.image_path(), frame

def image_and_annotation(frame):
    frame_image = frame.image(type="cv2")
    frame_image_annotated = frame.image_annotated()

    return frame_image, frame_image_annotated

def plot_image_and_annotation(image, annotated_image, figsize=(50, 65), dpi=80):
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=figsize, dpi=80)
    ax = fig.add_subplot(1, 2, 1)
    ax.imshow(image)
    ax = fig.add_subplot(1, 2, 2)
    ax.imshow(annotated_image)
    plt.show()

def mdprint(text):
    '''
        Display the input text as in Markdown format
    '''
    display({
        'text/markdown': text,
        'text/plain': text
    }, raw=True)