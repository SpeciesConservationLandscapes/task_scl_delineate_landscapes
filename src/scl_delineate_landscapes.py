import argparse
import ee
from datetime import datetime, timezone
from task_base import SCLTask

class SCLDelineateLandscapes(EETask):
    ee_rootdir = "projects/SCL/v1"
    inputs = {
        "countries": {
            "ee_type": SCLTask.FEATURECOLLECTION,
            "ee_path": "USDOS/LSIB/2013",
            "maxage": 10,
        },
        "country_aoi": {
            "ee_type": SCLTask.FEATURECOLLECTION,
            "ee_path": "Panthera_tigris/sumatra_poc_aoi",
            "maxage": 10,
        },
        "structural_habatat": {
            "ee_type": EETask.IMAGECOLLECTION,
            "ee_path": "Panthera_tigris/geographies/Sumatra/hab/structural_habitat",
            "maxage": 1  # years
        },
        "hii": {
            "ee_type": EETask.IMAGECOLLECTION,
            "ee_path": "projects/HII/v1/sumatra_poc/final/weighted_hii",
            "maxage": 1  # years
        },
        "elevation": {
            "ee_type": EETask.IMAGE,
            "ee_path": "CGIAR/SRTM90_V4",
            "maxage": 10  # years
        },
        "historic_range": {
            "ee_type": EETask.IMAGE,
            "ee_path": "Panthera_tigris/source/Inputs_2006/hist",
            "maxage": 10  # years
        },
        "extirpated_range": {
            "ee_type": EETask.IMAGE,
            "ee_path": "Panthera_tigris/source/Inputs_2006/extirp_fin",
            "maxage": 10  # years
        },
        "density": {
            "ee_type": EETask.IMAGE,
            "ee_path": "Panthera_tigris/source/Inputs_2006/density",
            "maxage": 10  # years
        },
        "water_mask": {
            "ee_type": EETask.IMAGE,
            "ee_path": "projects/HII/v1/source/phys/watermask_jrc70_cciocean",
            "maxage": 10  # years
        }
        }

        thresholds = {
            'structural_lc': 50,
            'elevation': 3350,
            'structural_patch': 5,
            'hii': 35,
            'probability': 0.4
        }
        
print(self.thersholds.elevation)
