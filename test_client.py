import gevent
import zmq.green as zmq
import threading
import time

context = zmq.Context()


def client3():
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:10086')
    time.sleep(2)
    socket.send_string('你认识鲁迅吗？')
    reply = socket.recv()  # fixing for recv-send pair
    reply = str(reply, encoding="utf-8")
    print(reply)

def client():
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:10086')
    time.sleep(3)
    socket.send_string('我对你很失望')
    reply = socket.recv()  # fixing for recv-send pair
    reply = str(reply, encoding="utf-8")
    print(reply)


def client2():
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:10086')
    socket.send_string('我要你做我女朋友')
    reply = socket.recv()  # fixing for recv-send pair
    reply = str(reply, encoding="utf-8")
    print(reply)


def start_client():
    client_ = gevent.spawn(client)
    gevent.joinall([client_])


def start_client2():
    client2_ = gevent.spawn(client2)
    gevent.joinall([client2_])


def start_client3():
    client3_ = gevent.spawn(client3)
    gevent.joinall([client3_])


def start_thread():
    thread_ls = []
    for i in range(5):
        thread_ls.append(threading.Thread(target=start_client2))
    for i in range(3):
        thread_ls.append(threading.Thread(target=start_client))
    for i in range(3):
        thread_ls.append(threading.Thread(target=start_client3))

    for each_thread in thread_ls:
        each_thread.start()


start_thread()
# for i in range(10):
#     t = threading.Thread(target=start_thread)
#     t.start()

# for i in range(1000):
#     client(i)


