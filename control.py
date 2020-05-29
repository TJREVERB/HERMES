from modules.eps import EPS

class ControlHandler:

    def __init__(self, config):
        self.config = config
        self.submodules = []
        if "EPS" in self.config:
            self.submodules.append(EPS(self.config))


    def run(self):
        print(self.submodules[0].pdm_states)
        for submodule in self.submodules:
            submodule.run()
