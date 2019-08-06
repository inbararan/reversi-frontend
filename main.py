from queue import Queue

import client
import gui

req_q = Queue()
res_q = Queue()

t = client.ClientThread(req_q, res_q)
t.start()

gui.start(res_q, req_q)
