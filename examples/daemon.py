"""
File: sillystream/examples/daemon.py
Author: John Andersen
Description: A process that forks off and redirects stdout to sillystream server

To run:
python examples/daemon.py
python sillystream/__main__.py client
"""
import os
import sys
import time
import sillystream

# Send stdout to sillystream
STREAM = True
# Seconds to stay alive for
STAY_ALIVE = 20

def make_daemon():
    """
    Daemonize to run in background
    """
    pid = os.fork()
    if pid > 0:
        # exit first parent
        sys.exit(0)
    pid = os.fork()
    if pid > 0:
        # exit second parent
        sys.exit(0)
    if STREAM:
        # Create sillystream server
        output = sillystream.server()
        # Start the server
        output.start_thread()
    else:
        output = open("/dev/null", 'wb')
    sys.stdout = output
    sys.stderr = output

def main():
    """
    Daemonizes and prints numbers
    """
    make_daemon()
    i = 0
    while i < STAY_ALIVE:
        print("test {}".format(i))
        i += 1
        time.sleep(1)

if __name__ == '__main__':
    main()
