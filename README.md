# retrieval_chatbot

## 部署:
* 目录cluster_model, data, index, model, vec_model为存放各类模型数据的目录, 需要从各目录README.md中指定的链接下载所需文件放在该目录中(不要嵌套目录, 直接拷贝指定共享目录下的所有文件)
* 安装依赖库: `pip3 install -r requirements.txt`

## 启动方法:
* 启动命令: `nohup python3 server.py &`
* **注意: 该方法服务会监听在10086端口**

## 环境要求:
* Python3
* 最好是Linux, Windows上需要安装VS2010+

## 说明:
* 如果使用server服务的方式启动，client代码为reterival_client.py，client_example.py为使用示例
* control.py为各个功能的接口模块，如果不通过server的服务调用，那么可以直接实例化Agent类为agent对象，通过`agent.api("utterance")`，返回回答和评分
