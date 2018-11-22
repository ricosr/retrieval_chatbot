# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

def main_model(input_utterance):
    task_type = classification_task()

    if task_type == "weather":
        result = weather_api()
    if task_type == "poems":
        result = poems()
    if ...:
        ...
    ...
    ...


    if task_type == "chat":
        result = rules()
        if not result:
            result = IR()
            if not result:
                reslut = seq2seq()

    return output_content





