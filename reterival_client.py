# -*- coding: utf-8 -*-

import time
import random

import gevent
import zmq.green as zmq


TIME_OUT = 5000
WAITE_TIME = 10
CLIENT_NUM = 20
CLIENT_BUSY = []
CLIENT_DICT = {}


class Client:
    msg_id = -1

    def __init__(self):
        self.context = zmq.Context()
        # self.utterance = None
        self.start_client()

    def client(self):
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, TIME_OUT)
        self.socket.connect('tcp://127.0.0.1:10086')

    def start_client(self):
        client = gevent.spawn(self.client)
        gevent.joinall([client])

    def get_response(self, utterance, client_no, msgid):
        self.socket.send_string(utterance)
        reply = self.socket.recv()

        if reply:
            response = str(reply, encoding="utf-8")
        if Client.msg_id != msgid:
            Client.msg_id = msgid
            while True:
                if response:
                    # print(self.socket)
                    reply_txt = response.split("---")[0]
                    score = float(response.split("---")[1])
                    CLIENT_BUSY.remove(int(client_no))
                    return reply_txt, score
        time.sleep(WAITE_TIME)
        return "@@##$$@@", 100


def load_clients():
    for i in range(CLIENT_NUM):
        CLIENT_DICT[i] = Client()
    # for k,v in CLIENT_DICT.items():
    #     print("{}:{}".format(k, v.socket))


def select_client(utterance):
    i = random.randint(0, 19)
    while True:
        if i == CLIENT_NUM:
            i = 0
        if i in CLIENT_BUSY:
            i += 1
            continue
        else:
            CLIENT_BUSY.append(i)
            # print(CLIENT_BUSY)
            return CLIENT_DICT[i], i


# if __name__ == '__main__':
#     import random
#     load_clients()
#     # thread_ls = []
#     utterance1 = ['我超级喜欢周杰伦！', '我昨天去了周杰伦的演唱会', '我昨天去了周杰伦的演唱会，太精彩了，我超级喜欢周杰伦！',
#                   '绫波丽', '哎呦喂厉害了你', '还学习呢', '碇真嗣', '我吃的饭比你吃的盐都多', '我什么时候撒过慌',
#                   '我从来不说谎', '笨蛋', '你终于出现了', '新世纪福音战士', '你才是死基佬', '蜡笔小新', '我不看非诚勿扰',
#                   '我超级喜欢周杰伦！', '我昨天去了周杰伦的演唱会', '我昨天去了周杰伦的演唱会，太精彩了，我超级喜欢周杰伦！',
#                   '哎呦喂厉害了你', '明日香', '还学习呢', '我吃的饭比你吃的盐都多', '我什么时候撒过慌', '我从来不说谎',
#                   '笨蛋', '你终于出现了', '新世纪福音战士', '你才是死基佬', '蜡笔小新', '我不看非诚勿扰']
#     while True:
#         for each in utterance1:
#             cli, index = select_client(each)
#             print(cli.get_response(each, index, random.random()), index)
