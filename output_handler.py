# Handler for giving output to drivers
import json

class OutputHandler:

    def __init__(self, config):
        self.config = config
        self.data = {}
        for subprocess in self.config:
            filepath = self.config[subprocess]["output_filepath"]
            open(filepath, "w+").close()


    def update_file(self, subprocess, data):
        filepath = self.config[subprocess]["output_filepath"]
        file = open(filepath, "w+")
        file.write(data)
        file.close()


    def set_data(self, subprocess, data):
        self.data[subprocess] = data
        self.update_file(subprocess, data)
