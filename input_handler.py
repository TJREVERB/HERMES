# Handler for giving input to drivers
class InputHandler:

    def __init__(self, config):
        self.config = config
        self.data = {}


    def update_file(self, subprocess, data):
        filepath = self.config[subprocess]["filepath"]
        file = open(filepath, "w+")
        file.write(data)
        file.close()


    def set_data(self, subprocess, data):
        self.data[subprocess] = data
        self.update_file(subprocess, data)
