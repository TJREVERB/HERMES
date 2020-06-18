from enum import Enum


class Generator(Enum):
    BOOT = "BOOT"
    STARTUP = "STARTUP"
    NORMAL = "NORMAL"
    LOW_POWER = "LOW_POWER"
    DANGER = "DANGER"
