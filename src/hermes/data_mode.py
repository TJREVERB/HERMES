from enum import Enum


class DataType(Enum):
    BOOT = "BOOT"
    STARTUP = "STARTUP"
    NORMAL = "NORMAL"
    LOW_POWER = "LOW_POWER"
    DANGER = "DANGER"
