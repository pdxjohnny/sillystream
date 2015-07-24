#! /usr/bin/python
import sys
import socket
# Python 2 thread
try:
    import thread
# Python 3 thread
except:
    import _thread as thread

# For constant variables such as the port
import constants

class client(object):
    """
    Listens for incoming data sent by the server
    when data is received is it sent to the recv
    method.
    """
    def __init__(self):
        """
        Sets up the variables used by client
        """
        super(client, self).__init__()
        # Should logs be writen to stdout
        self.silly_logging = constants.LOGGING
        # The connection to the server
        self.silly_socket = False
        # If we are recveing data from the server
        self.silly_running = False

    def log(self, *args):
        """
        Logs messages if self.silly_logging is True
        """
        if self.silly_logging:
            for string in args:
                sys.stdout.write(str(string) + " ")
            sys.stdout.write("\n")

    def connect(self, host=constants.HOST, port=constants.PORT, \
        split=constants.SPLIT):
        """
        Connects to the remote server and spawns the listening thread
        """
        # Create the socket
        self.silly_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        self.log("Connecting to {}:{}".format(host, port))
        self.silly_socket.connect((host, port))
        self.log("Connected")
        # Start a thread to listen for data sent from server
        thread.start_new_thread(self.listen, (split, ))
        return self.silly_socket

    def listen(self, split=constants.SPLIT):
        """
        Data can be held in waiting before sending
        to the recv function by specifiying what to split on
        with the split argument. This is pasted to client.start
        For example spliting on the word test would be split="test"
        Then whenever the word test is seen all that was sent before it
        incuding the word test would be sent to client.recv
        """
        # So that close will work
        self.silly_running = True
        # Data buffer
        data = u""
        while self.silly_running:
            # Try to get data from server
            try:
                data += self.silly_socket.recv(1).decode(constants.ENCODEING)
            # Server shutdown so close
            except ConnectionResetError as error:
                self.close()
            # No data being received so close
            if len(data) < 1:
                self.close()
            # Senf data to self.recv every char received or on split
            elif split is False or data[-len(split):] == split:
                # Call the recv function in a thread so we
                # can go bask to recving
                thread.start_new_thread(self.recv, (data, ))
                # Clear data buffer
                data = u""

    def write(self, message):
        """
        Sends a message to the server
        """
        message = str(message).encode("utf8")
        self.silly_socket.sendall(message)

    def recv(self, message):
        """
        Handles a message from the server
        """
        self.log('Received', repr(message))

    def close(self):
        """
        Closes connection with server or called on server close
        """
        self.silly_running = False
        self.silly_socket.close()
        self.log("Connection closed")

def main():
    """
    Connects and sends input to server ctrl-d to stop
    """
    # Create the client
    test = client()
    # Connect the client, default host is localhost
    test.connect()
    # In python 2x you need to send a ctrl-d to flush the buffer
    # and send everything you have typed and hit enter on
    for send in sys.stdin:
        # Send any input
        test.write(send)
    # Close connection
    test.close()

if __name__ == '__main__':
    main()