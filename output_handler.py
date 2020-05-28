# Handler for giving output to drivers
class OutputHandler:

    def __init__(self, config):
        self.config = config
        self.data = {}


    def update_data(self):
        for subprocess in self.config:
            self.read_file(subprocess)


    def read_file(self, subprocess):
        filepath = self.config[subprocess]["filepath"]
        # Read data in file
        file = open(filepath, "r")
        data = file.read()
        file.close()
        # Clear any data that's in there
        file = open(filepath, "w")
        file.write("")
        file.close()
        self.data[subprocess] = data

