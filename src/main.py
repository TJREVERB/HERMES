import sys, os
# Add MCL to path so that we can import it
sys.path.append(os.path.abspath(os.path.join('../..', 'pfs')))

import json
import time
import argparse
from threading import Thread

from hermes import Hermes
from MainControlLoop.main_control_loop import MainControlLoop


def mcl_thread(mcl):
    while True:
        mcl.execute()


def ingest(inp):
    print(inp)


def main():
#    parser = argparse.ArgumentParser(description="Pass some arguments")
#    parser.add_argument('--live', dest='live', const=True, default=False, nargs='*')
#    args = parser.parse_args()
    config = json.load(open("config.json"))
    hermes = Hermes(config)
    hermes.run()
    mcl = MainControlLoop()
    thread = Thread(target=mcl_thread, args=(mcl,))
    thread.daemon = True
    thread.start()

    while True:
        if True:
#        if args.live:
            inp = input()
            ingest(inp)


if __name__ == '__main__':
    main()
