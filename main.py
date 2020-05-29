import sys
import json
import time
from enum import Enum
from control import ControlHandler


class SimulationModes(Enum):
    BOOT = "BOOT"
    STARTUP = "STARTUP"
    NORMAL = "NORMAL"
    COMMS = "COMMS"
    LOW = "LOW"
    POWER = "POWER"
    BOOT_STARTUP = "BOOT_STARTUP"
    STARTUP_NORMAL = "STARTUP_NORMAL"
    NORMAL_LOWPOWER = "NORMAL_LOWPOWER"
    LOWPOWER_NORMAL = "LOWPOWER_NORMAL"
    NORMAL_COMMS = "NORMAL_COMMS"
    COMMS_NORMAL = "COMMS_NORMAL"
    BOOT_SAFE = "BOOT_SAFE"
    STARTUP_SAFE = "STARTUP_SAFE"
    NORMAL_SAFE = "NORMAL_SAFE"
    COMMS_SAFE = "COMMS_SAFE"
    LOWPOWER_SAFE = "LOWPOWER_SAFE"


def main():
    config = json.load(open("config.json"))
    controller = ControlHandler(config)
    while True:
        time.sleep(0.1)
        controller.run()


if __name__ == '__main__':
    main()
