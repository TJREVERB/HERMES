from modules.eps import EPS

class ControlHandler:

    def __init__(self, config):
        self.config = config
        self.submodules = {}
        if "EPS" in self.config:
            self.submodules["EPS"] = EPS(self.config)


    def run(self, data):
        for submodule in self.submodules:
            if data[submodule]:
                submodule.ingest(*data[submodule])

        output = {}
        for submodule in self.submodules:
            if submodule.return_data:
                output[submodule] = submodule.return_data
            else:
                output[submodule] = ""
