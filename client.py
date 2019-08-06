import socket
import threading


class ClientThread(threading.Thread):
    def __init__(self, request_queue, response_queue):
        threading.Thread.__init__(self)
        self.request_queue = request_queue
        self.response_queue = response_queue

    def run(self):
        client_socket = socket.socket()
        client_socket.connect(("127.0.0.1", 5040))
        print("Connected")
        while True:
            request = self.request_queue.get()
            print("Sending request: %s" % request)
            client_socket.send(str.encode(request))
            response = client_socket.recv(4096)
            self.response_queue.put(response.decode())

        # Close socket
        client_socket.close()
