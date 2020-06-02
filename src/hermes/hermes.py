import sys
import time
from threading import Thread

from .modules.eps import EPS
from .data_mode import DataType


class Hermes:

    def __init__(self, config):
        self.config = config
        self.submodules = {}
        self.registry = {
            "EPS_ON": True,
            "PI_ON": True,
            "ADCS_ON": True,
            "ANTENNA_DEPLOYER_ON": True,
            "IRIDIUM_ON": True
        }
        starting_data_type = DataType(config['starting_data_type'])
        if "EPS" in self.config:
            self.submodules["EPS"] = EPS(self.config, self.registry, starting_data_type)

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
            print(f"Submodule {submodule} not found!")
        self.submodules[submodule].terminated = True

    def turn_on(self, submodule):
        if submodule not in self.submodules:
            print(f"Submodule {submodule} not found!")
        self.submodules[submodule].terminated = False

    def reset(self, submodule):
        if submodule not in self.submodules:
            print(f"Submodule {submodule} not found!")

        self.submodules[submodule].terminated = True
        time.sleep(self.config[submodule]["reset_time"])
        self.submodules[submodule].terminated = False
        self.submodules[submodule].reset()

    def shift_mode(self, mode: DataType):
        for submodule in self.submodules:
            self.submodules[submodule].shift_mode(mode)

    def run(self):
        for name in self.submodules:
            submodule = self.submodules[name]
            sub_thread = Thread(target=submodule.run)
            sub_thread.daemon = True
            sub_thread.start()
