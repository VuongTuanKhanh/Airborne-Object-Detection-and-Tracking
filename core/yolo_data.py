import shutil, os
from helper import *

class Yolo_Data:
    
    def __init__(self):
        self.image_paths = []
        self.yolo_locations = []
        self.original_paths = []

        working_directory = "/content/drive/MyDrive/Airborne-Object-Tracking/"
        
        if os.getcwd() != working_directory:
            os.chdir(working_directory)

        if not os.path.exists(self.training_path):
            os.mkdir(self.training_path)


    def get_frame(self, dataset, path):
        import re
        flight_name, timestamp, flight_name_2 = re.match(r'(\w+)/(\w{19})(\w+).png', path, re.S).groups()
        assert flight_name == flight_name_2

        flight = dataset.get_flight_by_id(flight_name)

        return [flight.get_frame(frame_id) for frame_id in flight.frames if flight.get_frame(frame_id).timestamp == int(timestamp)][0]


    def get_frame_and_path(self, dataset, folder_path, folder_name, image):
        import os

        image_path = os.path.join(folder_path, image)
        curr_image = self.get_frame(dataset, os.path.join(folder_name, image))

        return image_path, curr_image

    
    def get_frame_info(self, frame, airborne_object):
        bounding_box = frame.detected_object_locations[airborne_object].bb.get_bbox()
        img_width = frame.flight.metadata.resolution.width
        img_height = frame.flight.metadata.resolution.height
        center = frame.detected_object_locations[airborne_object].bb.get_center()

        return bounding_box, img_width, img_height, center


    def norm(self, center, width_height, img_width, img_height):
        return [float(center[0])/img_width, float(center[1])/img_height,
            float(width_height[0])/img_width, float(width_height[1])/img_height]

    
    def get_yolo(self, center, bounding_box, img_width, img_height):
        yolo_value = self.norm(center, bounding_box[2:], img_width, img_height)
        yolo_format = " ".join([str(int) for int in [0] + yolo_value])

        return yolo_value, yolo_format


    def get_yolo_locations(self, frame):
        yolo_locations = []

        for airborne_object in frame.detected_object_locations:
            bounding_box, img_width, img_height, center = self.get_frame_info(frame, airborne_object)       
            yolo_value, yolo_format = self.get_yolo(center, bounding_box, img_width, img_height)
            yolo_locations.append(yolo_format)
        
        return yolo_locations


    def write_yolo_labels(self, path, yolo_locations):
        with open(path, 'w') as text_file:
            newline = ""
            for yolo_location in yolo_locations:
                text_file.write(newline + yolo_location)
                newline = "\n"

    
    def generate_labels(self):
        for yolo_location in self.yolo_locations:
            file_name, yolo_values = list(yolo_location.items())[0]
            self.write_yolo_labels(os.path.join(self.training_path, file_name), yolo_values)

    
    def generate_images(self):
        for original_path in self.original_paths:
            copy(original_path, self.training_path)
            
    
    def generate_data(self, dataset, generate_images = True, generate_labels = True):
        iter = total_object = 0

        for source_path in self.source_paths:
            print("Iterating through " + source_path)
            for folder in os.listdir(source_path):
                folder_path = os.path.join(source_path, folder)
                
                for image in os.listdir(folder_path):

                    image_path = os.path.join(folder_path, image)
                    image_path, curr_image = self.get_frame_and_path(dataset, folder_path, folder, image)
                    
                    number_of_objects = curr_image.num_detected_objects
                    if number_of_objects >= self.objects_per_frame:
                        iter = iter + 1
                        self.image_paths.append(os.path.join(self.relative_path, image))
                        self.original_paths.append(image_path)
                        self.yolo_locations.append(
                            {
                                str(image).replace(".png", ".txt"): self.get_yolo_locations(curr_image)
                            }
                        )
                        total_object += number_of_objects

        if generate_images:
            self.generate_images()

        if generate_labels:
            self.generate_labels()
        
        self.write_data_files()


        print("Finish Generating !!! Total of {} images and {} objects".format(iter, total_object))

    
    def train_test_split(self, percent=80):
        if percent > 100:
            percent = 100
        percent_split = int(len(self.image_paths) * percent/100)

        return self.image_paths[percent_split:], self.image_paths[:percent_split:]


    def write_file(self, path, data):
        if os.path.exists(path):
            os.remove(path)

        with open(path, "w") as text_file:
            newline = ""
            for line in data:
                text_file.write(newline + line)
                newline = "\n"


    def write_data_files(self):
        train, test = self.train_test_split()

        self.write_file(self.train_txt, train)
        print("Generating train.txt")
        self.write_file(self.test_txt, test)
        print("Generating test.txt")
        self.write_file(self.original_txt, self.original_paths)
        print("Generating original_paths.txt")


    @property
    def objects_per_frame(self):
        return 2
    
    @property
    def relative_path(self):
        return "./data/images"
        
    @property
    def training_path(self):
        return "./darknet/data/images"

    @property
    def train_txt(self):
        return "./darknet/data/train.txt"

    @property
    def test_txt(self):
        return "./darknet/data/test.txt"

    @property
    def original_txt(self):
        return "./darknet/data/original_paths.txt"
    
    @property
    def source_paths(self):
        return ["./data/part1/Images", "./data/part2/Images", "./data/part3/Images"]