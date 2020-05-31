import os
import sys
import json
import argparse
from hermes import Hermes
from threading import Thread


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Add MCL to path so that we can import it
sys.path.append(os.path.abspath(os.path.join('../..', 'pfs')))

try:
    from MainControlLoop import main_control_loop as mcl
except ImportError:
    raise RuntimeError("Unable to import pFS Main Control Loop, are you in the pFS directory?")


def mcl_thread(mcl):
    while True:
        mcl.execute()


def ingest(inp):
    print(inp)


def run_tests():
    print('running tests')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="HERMES configuration file", )
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.load(f)

    hermes = Hermes(config)
    hermes.run()
    mcl = MainControlLoop()
    thread = Thread(target=mcl_thread, args=(mcl,))
    thread.daemon = True
    thread.start()

    if sys.flags.interactive:
        while True:
            inp = input()
            ingest(inp)
    else:
        run_tests()


if __name__ == '__main__':
    main()
