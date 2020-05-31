import sys
import json
import time
import argparse
from hermes import Hermes
from threading import Thread


def hermes_thread(hermes):
    while True:
        time.sleep(0.1)
        hermes.run()



def ingest(inp):
    print(inp)


def main():
#    parser = argparse.ArgumentParser(description="Pass some arguments")
#    parser.add_argument('--live', dest='live', const=True, default=False, nargs='*')
#    args = parser.parse_args()
    config = json.load(open("config.json"))
    hermes = Hermes(config)
    thread = Thread(target=hermes_thread, args=(hermes,))
    thread.daemon = True
    thread.start()

    while True:
        if True:
#        if args.live:
            inp = input()
            ingest(inp)


if __name__ == '__main__':
    main()
