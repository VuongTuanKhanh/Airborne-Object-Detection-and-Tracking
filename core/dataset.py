#!/usr/bin/env python3
import os
import json
from loguru import logger
from core.flight import Flight
from core.file_handler import FileHandler


class Dataset:
    # Metadata of the Dataset. This will be defined by the groundtruth metadata
    metadata = None
    # List of flights
    flights = {}

    def __init__(self, local_path=None, s3_path=None, download_if_required=True, partial=False, prefix=None):
        '''
            Generate an empty Dictionary to store all the Flights
        '''
        self.file_handler = None
        self.partial = partial
        # A dictionary of valid encounter only
        self.valid_encounter = {}

    def load_gt(self):
        '''
            Load ground truth folder
        '''
        logger.info("Loading ground truth...")
        # Get the hold content of valid encounter base on gt_loc
        gt_content = self.file_handler.get_file_content(self.gt_loc)
        # Load the json format of the grouth truth folder
        gt = json.loads(gt_content)

        # Assign dataset.metadata
        self.metadata = gt["metadata"]
        # Iterate through every flight
        for flight_id in gt["samples"].keys():
            # Copy the original flight id
            flight_id_with_prefix = flight_id
            # Assign this flight to the data part prefix if available
            if self.prefix:
                flight_id_with_prefix = self.prefix + flight_id
            # Skipping this flight if it is not belong to the partial part
            if self.partial and flight_id not in self.valid_encounter:
                # Print out the flight id
                logger.info("Skipping flight, not present in valid encounters: %s" % flight_id)
                continue
            # Push this flight to the dataset flights list
            self.flights[flight_id_with_prefix] = Flight(flight_id_with_prefix, gt["samples"][flight_id], self.file_handler, self.valid_encounter.get(flight_id), prefix=self.prefix)

    def load_ve(self):
        '''
            Load valid encounter folder
        '''
        # Consider only if partial = True
        if self.partial:
            logger.info("Loading valid encounters...")
            # Get the hold content of valid encounter base on valid_encounters_loc
            ve = self.file_handler.get_file_content(self.valid_encounters_loc)

            # For every valid encounter in valid_encounters_loc
            for valid_encounter in ve.split('\n\n    '):
                # Loads the json format of the encounter
                valid_encounter = json.loads(valid_encounter)
                # Create a list to store the information for that specific encounter id
                if valid_encounter["flight_id"] not in self.valid_encounter:
                    # Create a new list if we haven't have that encounter
                    self.valid_encounter[valid_encounter["flight_id"]] = []
                self.valid_encounter[valid_encounter["flight_id"]].append(valid_encounter)

    def add(self, local_path, s3_path, download_if_required=True, prefix=None):
        '''
            Add a specific part to the dataset
        '''
        # Set up the dataset prefix
        self.prefix = prefix
        # Create file handler instance
        self.file_handler = FileHandler(local_path, s3_path, download_if_required)
        # Load valid encounter. Available only if partial=True
        self.load_ve()
        # Load groundtruth
        self.load_gt()

    def get_flight_ids(self):
        '''
            Return the list of all flight ids
        '''
        return list(self.flights.keys())

    @property
    def gt_loc(self):
        return 'ImageSets/groundtruth.json'

    @property
    def valid_encounters_loc(self):
        '''
            Return the path to the valid encounter folder
        '''
        return 'ImageSets/valid_encounters_maxRange700_maxGap3_minEncLen30.json'

    def get_flight_by_id(self, flight_id):
        '''
            Return the flight at a specific id in the dataset list
        '''
        return self.flights[flight_id]

    def get_flight(self, flight_id):
        return self.get_flight_by_id(flight_id)

    def __str__(self):
        return "Dataset(num_flights=%s)" % (len(self.flights))


if __name__ == "__main__":
    local_path = '/Users/skbly7/Terminal/aicrowd/repos/airborne-detection-starter-kit/data'
    s3_path = 's3://airborne-obj-detection-challenge-training/part1/'
    dataset = Dataset(local_path, s3_path)
    print(dataset.flights)
