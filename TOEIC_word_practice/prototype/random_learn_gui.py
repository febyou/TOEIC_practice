import os
import json
import random
import PySimpleGUI as sg

#自作モジュール
from function_gui import DataInfo, update_problem


def create_problem_list(data):
    problem_list = []
    for d in data:
        if d.flag == 0:
            problem_list.append(d.pid)

    return problem_list


def add_problem(path, data):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8_sig") as f:
            json.dump(data.to_dict(), f, ensure_ascii=False)
    else:
        flag = True
        with open(path, "r", encoding="utf-8_sig") as f:
            for l in f:
                item = json.loads(l)
                if item["id"] == data.pid:
                    flag = False
        if flag:
            with open(path, "a", encoding="utf-8_sig") as f:
                json.dump(data.to_dict(), f, ensure_ascii=False)
                f.write("\n")


def get_options(data, ans_num):
    while True:
        flag = True
        cand_num = random.sample(range(len(data)), 3)
        for n in cand_num:
            if data[n].pid == ans_num:
                flag = False
        if flag:
            break

    options = [data[ans_num].ans, data[cand_num[0]].ans, data[cand_num[1]].ans, data[cand_num[2]].ans]
    return options


def ans_judge(data, options, ans_num, p_num):
    if data[p_num].ans == options[ans_num-1]:
        sg.popup("正解！", title="解答判定", font=("System", 12))
    else:
        sg.popup("不正解！\n"+
                 "正解は "+data[p_num].ans+" です。",
                 title="解答判定", font=("System", 12))
        path = str(os.path.dirname(os.path.abspath(__file__))) + "/data/re_data.jsonl"
        add_problem(path, data[p_num])


def flag_reset(data):
    for d in data:
        d.flag = 0


def random_learn(data, path):
    sub_layout = [[sg.Output(size=(70, 10), key="output")],
              [sg.Text("答えとなる選択肢番号を選んでください。", font=("System", 12))],
              [sg.Radio("1.", group_id="opt", key="opt1"),
               sg.Radio("2.", group_id="opt", key="opt2"),
               sg.Radio("3.", group_id="opt", key="opt3"),
               sg.Radio("4.", group_id="opt", key="opt4")],
              [sg.Button("Answer", border_width=4), sg.Button("終了", size=(6,1), border_width=4)]]
    sub_window = sg.Window("ランダム学習モード", sub_layout, modal=True, finalize=True)
    
    problem_list = create_problem_list(data)
    
    while True:
        num = random.randrange(0, len(problem_list))
        p_num = problem_list[num]
        options = get_options(data, p_num)
        random.shuffle(options)

        sub_window["output"].update("\n  "+data[p_num].jpn+"\n"+
                                    "  "+data[p_num].eng+"\n\n"+
                                    " 1. "+options[0]+"    2. "+options[1]+"    3. "+options[2]+"    4. "+options[3]+"\n\n\n\n\n"+
                                    "  残り問題数: "+str(len(problem_list)))
        
        sub_event, sub_value = sub_window.read()
        
        if sub_event in [None, "終了"] :
            break
        elif sub_event == "Answer":
            if sub_value["opt1"]:
                ans_judge(data, options, 1, p_num)
            elif sub_value["opt2"]:
                ans_judge(data, options, 2, p_num)
            elif sub_value["opt3"]:
                ans_judge(data, options, 3, p_num)
            elif sub_value["opt4"]:
                ans_judge(data, options, 4, p_num)
            else:
                continue
        problem_list.remove(p_num)

        data[p_num].flag = 1
        if not problem_list:
            sg.popup("全ての問題を解き終えたので、一度モードを終了します。", title="全問解答済み")
            flag_reset(data)
            break
    update_problem(path, data)
    sub_window.close()
