import sys
import time
from threading import Thread

from .modules import APRS, EPS, Generator, Iridium


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

        if "EPS" in self.config['modules']:
            self.submodules["EPS"] = EPS(self.config, self.registry, generator)

        if "APRS" in self.config['modules']:
            self.submodules["APRS"] = APRS(self.config, mcl, generator)

        if "IRIDIUM" in self.config['modules']:
            self.submodules["IRIDIUM"] = Iridium(self.config, mcl, generator)

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
        time.sleep(self.config["modules"][submodule]["reset_time"])
        self.submodules[submodule].terminated = False
        self.submodules[submodule].reset()

    def change_generator(self, generator: Generator):
        for submodule in self.submodules:
            self.submodules[submodule].change_generator(generator)

    def run_action(self, submodule, name):
        if submodule != 'HERMES':
            print(f"Attempting to execute action {name} in submodule {submodule}")
            if submodule not in self.submodules:
                print(f"Submodule {submodule} not found!")
                return

            self.submodules[submodule].run_action(name)
            return

        print("HERMES actions not built yet")

    def send(self, radio, command):
        if radio != 'aprs' and radio != 'iridium':
            print(f"Radio `{radio}` is not available, please use either aprs or iridium")
            return

        if radio.upper() not in self.submodules:
            print(f"Submodule {radio.upper()} not found!")
            return

        if "\n" != command[-1]:
            command += "\n"

        self.submodules[radio.upper()].send(command)

    def run(self):
        for name in self.submodules:
            submodule = self.submodules[name]
            sub_thread = Thread(target=submodule.run)
            sub_thread.daemon = True
            sub_thread.start()
