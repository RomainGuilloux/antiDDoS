import os
import time
import subprocess

print 'Running TShark'
try:
    while(True):
        command='sudo tshark -i 1 -Y "tcp.flags.ack" -a duration:7> 1.log'
        os.system(command)
        time.sleep(0.01)
        print 'Starting again'
except KeyboardInterrupt:
    pass
