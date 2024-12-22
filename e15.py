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
wd = r'C:\Users\rbarr\Documents\AoC'

excercise = 15
tc = 'a'

global CASE_FILE, TEST_FILE
CASE_FILE = os.path.join(wd,'in_e' + str(excercise) + '.txt')
TEST_FILE = os.path.join(wd,'in_test_e' + str(excercise) + tc + '.txt')

global ROCK_DICT, MOVE_INSTRUCTIONS
global ROBOT_POSITION, H_MAP, L_MAP
global MAP_LIST, MAP_OBJ_LOC
global DELTA_DICT
global DEBUG_FLAG


'''
ROCK_DICT = {i: (x,y)} for each rock i
ROBOT_POSITION = (x,y)
MOVE_INSTRUCTIONS = '>^v<...'
'''

'''
FUNCTIONS HERE
'''
def init_global_variables(map_list, H, L, rock_dict, move_inst) :
    global MAP_LIST, H_MAP, L_MAP, MAP_OBJ_LOC
    global ROCK_DICT, MOVE_INSTRUCTIONS, DELTA_DICT, DEBUG_FLAG
    
    ROCK_DICT = rock_dict
    MOVE_INSTRUCTIONS = move_inst

    H_MAP = H
    L_MAP = L
    MAP_LIST = map_list
    MAP_OBJ_LOC = [ [ '.' for x in range(L_MAP) ] for y in range(H_MAP) ]
    for r, (x,y) in rock_dict.items(): MAP_OBJ_LOC[y][x] = r
    
    DELTA_DICT = {  '>' : (+1, 0) ,
                    '<' : (-1, 0) ,
                    'v' : ( 0,+1) ,
                    '^' : ( 0,-1) }
    DEBUG_FLAG = False
    
    

def process_file(in_file: str)  :
    global ROBOT_POSITION
    
    rock_dictionary = {}
    map_list = []
    move_inst = ''
    
    read_map = True
    with open(in_file, 'r') as f:
        for y,line in enumerate(f):
            
            if read_map :
                row = line.rstrip()
                if row == '' :
                    read_map = False
                    L = x+1
                    H = y
                    continue
                
                map_list.append(list(row))
                for x, el in enumerate(row) :
                    if el == 'O' :
                        rock_dictionary[len(rock_dictionary)] = (x,y)
                    if el == '@' :
                        ROBOT_POSITION = (x,y)

            else :
                move_inst += line.rstrip()
    
    init_global_variables(map_list,H,L,rock_dictionary,move_inst)
                
def pos_from_xy(x: int, y: int) -> int:
    return y*H_MAP + x

def get_GPS_coordinates(x,y) :
    return y*100 + x

def traspose_map(map_var: list, H: int, L: int) -> list:
    return [ [ map_var[y][x] for y in range(H) ] for x in range(L) ]

def print_map(map_var: list):
    for row in map_var : print(''.join([str(el) for el in row]))

def update_global_variables(r, sym, xo, yo, xn, yn):
    MAP_LIST[yo][xo] = '.'
    MAP_OBJ_LOC[yo][xo] = '.'
    
    MAP_LIST[yn][xn] = sym
    MAP_OBJ_LOC[yn][xn] = r

    if r != '.' :
        ROCK_DICT[r] = (xn,yn)
    
    if sym == '@' :
        global ROBOT_POSITION
        ROBOT_POSITION = (xn, yn)

def make_move(ins):

    x , y  = ROBOT_POSITION
    xn, yn = x , y
    
    dx, dy = DELTA_DICT[ins]

    move_list = []
    while True:
        xn += dx
        yn += dy
        obj = MAP_OBJ_LOC[yn][xn]
        if type(obj) != int :
            break
        move_list.insert(0,obj)
    
    if MAP_LIST[yn][xn] == '#': 
        return

    for rock in move_list :
        x_old, y_old = ROCK_DICT[rock]
        x_new, y_new = x_old+dx, y_old+dy
        update_global_variables(rock, 'O', x_old, y_old, x_new, y_new)

    update_global_variables('.', '@', x, y, x+dx, y+dy)

def execute_instructions():
    
    for N, instruction in enumerate(MOVE_INSTRUCTIONS): 
        x , y = ROBOT_POSITION
        
        make_move(instruction)
        
        if DEBUG_FLAG: 
            print(f"\nMove number {N+1}: {instruction}")
            print_map(MAP_LIST)

def get_total_GPS():
    total_GPS = 0
    for x,y in ROCK_DICT.values():
        total_GPS += get_GPS_coordinates(x,y)
    return total_GPS

if __name__ == "__main__" :
    file_path = CASE_FILE
    #file_path = TEST_FILE
    
    process_file(file_path)

    if DEBUG_FLAG:
        print(f"\nInitial State:")
        print_map(MAP_LIST)
    
    execute_instructions()
    
    ans_1 = get_total_GPS()
    #ans_2 = total_tokens_2
    
    print(ans_1)
    #print(ans_2)
    