import os
import json
import random
import PySimpleGUI as sg

class DataInfo(object):
    def __init__(self, pid, eng, jpn, ans, flag):
        self.num = pid
        self.text_eng = eng
        self.text_jpn = jpn
        self.answer = ans
        self.f = flag

    @property
    def pid(self):
        return self.num
        
    @property
    def eng(self):
        return self.text_eng

    @property
    def jpn(self):
        return self.text_jpn

    @property
    def ans(self):
        return self.answer

    @property
    def flag(self):
        return self.f

    @flag.setter
    def flag(self, value):
        self.f = value

    def to_dict(self):
        return {"id": self.pid, "eng": self.text_eng, "jpn": self.text_jpn, "ans": self.answer, "flag": self.f}


def update_problem(path, data):
    if not os.path.exists(path):
        sg.popup("File Error", "更新すべきファイルが存在しません")
    else:
        with open(path, "w", encoding="utf-8_sig") as f:
            for d in data:
                json.dump(d.to_dict(), f, ensure_ascii=False)
                f.write("\n")

