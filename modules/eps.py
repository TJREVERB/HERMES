from enum import Enum
from .helpers import read_file, write_file

class EPSRegister(Enum):
    SWITCH_PDM_N_ON = 0x50
    SWITCH_PDM_N_OFF = 0x51
    MANUAL_RESET = 0x33
    GET_PDM_N_ACTUAL_STATUS = 0x54
    SET_ALL_PDMS_TO_INITIAL_STATE = 0x45
    RESET_COMMS_WATCHDOG = 0x22
    GET_COMMS_WATCHDOG_PERIOD = 0x20
    SET_COMMS_WATCHDOG_PERIOD = 0x21
    BOARD_STATUS = 0x01


class EPS:

    def __init__(self, config):
        # 0 is off, 1 is on
        # Initial states
        self.initial_state = [0 for i in range(10)]
        self.pdm_states = self.initial_state.copy()
        self.initial_watchdog = 0.5
        self.watchdog = self.initial_watchdog
        self.config = config["EPS"]
        self.address = self.config["address"]
        self.state_filename = self.config["state_filename"]
        self.command_filename = self.config["command_filename"]
        self.return_data = None

        # Create files
        self.state = {register.value: 0 for register in EPSRegister}
        self.empty_commands = {register.value: -1 for register in EPSRegister}
        write_file(self.state_filename, self.state)
        write_file(self.command_filename, self.empty_commands)


    def run(self):
        # Add some sort of control loop? (What does the EPS do when its just being left)
            # Implement watchdog
        commands = read_file(self.command_filename)
        performed_command = False
        for register in commands:
            if commands[register] == -1: continue
            self.ingest(register, commands[register])
            performed_command = True
        if performed_command:
            write_file(self.command_filename, self.empty_commands)
        write_file(self.state_filename, self.state)


    def get_pin_num(self, command):
        return command - 1


    def get_board_status(self):
        raise NotImplementedError


    def get_pdm_actual_status(self):
        return 
#        raise NotImplementedError


    def ingest(self, register, command):
        # TODO: Make this stuff run in a thread so that we can add a delay
        # TODO: Read EPS documentation to verify that commands are right
        # TODO: Does the command value "0" need to be sent for certain stuff?
        print(register, command)
        if register == EPSRegister.SWITCH_PDM_N_ON.value:
            print("Turning on")
            pin_num = self.get_pin_num(command[0])
            self.pdm_states[pin_num] = 1
        elif register == EPSRegister.SWITCH_PDM_N_OFF.value:
            pin_num = self.get_pin_num(command[0])
            self.pdm_states[pin_num] = 0
        elif register == EPSRegister.MANUAL_RESET.value:
            self.reset()
        elif register == EPSRegister.SET_ALL_PDMS_TO_INITIAL_STATE.value:
            self.pdm_states = self.initial_state.copy()
        elif register == EPSRegister.GET_PDM_N_ACTUAL_STATUS.value:
            self.return_data = self.get_pdm_actual_status()
        elif register == EPSRegister.BOARD_STATUS.value:
            self.state[register] = self.get_board_status()
        elif register == EPSRegister.RESET_COMMS_WATCHDOG.value:
            self.watchdog = self.initial_watchdog
            self.state[register] = [self.watchdog] # TODO: Verify this
        elif register == EPSRegister.GET_COMMS_WATCHDOG_PERIOD.value:
            self.state[register] = [self.watchdog]
        elif register == EPSRegister.SET_COMMS_WATCHDOG_PERIOD.value:
            self.watchdog = command[0]
        else:
            print("Unknown register")

