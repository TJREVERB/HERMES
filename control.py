from modules.eps import EPS

class ControlHandler:

    def __init__(self, config):
        self.config = config
        self.submodules = {}
        if "EPS" in self.config:
            self.submodules["EPS"] = EPS(self.config)


    def run(self, data):
        print(self.submodules["EPS"].pdm_states)
        for key in self.submodules:
            submodule = self.submodules[key]
            submodule.ingest(data[key])

        output = {}
        for key in self.submodules:
            submodule = self.submodules[key]
            if submodule.return_data:
                output[key] = submodule.return_data
            else:
                output[key] = ""
        return output
