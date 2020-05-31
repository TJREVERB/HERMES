import sys
import json
import time
from enum import Enum
from hermes import Hermes


def main():
    config = json.load(open("config.json"))
    hermes = Hermes(config)
    while True:
        time.sleep(0.1)
        hermes.run()


if __name__ == '__main__':
    main()
