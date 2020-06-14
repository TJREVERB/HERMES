import os
import sys
import json
import yaml
import time
import argparse
from threading import Thread
from serial import Serial


from hermes import Hermes, Generator


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if not os.path.exists(os.path.join(BASE_DIR, 'root')):
    os.makedirs(os.path.join(BASE_DIR, 'root'))
os.environ["HOME"] = os.path.join(BASE_DIR, 'root')

if not os.path.exists(Serial.PROJECT_ROOT):
    os.makedirs(Serial.PROJECT_ROOT)

# Add MCL to path so that we can import it
sys.path.append(os.path.abspath(os.path.join('../..', 'pfs')))
console_logger = print

starting_time = time.time()

try:
    from MainControlLoop.main_control_loop import MainControlLoop as MCL
    from MainControlLoop.lib.StateFieldRegistry import StateField, ErrorFlag
except ImportError:
    raise RuntimeError("Unable to import pFS Main Control Loop, are you in the pFS directory?")


def log(*args, console=True, save=True):
    content = "T+{0:.2f}".format(time.time() - starting_time) + ': ' + ' '.join([str(i) for i in args]) + "\n"

    if save:
        with open(os.path.join(Serial.PROJECT_ROOT, "blackbox.txt"), "a+") as file:
            file.write(content)

    if console:
        console_logger(content)


def mcl_thread(mcl):
    while True:
        mcl.execute()


def ingest(hermes, mcl, inp):
    inp += ' '
    print(f"Executing command {inp}")

    inp = inp.split()
    header, cmd = inp[0], inp[1:]

    if header == 'print':
        submodule = cmd[0]
        if submodule not in hermes.submodules:
            print("Submodule not found:", submodule)
            return
        dct = hermes.submodules[submodule].__dict__
        for key in cmd[1:]:
            dct = dct[key]
        print(dct)

    elif header == 'sfr':
        try:
            state_field = StateField(cmd[0])
        except:
            print('Unknown state field:', cmd)
            return

        print(mcl.state_field_registry.get(state_field))

    elif header == 'flag':
        try:
            flag = ErrorFlag(cmd[0])
        except:
            print('Unknown flag:', cmd)
            return

        print(mcl.state_field_registry.hardware_faults[flag])

    elif header == 'get_state':
        print(mcl.core.mode)

    elif header == 'quit':
        return True

    else:
        print("Unknown header:", header)
    

def run_tests(config, hermes, mcl):
    run_stack = []
    for time_stamp, action in config['actions']:
        run_stack.append((time_stamp, 'action', action))
    for time_stamp, command in config['commands']:
        run_stack.append((time_stamp, 'command', command))
    run_stack.sort()

    while True:
        now = time.time() - starting_time
        if now > config['runtime']:
            return

        if len(run_stack) > 0 and now >= run_stack[0][0]:
            time_stamp, rs_type, content = run_stack.pop(0)
            if rs_type == 'command':
                ingest(hermes, mcl, content)
            elif rs_type == 'action':
                print("Running Action", content, console=True)


def main():
    open(os.path.join(Serial.PROJECT_ROOT, "blackbox.txt"), "w+")
    __builtins__.__dict__['print'] = log

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="HERMES configuration file", )
    args = parser.parse_args()

    with open(args.config, 'r') as config_file:
        config = yaml.full_load(config_file)

    if not config['first_boot']:
        open(os.path.join(os.environ["HOME"], 'first_boot'), 'w')

    if config['antenna_deployed']:
        open(os.path.join(os.environ["HOME"], 'antenna_deployed'), 'w')

    hermes = Hermes(config)
    hermes.run()

    mcl = MCL()
    thread = Thread(target=mcl_thread, args=(mcl,))
    thread.daemon = True
    thread.start()

    if config['interactive']:
        while True:
            inp = input()
            if ingest(hermes, mcl, inp):
                break
    else:
        run_tests(config, hermes, mcl)

    if not config['first_boot']:
        os.remove(os.path.join(os.environ["HOME"], 'first_boot'))

    if config['antenna_deployed']:
        os.remove(os.path.join(os.environ["HOME"], 'antenna_deployed'))


if __name__ == '__main__':
    main()
