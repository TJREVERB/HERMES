from serial import Serial
from .generator import Generator
from time import sleep


class Iridium:

    def __init__(self, config, mcl, generator: Generator):
        self.config = config
        self.mcl = mcl
        self.generator = generator

        self.pfs_logging = config['modules']['Iridium']['pfs_logging']
        self.pfs_error = config['modules']['Iridium']['start_with_error']

        self.serial = Serial(port='/dev/serial0', invert=True, timeout=0.1)
        self.serial.logging = True

        self.terminated = False

    def run(self):
        sleep(0.1)

        while True:
            if self.mcl.iridium.iridium.serial is not None:
                self.mcl.iridium.iridium.serial.logging = self.pfs_logging
                self.mcl.iridium.iridium.serial.error = self.pfs_error

            nb = self.serial.read(size=1)

            if nb != b'' and self.generator == Generator.BOOT:
                print("Ummmm, the SATT-4 is transmitting during the boot interval...")

            if nb != b'' and self.generator == Generator.STARTUP:
                print("pFS is utilizing its antenna, response will indicate successful antenna deployment")

    def send(self, command):
        if self.terminated:
            print(f"Iridium module isn't active, cannot send: {command}")
            return

        print(f"Sending {command}")

        if self.generator == Generator.BOOT:
            print("We shouldn't send now, as it is assumed pFS is in its BOOT state")
            return

        if self.generator == Generator.STARTUP:
            print("We should only send in response to a message from pFS as it is assumed pFS is in its STARTUP state")
            return

        if self.generator == Generator.DANGER:
            print("pFS should be in SAFE, so the command may be ignored (still sending it though)")

        self.serial.write(command.encode('utf-8'))

    def change_generator(self, generator: Generator):
        if generator in [Generator.NORMAL, Generator.LOW_POWER] and self.generator == Generator.STARTUP:
            self.serial.write(b'TJ:C;pFS;EXIT_STARTUP;;\n')

        if generator == Generator.DANGER:
            self.pfs_error = True
        else:
            self.pfs_error = False

        self.generator = Generator

    def run_action(self, name):
        if name == 'connect':
            self.pfs_error = False
        elif name == 'disconnect':
            self.pfs_error = True
        else:
            print(f'Unknown Iridium action: {name}')

    def terminate(self):
        self.terminated = True

    def reset(self):
        self.terminated = False
