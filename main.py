import sys
from enum import Enum


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


while True:
    input_handler.update_data()
    output = controller.run(input_handler.data)
    for subprocess in output:
        output_handler.set_data(subprocess, output[subprocess])


if __name__ == '__main__':
    main()
