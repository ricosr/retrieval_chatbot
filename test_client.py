import gevent
import zmq.green as zmq
import threading
import time

context = zmq.Context()

def client(i):
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5555')
    socket.send_string('{}我昨天去了周杰伦的演唱会，太精彩了，我超级喜欢周杰伦！'.format(i))
    reply = socket.recv()  # fixing for recv-send pair
    reply = str(reply, encoding="utf-8")
    print(reply)


def start_client(i):
    client2 = gevent.spawn(client(i))
    gevent.joinall([client2])


def start_thread():
    thread_ls = []
    for i in range(100):
        thread_ls.append(threading.Thread(target=start_client(i)))

    for each_thread in thread_ls:
        each_thread.start()


for i in range(50):
    t = threading.Thread(target=start_thread)
    t.start()
    time.sleep(1)

