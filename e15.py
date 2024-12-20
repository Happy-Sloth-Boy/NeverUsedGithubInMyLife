# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 15:23:27 2024

@author: RB0F337L
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:07:21 2024

@author: RB0F337L
"""

import os

cwd = os.getcwd()
wd = r'X:\Winpython.385\AoC'

excercise = 15

global CASE_FILE, TEST_FILE
CASE_FILE = os.path.join(wd,'in_e' + str(excercise) + '.txt')
TEST_FILE = os.path.join(wd,'in_test_e' + str(excercise) + '.txt')

global MOVABLE_ROCK_LIST, UNMOVABLE_OBJECTS, ROBOT_POSITION, MAP_LAST_CHANGE, MOVE_INSTRUCTIONS, COOKIE_JAR
global H_MAP, L_MAP
'''
MOVABLE_ROCK_LIST = {i: (x,y)} for each rock i
UNMOVABLE_OBJECTS = {i: (x,y)} for each object i
ROBOT_POSITION = (x,y)
MAP_LAST_CHANGE = int
MOVE_INSTRUCTIONS = '>^v<...'
COOKIE_JAR = { str(pos)+"U/D/L/R": move_number }
'''

'''
FUNCTIONS HERE
'''

def pos_from_xy(x: int, y: int) -> :
    return y*H_MAP + x

def process_file(in_file: str)  :
    global MACHINES_LIST
    MACHINES_LIST = []
    with open(in_file, 'r') as f:
        for line in f:
            
                

def execute_instructions():
    global MOVE_INSTRUCTIONS
    for n, instruction in enumerate(MOVE_INSTRUCTIONS): 
        
        cookie = str(pos_from_xy(x, y)) + instruction
        in_loop = COOKIE_JAR[cookie] > MAP_LAST_CHANGE if cookie in COOKIE_JAR else False
        if in_loop :
            break
        
        COOKIE_JAR[cookie] = n
        make_move(instruction)
        
        


if __name__ == "__main__" :
    file_path = CASE_FILE
    #file_path = TEST_FILE
    
    
    
    ans_1 = total_tokens_1
    ans_2 = total_tokens_2
    
    print(ans_1)
    print(ans_2)