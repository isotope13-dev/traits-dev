import os
import time
r,w = os.pipe()
first()
second()
a = start()
while True:
    time.sleep(10)
