from enum import Enum

class EPSRegister(Enum):
    SWITCH_PDM_N_ON = 0x50
    SWITCH_PDM_N_OFF = 0x51
    MANUAL_RESET = 0x33
    GET_PDM_N_ACTUAL_STATUS = 0x54
    SET_ALL_PDMS_TO_INITIAL_STATE = 0x45
    RESET_COMMS_WATCHDOG = 0x22
    BOARD_STATUS = 0x01


class EPS:

    def __init__(self, config):
        # 0 is off, 1 is on
        # Initial states
        self.initial_state = [0 for i in range(10)]
        self.pdm_states = self.initial_state.copy()
        self.initial_watchdog = 0.5
        self.watchdog = self.initial_watchdog
        self.config = config
        self.address = self.config["EPS"]["address"]
        self.return_data = None


    def get_pin_num(self, command):
        return command - 1


    def get_board_status(self):
        raise NotImplementedError


    def get_pdm_actual_status(self):
        raise NotImplementedError


    def parse_data(self, data):
        split = data.split(";")
        register = int(split[0].strip())
        command = eval(split[1].strip())
        return register, command


    def ingest(self, data):
        # TODO: Make this stuff run in a thread so that we can add a delay
        # TODO: Read EPS documentation to verify commands are right
        if not data:
            return
        register, command = self.parse_data(data)
        print(register, command)
        if register == EPSRegister.SWITCH_PDM_N_ON.value:
            print("Turning on")
            pin_num = self.get_pin_num(command[0])
            self.pdm_states[pin_num] = 1
            self.return_data = None
        elif register == EPSRegister.SWITCH_PDM_N_OFF.value:
            pin_num = self.get_pin_num(command[0])
            self.pdm_states[pin_num] = 0
            self.return_data = None
        elif register == EPSRegister.MANUAL_RESET.value:
            assert(command[0] == EPSRegister.MANUAL_RESET.value and len(command) == 0)
            self.reset()
            self.return_data = None
        elif register == EPSRegister.SET_ALL_PDMS_TO_INITIAL_STATE.value:
            assert(command[0] == 0 and len(command) == 0)
            self.pdm_states = self.initial_state.copy()
            self.return_data = None
        elif register == EPSRegister.GET_PDM_N_ACTUAL_STATUS.value:
            self.return_data = self.get_pdm_actual_status()
        elif register == EPSRegister.BOARD_STATUS.value:
            assert(command[0] == 0 and len(command) == 0)
            self.return_data = self.get_board_status()
        elif register == EPSRegister.RESET_COMMS_WATCHDOG.value:
            assert(command[0] == 0 and len(command) == 0)
            self.watchdog = self.initial_watchdog
            self.return_data = None
        else:
            print("Unknown register")

