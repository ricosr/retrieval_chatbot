# 检索聊天机器人

## 部署:
* 目录cluster_model, data, index, model, vec_model为存放各类模型数据的目录, 需要从各目录README.md中指定的链接下载所需文件放在该目录中(不要嵌套目录, 直接拷贝指定共享目录下的所有文件)
* 安装依赖库: `pip3 install -r requirements.txt`

## 启动步骤:
* 启动命令: `nohup python3 server.py &`
* **注意: 该方法服务会监听在10086端口**

## 环境要求:
* Python3
* 最好是Linux, Windows上需要安装VS2010+

## 其他说明:
* 如果使用server服务的方式启动，client代码为reterival_client.py，client_example.py为使用示例
* control.py为各个功能的接口模块，如果不通过server的服务调用，那么可以直接实例化Agent类为agent对象，通过`agent.api("utterance")`，返回回答和评分; 或者通过`agent.start_cmd()`方法命令行交互式运行


# Retrieval_chatbot

## deploy:
* folders of cluster_model, data, index, model, vec_model are to save models and data, you should download the necessary files into corresponding folders according to the URL of every README.md in these folders (Do not embed one folder into a local folder, directly put all files from a URL into the local folder) 
* install requirement packages: `pip3 install -r requirements.txt`

## starting steps:
* starting command: `nohup python3 server.py &`
* **attention: this way will listen port 10086**

## environment requirement:
* Python3
* Operating system had better be Linux, if Windows you need to install VS2010+

## other introduction:
* if you use the way of server to start it, you can use reterival_client.py as client, client_example.py is an example
* control.py is the interface module, if you do not use server, you can build a agent object of class Agent, and use the function `agent.api("utterance")` to get answer and score. You also use it through command window by `agent.start_cmd()` 
