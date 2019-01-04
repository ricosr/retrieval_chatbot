import reterival_client

if __name__ == '__main__':
    utterance = '我昨天去了周杰伦的演唱会，太精彩了，我超级喜欢周杰伦！'
    cli = reterival_client.Client()
    print(cli.get_response(utterance, 1))



