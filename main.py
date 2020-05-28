import json
from control import ControlHandler
from input_handler import InputHandler
from output_handler import OutputHandler


config = json.load(open("config.json", "r"))
input_handler = InputHandler(config)
output_handler = OutputHandler(config)
controller = ControlHandler(config)


while True:
    input_handler.update_data()
    output = controller.run(input_handler.data)
    for subprocess in output:
        output_handler.set_data(subprocess, output[subprocess])

