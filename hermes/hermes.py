from modules.eps import EPS
from threading import Thread

class Hermes:

    def __init__(self, config):
        self.config = config
        self.submodules = []
        if "EPS" in self.config:
            self.submodules.append(EPS(self.config))


    def run(self):
        print(self.submodules[0].measure_pdms())
        for submodule in self.submodules:
            submodule.run()
