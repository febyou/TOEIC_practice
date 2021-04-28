import os
import sys
import json
import PySimpleGUI as sg

#以下は自作モジュール
from function_gui import DataInfo
from random_learn_gui import random_learn
from review_learn_gui import review_learn

is_frozen = hasattr(sys, "frozen")
problem_file = str(os.path.dirname(os.path.abspath(__file__))) + "/data/data.jsonl" if is_frozen else "data/data.jsonl"
re_problem_file = str(os.path.dirname(os.path.abspath(__file__))) + "/data/re_data.jsonl" if is_frozen else "data/re_data.jsonl"

def main():
    if(os.path.exists(problem_file)):
        data = []
        with open(problem_file, "r", encoding="utf-8_sig") as f:
            for l in f:
                item = json.loads(l)
                data.append(
                    DataInfo(item["id"], item["eng"], item["jpn"], item["ans"], item["flag"])
                )
    else:
        sg.popup("問題データが存在しません", title="File Error")

    #以下、GUI表示内容
    layout = [[sg.Text("*******************", font=("System", 24))],
              [sg.Text("***  TOEIC 単語練習  ***", font=("System", 24))],
              [sg.Text("*******************", font=("System", 24))],
              [sg.Text("学習モードを選び、STARTボタンを押してね。", font=("System", 16), pad=((0,0),(30,10)))],
              [sg.Radio("1. ランダム学習モード", font=("System", 12), group_id="opt", key="opt1")],
              [sg.Radio("2. 復習モード", font=("System", 12), group_id="opt", key="opt2")],
              [sg.Button("START", font=("System", 12), pad=((0,0),(10,20)), border_width=4)]]
    
    window = sg.Window("英単語暗記", layout, element_justification="center")
    
    while True:
        event, value = window.read()
        if event is None:
            break
        elif event == "START":
            if value["opt1"]:
                random_learn(data, problem_file)
            elif value["opt2"]:
                if os.path.exists(re_problem_file):
                    re_data = []
                    with open(re_problem_file, "r", encoding="utf-8_sig") as f:
                        for l in f:
                            item = json.loads(l)
                            re_data.append(
                                DataInfo(item["id"], item["eng"], item["jpn"], item["ans"], item["flag"])
                            )
                    review_learn(re_data, data, re_problem_file)
                else:
                    sg.popup("復習用の問題データが存在しません。\n先にランダム学習モードを解いてください。", title="File Error")
    #ここまで
    window.close()


if __name__ == '__main__':
    main()
