# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 16:52:59 2024

@author: RB0F337L
"""

import os
import time
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer

cwd = os.getcwd()
wd = r'X:\Winpython.385\AoC'

excercise = 14

global CASE_FILE, TEST_FILE
CASE_FILE = os.path.join(wd,'in_e' + str(excercise) + '.txt')
TEST_FILE = os.path.join(wd,'in_test_e' + str(excercise) + '.txt')

global ROBOTS_LIST, QUADRANT_COUNT, H_MAP, L_MAP, ROBOTS_END
QUADRANT_COUNT = dict.fromkeys(('Q1','Q2','Q3','Q4'), 0)

'''
FUNCTIONS HERE
'''

def process_file(in_file: str)  :
    global ROBOTS_LIST, ROBOTS_END
    ROBOTS_LIST = []
    ROBOTS_END = []
    with open(in_file, 'r') as f:
        for line in f:
            P, V = line.rstrip().split(" ")
            
            x, y = P.lstrip("p=").split(",")
            u, v = V.lstrip("v=").split(",")
            
            ROBOTS_LIST.append([int(x), int(y), int(u), int(v)])
                

def process_robot(x: int, y: int, u: int, v: int, t: int) -> int :
    global ROBOTS_END, H_MAP, L_MAP
    
    x_raw = x + t*u
    y_raw = y + t*v
    
    x_f = x_raw % L_MAP
    y_f = y_raw % H_MAP
    
    ROBOTS_END.append((x_f,y_f))
    
    if x_f < L_MAP//2 and y_f < H_MAP//2 :
        return "Q1"
    if x_f > L_MAP//2 and y_f < H_MAP//2 :
        return "Q2"
    if x_f < L_MAP//2 and y_f > H_MAP//2 :
        return "Q3"
    if x_f > L_MAP//2 and y_f > H_MAP//2 :
        return "Q4"
    
    return None

def prepare_map_text():
    global ROBOTS_END, H_MAP, L_MAP
    
    map_list = []
    for y in range(H_MAP) :
        map_list.append([])
        for x in range(L_MAP) :
            map_list[y].append('.')
            
    for x,y in ROBOTS_END :
        if map_list[y][x] == '.' :
            map_list[y][x] = '1'
        elif map_list[y][x] == '9' :
            map_list[y][x] = '0'
        elif 0 < int(map_list[y][x]) < 9 :
            map_list[y][x] = str(int(map_list[y][x]) + 1)
    
    str_to_print = '\n'.join([ ''.join(row) for row in map_list ])
    
    return str_to_print

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Courier",5))
        self.setCentralWidget(self.text_edit)
        
        self.resize(500, 900)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(10000)
        
        self.counter = 7501
    
    def update_text(self):
        global ROBOTS_END
    
        self.counter += 1
        
        t = self.counter
        ROBOTS_END = []
        for x, y, u, v in ROBOTS_LIST :
            q = process_robot(x, y, u, v, t)
        
        text = f"Time: {t}" + "\n" + prepare_map_text()
        self.text_edit.setPlainText(text)
        

def print_pyqt6_grid_through_time(total_time):
    
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
    '''
    layout = QVBoxLayout()
    
    text_edit = QPlainTextEdit()
    text_edit.setReadOnly(True)
    text_edit.setFont(QFont("Courier",5))
    text_edit.setPlainText(text)
    
    for t in range(1000):
        ROBOTS_END = []
        for x, y, u, v in ROBOTS_LIST :
            q = process_robot(x, y, u, v, t)
    
    layout.addWidget(text_edit)
    
    window.setLayout(layout)
    window.show()
    
    sys.exit(app.exec())
    '''

if __name__ == "__main__" :
    
    TEST_FLAG = False
    
    file_path = CASE_FILE
    H_MAP = 103
    L_MAP = 101
    
    if TEST_FLAG :
        file_path = TEST_FILE
        H_MAP = 7
        L_MAP = 11
    
    process_file(file_path)
    total_time = 100
    for x, y, u, v in ROBOTS_LIST :
        q = process_robot(x, y, u, v, total_time)
        
        if q is not None:
            QUADRANT_COUNT[q] += 1
    
    safety_factor = 1
    for q_n in QUADRANT_COUNT.values():
        safety_factor *= q_n
    
    ans_1 = safety_factor
    print(ans_1)
    
    
    print_pyqt6_grid_through_time(100)
    
    # Based on observation
    pattern_1_fst_occ = 28
    pattern_2_fst_occ = 86
    pattern_1_freq = 101
    pattern_2_freq = 103
    
    pattern_1_occ = pattern_1_fst_occ - pattern_1_freq
    pattern_2_occ = pattern_2_fst_occ - pattern_2_freq
    pattern_2_array = []
    for n_loops in range(1000):
        pattern_1_occ += pattern_1_freq
        pattern_2_occ += pattern_2_freq
        
        pattern_2_array.append(pattern_2_occ)
        
        if pattern_1_occ in pattern_2_array :
            ans_2 = pattern_1_occ
            break
    
    print(ans_2)