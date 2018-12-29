# -*- coding: utf-8 -*-

import gevent
import zmq.green as zmq


class Client:
    def __init__(self):
        self.context = zmq.Context()

    def client(self, utterance):
        socket = self.context.socket(zmq.REQ)
        socket.connect('tcp://127.0.0.1:10086')
        socket.send_string(utterance)
        reply = socket.recv()  # fixing for recv-send pair
        self.response = str(reply, encoding="utf-8")

    def post(self, utterance):
        client2 = gevent.spawn(self.client, utterance)
        gevent.joinall([client2])

    def get(self):
        replyTxt = self.response.split("---")[0]
        score = float(self.response.split("---")[1])
        return replyTxt, score

if __name__ == '__main__':
    utterance = '我昨天去了周杰伦的演唱会，太精彩了，我超级喜欢周杰伦！'
    cli = Client()
    cli.post(utterance)
    print(cli.get())



