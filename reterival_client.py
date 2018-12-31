# -*- coding: utf-8 -*-

import time

import gevent
import zmq.green as zmq


class Client:
    msg_id = 0

    def __init__(self):
        self.context = zmq.Context()

    def client(self, utterance):
        socket = self.context.socket(zmq.REQ)
        socket.setsockopt(zmq.LINGER, 5000)
        socket.connect('tcp://127.0.0.1:10086')
        socket.send_string(utterance)
        while True:
            reply = socket.recv()
            if reply:
                self.response = str(reply, encoding="utf-8")
                break

    def get_response(self, utterance, msgid):
        if Client.msg_id != msgid:
            Client.msg_id = msgid
            client2 = gevent.spawn(self.client, utterance)
            gevent.joinall([client2])
            if self.response:
                replyTxt = self.response.split("---")[0]
                score = float(self.response.split("---")[1])
                return replyTxt, score
        time.sleep(10)
        return "@@##$$@@", 100

# if __name__ == '__main__':
#     utterance = '我昨天去了周杰伦的演唱会，太精彩了，我超级喜欢周杰伦！'
#     cli = Client()
#     cli.post(utterance)
#     print(cli.get())



