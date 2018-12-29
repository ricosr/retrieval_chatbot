# Note: Remember to ``pip install pyzmq``
import gevent
import zmq.green as zmq

import control

agent = control.Agent()
context = zmq.Context()


def server():
    print("start listening ......")
    socket = context.socket(zmq.REP)
    socket.bind('tcp://127.0.0.1:10086')
    while True:
        msg = socket.recv()
        msg = str(msg, encoding="utf-8")
        reply = agent.socket_get(msg)
        socket.send_string(reply)  # fixing for recv-send pair

publisher = gevent.spawn(server)
gevent.joinall([publisher])
