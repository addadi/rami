# family_config.py
import json


class FamilyConfig:
    @staticmethod
    def read_family_config(file_path):
        with open(file_path, "r") as file:
            family_config_data = json.load(file)
        return family_config_data
