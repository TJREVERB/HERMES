import os
import sys
import json
import argparse
from hermes import Hermes
from threading import Thread


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Add MCL to path so that we can import it
sys.path.append(os.path.abspath(os.path.join('../..', 'pfs')))
print(os.getcwd())
console_logger = print

try:
    from MainControlLoop.main_control_loop import MainControlLoop as MCL
    from MainControlLoop.lib.StateFieldRegistry import StateField, ErrorFlag
except ImportError:
    raise RuntimeError("Unable to import pFS Main Control Loop, are you in the pFS directory?")


def log(*args, console=False, save=True):
    content = ' '.join([str(i) for i in args]) + "\n"

    if save:
        with open("blackbox.txt", "a+") as file:
            file.write(content)

    if console:
        console_logger(content)


def mcl_thread(mcl):
    while True:
        mcl.execute()


def ingest(hermes, mcl, inp):
    if ' ' not in inp:
        print("Invalid command: ", inp, console=True)
        return

    print(f"Executing command {inp}", console=True)

    inp = inp.split()
    header, cmd = inp[0], inp[1:]

    if header == 'print':
        submodule = cmd[0]
        if submodule not in hermes.submodules:
            print("Submodule not found: ", submodule, console=True)
            return
        dct = hermes.submodules[submodule].__dict__
        for key in cmd[1:]:
            dct = dct[key]
        print(dct, console=True)

    elif header == 'sfr':
        try:
            state_field = StateField(cmd[0])
        except:
            print('Unknown state field: ', cmd, console=True)
            return

        print(mcl.state_field_registry.get(state_field), console=True)

    elif header == 'flag':
        try:
            flag = ErrorFlag(cmd[0])
        except:
            print('Unknown flag: ', cmd, console=True)
            return

        print(mcl.state_field_registry.hardware_faults[flag], console=True)

    else:
        print("Unknown header:", header, console=True)
    

def run_tests():
    print('running tests')


def main():
    open("blackbox.txt", "w+")
    __builtins__.__dict__['print'] = log
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="HERMES configuration file", )
    args = parser.parse_args()

    with open(args.config, 'r') as config_file:
        config = json.load(config_file)

    hermes = Hermes(config)
    hermes.run()

    mcl = MCL()
    thread = Thread(target=mcl_thread, args=(mcl,))
    thread.daemon = True
    thread.start()

    if sys.flags.interactive:
        while True:
            inp = input()
            ingest(hermes, mcl, inp)
    else:
        run_tests()


if __name__ == '__main__':
    main()
