from .modules.eps import EPS
from threading import Thread

class Hermes:

    def __init__(self, config):
        self.config = config
        self.submodules = []
        if "EPS" in self.config:
            self.submodules.append(EPS(self.config))


    def run(self):
        for submodule in self.submodules:
            sub_thread = Thread(target=submodule.run)
            sub_thread.daemon = True
            sub_thread.start()
