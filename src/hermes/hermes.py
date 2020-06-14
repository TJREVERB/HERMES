import sys
import time
from enum import Enum
from threading import Thread

from .modules.eps import EPS


class Generator(Enum):
    BOOT = "BOOT"
    STARTUP = "STARTUP"
    NORMAL = "NORMAL"
    LOW_POWER = "LOW_POWER"
    DANGER = "DANGER"


class Hermes:

    def __init__(self, config, mcl):
        self.config = config
        self.submodules = {}
        self.registry = {
            "EPS_ON": True,
            "PI_ON": True,
            "APRS_ON": True,
            "ANTENNA_DEPLOYER_ON": True,
            "IRIDIUM_ON": True
        }
        self.mcl = mcl
        generator = Generator(config['generator'])
        if "EPS" in self.config:
            self.submodules["EPS"] = EPS(self.config, self.registry, generator)

    def control(self):
        while True:
            if not self.registry["PI_ON"]:
                # TODO: Somehow simulate a reboot (requires restarting MCL)
                raise Exception("Pi turned off!")
                sys.exit(0)

            for submodule in self.submodules:
                # If the submodule should be off but is currently on, turn it off
                if not self.registry[submodule + "_ON"] and not self.submodules[submodule].terminated:
                    self.terminate(submodule)
                # If the submodule should be on but is currently off, restart it
                elif self.registry[submodule + "_ON"] and not self.submodules[submodule].terminated:
                    self.reset(submodule)

    def terminate(self, submodule):
        if submodule not in self.submodules:
            print(f"Submodule {submodule} not found!")
            return

        self.submodules[submodule].terminated = True

    def activate(self, submodule):
        if submodule not in self.submodules:
            print(f"Submodule {submodule} not found!")
            return

        self.submodules[submodule].terminated = False

    def reset(self, submodule):
        if submodule not in self.submodules:
            print(f"Submodule {submodule} not found!")
            return

        self.submodules[submodule].terminated = True
        time.sleep(self.config[submodule]["reset_time"])
        self.submodules[submodule].terminated = False
        self.submodules[submodule].reset()

    def shift_mode(self, mode: Generator):
        for submodule in self.submodules:
            self.submodules[submodule].shift_mode(mode)

    def run_action(self, submodule, name):
        if submodule not in self.submodules:
            print(f"Submodule {submodule} not found!")
            return

        self.submodules[submodule].run_action(name)

    def run(self):
        for name in self.submodules:
            submodule = self.submodules[name]
            sub_thread = Thread(target=submodule.run)
            sub_thread.daemon = True
            sub_thread.start()
