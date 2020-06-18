# https://drive.google.com/drive/u/0/folders/1RtOsvaIf1FDO5OYh6ZsVETSZuCb2_O6_ page 39
import time
import json
from enum import Enum


def read_file(filename):
    data = json.load(open(filename))
    data = {int(key): data[key] for key in data}
    return data


def write_file(filename, data):
    json.dump(data, open(filename, "w+"))


class InvalidChannelError(Exception):
    pass


class InvalidDataError(Exception):
    pass


class EPSRegister(Enum):
    # Get methods
    BOARD_STATUS = 0x01
    GET_LAST_ERROR = 0x03
    GET_VERSION = 0x04
    GET_CHECKSUM = 0x05
    GET_REVISION = 0x06
    GET_TELEMETRY = 0x10
    GET_COMMS_WATCHDOG_PERIOD = 0x20
    GET_BROWNOUT_RESETS = 0x31
    GET_AUTO_SOFTWARE_RESETS = 0x32
    GET_MANUAL_RESETS = 0x33
    GET_WATCHDOG_RESETS = 0x34
    GET_PDM_ALL_ACTUAL_STATE = 0x42
    GET_PDM_ALL_EXPECTED_STATE = 0x43
    GET_PDM_ALL_INITIAL_STATE = 0x44
    GET_PDM_N_ACTUAL_STATE = 0x54
    GET_PDM_N_TIMER_LIMIT = 0x61
    GET_PDM_N_CURRENT_TIMER_VALUE = 0x62

    # Set methods
    SET_COMMS_WATCHDOG_PERIOD = 0x21
    RESET_COMMS_WATCHDOG = 0x22
    SWITCH_ON_ALL_PDMS = 0x40
    SWITCH_OFF_ALL_PDMS = 0x41
    SET_ALL_PDMS_TO_INITIAL_STATE = 0x45
    SWITCH_PDM_N_ON = 0x50
    SWITCH_PDM_N_OFF = 0x51
    SET_PDM_N_INITIAL_ON = 0x52
    SET_PDM_N_INITIAL_OFF = 0x53
    SET_PDM_N_TIMER_LIMIT = 0x60
    PCM_RESET = 0x70
    MANUAL_RESET = 0x80


class EPS:

    def __init__(self, config, registry, generator):
        # TODO: Use the actual initial states
        self.config = config["modules"]["EPS"]
        self.registry = registry
        self.generator = generator
        self.address = self.config["address"]
        self.state_filename = self.config["state_filename"]
        self.command_filename = self.config["command_filename"]
        self.initial_pdm_states = [0 for i in range(10)]  # everything is off
        self.initial_watchdog_period = 4
        self.board_version = 1234
        self.board_checksum = 4321
        self.board_firmware_revision = 2345
        self.timer_limits = [30 for i in range(10)]
        self.data_registers = [0x10, 0x21, 0x50, 0x51, 0x52, 0x53, 0x54, 0x60, 0x61, 0x62, 0x70]

        self.terminated = False
        self.reset()

    def change_generator(self, generator):
        # TODO: change the data type outputed by EPS based on the mode (might not be necessary)
        pass

    def reset(self):
        # Initial states
        # 0 is off, 1 is on
        self.expected_pdm_states = self.initial_pdm_states.copy()
        self.timer_values = [0 for i in range(10)]
        self.watchdog_period = self.initial_watchdog_period
        self.watchdog = time.time()

        # Create files
        #        self.state = {register.value: 0 for register in EPSRegister}
        self.state = 0x00

        self.empty_commands = {}
        self.state_dict = {-1: self.state}
        write_file(self.state_filename, self.state_dict)
        write_file(self.command_filename, self.empty_commands)

    def hard_reset(self):
        self.reset()

    def terminate(self):
        self.hard_reset()
        self.terminated = True

    def run(self):
        while True:
            if self.terminated:
                continue
            time.sleep(0.1)  # Temporary for testing, should remove this in final version
            print(self.measure_pdms())
            if time.time() - self.watchdog_period > self.watchdog:
                self.registry["EPS_ON"] = False
                self.registry["PI_ON"] = False
                self.expected_pdm_states = [0 for i in range(10)]
            # Implement watchdog
            commands = read_file(self.command_filename)
            performed_command = False
            for register in commands:
                self.ingest(register, commands[register])
                performed_command = True
            if read_file(self.command_filename) != self.empty_commands:
                write_file(self.command_filename, self.empty_commands)
            self.state_dict = {-1: self.state}
            if read_file(self.state_filename) != self.state_dict:
                write_file(self.state_filename, self.state_dict)

    def get_pin_num(self, command):
        pin = self.get_pin_num(command)
        if not (1 <= command <= 10):
            self.state = 0xFFFF
            raise InvalidChannelError("Invalid channel parameter was provided")
            return -1
        return command - 1

    def pdm_states_to_int(self, states):
        assert (len(states) == 10)
        ret = 0
        for i in range(10):
            ret |= (states[i] << (i + 1))
        return ret

    def measure_pdms(self):
        # TODO: Use this to implement overcurrent protection simulation (when actual != expected)
        return self.expected_pdm_states

    def brownout(self):
        raise NotImplementedError

    def get_board_status(self):
        raise NotImplementedError

    def get_last_error(self):
        raise NotImplementedError

    def get_telemetry(self, command):
        raise NotImplementedError

    def manual_reset(self):
        raise NotImplementedError

    def pcm_reset(self, command):
        V_battery = command | 0x01
        V_5 = command | 0x02
        V_33 = command | 0x04
        V_12 = command | 0x08
        raise NotImplementedError

    def get_n_pdm(self, register, command):
        pin = self.get_pin_num(command)
        if pin == -1:
            return 0xFFFF
        if register == EPSRegister.GET_PDM_N_ACTUAL_STATE:
            return self.measure_pdms()[pin]
        elif register == EPSRegister.GET_PDM_N_TIMER_LIMIT:
            if self.timer_limits[pin] == float("inf"):
                return 0xFF
            return self.timer_limits[pin] // 30
        elif register == EPSRegister.GET_PDM_N_CURRENT_TIMER_VALUE:
            return self.timer_values[pin] // 30
        raise Exception

    def ingest(self, register, command):
        # NOTE: I2C should convert byte arrays to ints and vice versa, simulator will always deal w/ ints
        # TODO: Add WR delays (prolly need to use threads for this)
        # TODO: Fix return bytes
        print(register, command)
        if register not in self.data_registers and command > 255:
            # TODO: EPS sometimes acts weirdly here, gotta figure out what it's actually doing
            return

        if register not in {r.value for r in EPSRegister}:
            raise Exception("Unknown register was passed")

        register_read_dict = self.get_register_read_dict(command)
        if register in register_read_dict:
            val = register_read_dict[register]()
            self.state = val
            return

        self.write_register_command(register, command)

    # Just making this method for the sake of conveniance
    def get_register_read_dict(self, command):
        return {
            EPSRegister.BOARD_STATUS.value: self.get_board_status,
            EPSRegister.GET_LAST_ERROR.value: self.get_last_error,
            EPSRegister.GET_VERSION.value: lambda: self.board_version,
            EPSRegister.GET_CHECKSUM.value: lambda: self.board_checksum,
            EPSRegister.GET_REVISION.value: lambda: self.board_firmware_revision,
            EPSRegister.GET_TELEMETRY.value: lambda: self.get_telemetry(command),
            EPSRegister.GET_COMMS_WATCHDOG_PERIOD.value: lambda: self.watchdog_period,
            EPSRegister.GET_BROWNOUT_RESETS.value: lambda: self.brownout_resets,
            EPSRegister.GET_AUTO_SOFTWARE_RESETS.value: lambda: self.auto_software_resets,
            EPSRegister.GET_MANUAL_RESETS.value: lambda: self.manual_resets,
            EPSRegister.GET_WATCHDOG_RESETS.value: lambda: self.watchdog_resets,
            EPSRegister.GET_PDM_ALL_ACTUAL_STATE.value: lambda: self.pdm_states_to_int(self.measure_pdms()),
            EPSRegister.GET_PDM_ALL_EXPECTED_STATE.value: lambda: self.pdm_states_to_int(self.expected_pdm_states),
            EPSRegister.GET_PDM_ALL_INITIAL_STATE.value: lambda: self.pdm_states_to_int(self.initial_pdm_states),
            EPSRegister.GET_PDM_N_ACTUAL_STATE.value: lambda: self.get_n_pdm(EPSRegister.GET_PDM_N_ACTUAL_STATE,
                                                                             command),
            EPSRegister.GET_PDM_N_TIMER_LIMIT.value: lambda: self.get_n_pdm(EPSRegister.GET_PDM_N_TIMER_LIMIT, command),
            EPSRegister.GET_PDM_N_CURRENT_TIMER_VALUE.value: lambda: self.get_n_pdm(
                EPSRegister.GET_PDM_N_CURRENT_TIMER_VALUE, command),
        }

    def write_register_command(self, register, command):
        if register == EPSRegister.SET_COMMS_WATCHDOG_PERIOD.value:
            if command < 1 or command > 90:
                raise InvalidDataError("Invalid watchdog period was given")
                return
            self.watchdog_period = command
        if register == EPSRegister.RESET_COMMS_WATCHDOG.value:
            return  # Technically does nothing
        if register == EPSRegister.SWITCH_ON_ALL_PDMS.value:
            self.expected_pdm_states = [1 for i in range(10)]
        if register == EPSRegister.SWITCH_OFF_ALL_PDMS.value:
            self.expected_pdm_states = [0 for i in range(10)]
        if register == EPSRegister.SET_ALL_PDMS_TO_INITIAL_STATE.value:
            self.expected_pdm_states = [i for i in self.initial_pdm_states]
        if register == EPSRegister.SWITCH_PDM_N_ON.value:
            pin = self.get_pin_num(command)
            if pin == -1: return
            self.expected_pdm_states[pin] = 1
        if register == EPSRegister.SWITCH_PDM_N_OFF.value:
            pin = self.get_pin_num(command)
            if pin == -1: return
            self.expected_pdm_states[pin] = 0
        if register == EPSRegister.SET_PDM_N_INITIAL_ON.value:
            pin = self.get_pin_num(command)
            if pin == -1: return
            self.initial_pdm_states[pin] = 1
        if register == EPSRegister.SET_PDM_N_INITIAL_OFF.value:
            pin = self.get_pin_num(command)
            if pin == -1: return
            self.initial_pdm_states[pin] = 0
        if register == EPSRegister.SET_PDM_N_TIMER_LIMIT.value:
            timer = command | 0xFF
            pin_cmd = command | 0xFF00
            pin = self.get_pin_num(pin_cmd)
            if pin == -1: return
            self.timer_limits[pin] = timer * 30
            if timer == 0xFF:
                self.timer_limits[pin] = float("inf")
        if register == EPSRegister.PCM_RESET.value:
            self.pcm_reset(command)
        if register == EPSRegister.MANUAL_RESET.value:
            self.manual_reset()

    def run_action(self, name):
        if name == 'brownout':
            self.brownout()
            return
