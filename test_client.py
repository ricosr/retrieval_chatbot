import gevent
import zmq.green as zmq

context = zmq.Context()

def client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5555')
    socket.send_string('我昨天去了周杰伦的演唱会，太精彩了！')
    reply = socket.recv()  # fixing for recv-send pair
    reply = str(reply, encoding="utf-8")
    print(reply)

client = gevent.spawn(client)

gevent.joinall([client])
