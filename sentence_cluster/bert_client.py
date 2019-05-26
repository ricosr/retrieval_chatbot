from bert_serving.client import BertClient

bc = BertClient()  # ip address of the GPU machine
print(bc.encode(['我看到你第一眼,就喜欢你了', '发的哈浪费大数据库']*10))

