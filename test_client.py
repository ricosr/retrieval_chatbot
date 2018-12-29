import gevent
import zmq.green as zmq
import threading
import time

context = zmq.Context()

def client():
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:10086')
    socket.send_string('我昨天去了周杰伦的演唱会，太精彩了，我超级喜欢周杰伦！')
    reply = socket.recv()  # fixing for recv-send pair
    reply = str(reply, encoding="utf-8")
    # print(reply)


def start_client():
    client2 = gevent.spawn(client)
    gevent.joinall([client2])


def start_thread():
    thread_ls = []
    for i in range(1000):
        thread_ls.append(threading.Thread(target=start_client))
        if i == 999:
            print(i)
    for each_thread in thread_ls:
        each_thread.start()

start_thread()
# for i in range(10):
#     t = threading.Thread(target=start_thread)
#     t.start()

# for i in range(1000):
#     client(i)


