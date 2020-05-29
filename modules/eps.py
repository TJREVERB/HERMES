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
        self.address = self.config["EPS"]["address"]
        self.return_data = None


    def get_pin_num(self, command):
        return command - 1


    def get_board_status(self):
        raise NotImplementedError


    def get_pdm_actual_status(self):
        raise NotImplementedError


    def ingest(self, register, command):
        # TODO: Make this stuff run in a thread so that we can add a delay
        if register == EPSRegister.SWITCH_PDM_N_ON:
            pin_num = self.get_pin_num(command)
            self.pdm_states[pin_num] = 1
            self.return_data = None
        elif register == EPSRegister.SWITCH_PDM_N_OFF:
            pin_num = self.get_pin_num(command)
            self.pdm_states[pin_num] = 0
            self.return_data = None
        elif register == EPSRegister.MANUAL_RESET:
            assert(command == EPSRegister.MANUAL_RESET)
            self.reset()
            self.return_data = None
        elif register == EPSRegister.SET_ALL_PDMS_TO_INITIAL_STATE:
            assert(command == 0)
            self.pdm_states = self.initial_state.copy()
            self.return_data = None
        elif register == EPSRegister.GET_PDM_N_ACTUAL_STATUS:
            self.return_data = self.get_pdm_actual_status()
        elif register == EPSRegister.BOARD_STATUS:
            assert(command == 0)
            self.return_data = self.get_board_status()
        elif register == EPSRegister.RESET_COMMS_WATCHDOG:
            assert(command == 0)
            self.watchdog = self.initial_watchdog
            self.return_data = None
        else:
            print("Unknown register")

