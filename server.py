# Note: Remember to ``pip install pyzmq``
import gevent
import zmq.green as zmq

import control

agent = control.Agent()

def server():
    print("start listening ......")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://127.0.0.1:5555')
    while True:
        msg = socket.recv()
        msg = str(msg, encoding="utf-8")
        print(msg)
        reply = agent.api(msg)
        socket.send_string(reply)  # fixing for recv-send pair

publisher = gevent.spawn(server)
gevent.joinall([publisher])
