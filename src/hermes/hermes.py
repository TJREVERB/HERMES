import sys
import time
from threading import Thread
from hermes.modules.eps import EPS

class Hermes:

    def __init__(self, config):
        self.config = config
        self.submodules = []
        self.registry = {
            "EPS_ON": True,
            "PI_ON": True,
            "ADCS_ON": True,
            "ANTENNA_DEPLOYER_ON": True,
            "IRIDIUM_ON": True
        }
        self.running = []
        if "EPS" in self.config:
            self.submodules["EPS"] = EPS(self.config, self.registry)


    def control(self):
        while True:
            if not self.registry["PI_ON"]:
                # TODO: Somehow simulate a reboot (requires restarting MCL)
                raise Exception("Pi turned off!")
                sys.exit(0)
            for submodule in self.submodules:
                # If the submodule should be off but is currently on, turn it off
                if not self.registry[submodule + "_ON"] and not self.submodules[submodule].terminated:
                    self.turn_off(submodule)
                # If the submodule should be on but is currently off, restart it
                elif self.registry[submodule + "_ON"] and not self.submodules[submodule].terminated:
                    self.reset(submodule)
                    

    def turn_off(self, submodule):
        if submodule not in self.submodules:
            print("Submodule {} not found!".format(submodule))
        self.submodules[submodule].terminated = True


    def turn_on(self, submodule):
        if submodule not in self.submodules:
            print("Submodule {} not found!".format(submodule))
        self.submodules[submodule].terminated = False


    def reset(self, submodule):
        if submodule not in self.submodules:
            print("Submodule {} not found!".format(submodule))
        self.submodules[submodule].terminated = True
        time.sleep(self.config[submodule]["reset_time"])
        self.submodules[submodule].terminated = False
        self.submodules[submodule].reset()


    def run(self):
        for submodule in self.submodules:
            sub_thread = Thread(target=submodule.run)
            sub_thread.daemon = True
            sub_thread.start()
            self.running.append(submodule)
