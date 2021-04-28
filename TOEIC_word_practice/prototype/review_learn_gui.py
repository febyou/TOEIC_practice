import os
import json
import random
import PySimpleGUI as sg

#自作モジュール
from function_gui import DataInfo, update_problem


def get_options(re_data, data, ans_num):
    if len(re_data) >= 4:
        while True:
            flag = True
            cand_num = random.sample(range(len(re_data)), 3)
            for n in cand_num:
                if re_data[n].pid == ans_num:
                    flag = False
            if flag:
                break
        options = [data[ans_num].ans, re_data[cand_num[0]].ans, re_data[cand_num[1]].ans, re_data[cand_num[2]].ans]

    else:
        options = [data[ans_num].ans]
        for r_d in re_data:
            if not r_d.pid == ans_num:
                options.append(r_d.ans)
        while True:
            num = random.randrange(0, 1000)
            if not num == ans_num:
                options.append(data[num].ans)
            if len(options) == 4:
                break
            
    return options


def ans_judge(data, options, ans, p_num):
    if data[p_num].ans == options[ans-1]:
        sg.popup("正解！", title="解答判定", font=("System", 12))
        data[p_num].flag = data[p_num].flag + 1
    else:
        sg.popup("不正解！\n"+
                 "正解は "+data[p_num].ans+" です。",
                 title="解答判定", font=("System", 12))
        if not data[p_num].flag == 0:
            data[p_num].flag = data[p_num].flag - 1


def review_learn(re_data, data, path):
    sub_layout = [[sg.Output(size=(70, 10), key="output")],
              [sg.Text("答えとなる選択肢番号を選んでください。", font=("System", 12))],
              [sg.Radio("1.", group_id="opt", key="opt1"),
               sg.Radio("2.", group_id="opt", key="opt2"),
               sg.Radio("3.", group_id="opt", key="opt3"),
               sg.Radio("4.", group_id="opt", key="opt4")],
              [sg.Button("Answer", border_width=4), sg.Button("終了", size=(6,1), border_width=4)]]
    sub_window = sg.Window("復習モード", sub_layout, modal=True, finalize=True)
    
    while True:
        if not re_data:
            sg.popup("全ての復習用の問題が解かれています。\n"+
                     "もう一度、ランダム学習モードから学習してください。",
                     title="全問解答済み")
            break
        
        num = random.randrange(0, len(re_data))
        p_num = re_data[num].pid
        options = get_options(re_data, data, p_num)
        random.shuffle(options)

        sub_window["output"].update("\n  "+data[p_num].jpn+"\n"+
                                    "  "+data[p_num].eng+"\n\n"+
                                    " 1. "+options[0]+"    2. "+options[1]+"    3. "+options[2]+"    4. "+options[3]+"\n\n\n\n\n"+
                                    "  残り問題数: "+str(len(re_data)))

        sub_event, sub_value = sub_window.read()

        if sub_event in [None, "終了"] :
            break
        elif sub_event == "Answer":
            if sub_value["opt1"]:
                ans_judge(re_data, options, 1, num)
            elif sub_value["opt2"]:
                ans_judge(re_data, options, 2, num)
            elif sub_value["opt3"]:
                ans_judge(re_data, options, 3, num)
            elif sub_value["opt4"]:
                ans_judge(re_data, options, 4, num)
            else:
                continue

        if re_data[num].flag == 2:
            re_data.remove(re_data[num])

    update_problem(path, re_data)
    sub_window.close()
