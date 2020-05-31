import time
from threading import Thread

def run():
    global local_dict
    code = """
import time
arr = []
for i in range(100):
    arr.append(i)
    time.sleep(0.1)

print(arr)
    """
#    exec(code)
    exec(code, globals(), local_dict)

global local_dict
local_dict = {}

thread = Thread(target=run)
thread.daemon = True
thread.start()

print("HI")
while True:
    print(local_dict)
    time.sleep(0.1)
