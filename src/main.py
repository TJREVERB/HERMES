import os
import sys
import json
import argparse

from hermes import Hermes

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    from MainControlLoop import main_control_loop as mcl
except ImportError:
    raise RuntimeError("Unable to import pFS Main Control Loop, are you in the pFS directory?")



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="HERMES configuration file",)
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.load(f)






if __name__ == '__main__':
    main()
