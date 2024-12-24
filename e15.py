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
CASE_FILE = os.path.join(cwd,'in_e' + str(excercise) + '.txt')
TEST_FILE = os.path.join(cwd,'in_test_e' + str(excercise) + tc + '.txt')

global ROCK_DICT, ROCK_DICT_WIDE, MOVE_INSTRUCTIONS
global ROBOT_POSITION, H_MAP, L_MAP
global MAP_LIST, MAP_OBJ_LOC
global ROBOT_POS_WIDE, L_WIDE
global MAP_LIST_WIDE, MAP_OBJ_LOC_WIDE
global DELTA_DICT
global DEBUG_FLAG, DEBUG_FLAG_WIDE


'''
ROCK_DICT = {i: (x,y)} for each rock i
ROBOT_POSITION = (x,y)
MOVE_INSTRUCTIONS = '>^v<...'
'''

'''
FUNCTIONS HERE
'''
def init_global_variables(map_list, map_list_wide, H, L, rock_dict, rock_dict_wide, move_inst) :
    global MAP_LIST, H_MAP, L_MAP, MAP_OBJ_LOC
    global MAP_LIST_WIDE, L_WIDE, MAP_OBJ_LOC_WIDE
    global ROCK_DICT, ROCK_DICT_WIDE, MOVE_INSTRUCTIONS, DELTA_DICT
    
    ROCK_DICT = rock_dict
    ROCK_DICT_WIDE = rock_dict_wide
    MOVE_INSTRUCTIONS = move_inst

    H_MAP = H
    L_MAP = L
    L_WIDE = 2*L
    MAP_LIST = map_list
    MAP_LIST_WIDE = map_list_wide
    MAP_OBJ_LOC = [ [ '.' for x in range(L_MAP) ] for y in range(H_MAP) ]
    MAP_OBJ_LOC_WIDE = [ [ '.' for x in range(L_WIDE) ] for y in range(H_MAP) ]
    for r, (x,y) in rock_dict.items(): MAP_OBJ_LOC[y][x] = r
    
    for r, (x,y) in rock_dict_wide.items(): 
        MAP_OBJ_LOC_WIDE[y][x] = float(r)
        MAP_OBJ_LOC_WIDE[y][x+1] = float(r+0.5)
    
    DELTA_DICT = {  '>' : (+1, 0) ,
                    '<' : (-1, 0) ,
                    'v' : ( 0,+1) ,
                    '^' : ( 0,-1) ,
                    '[' :     +1  ,
                    ']' :     -1  }

def process_file(in_file: str)  :
    global ROBOT_POSITION, ROBOT_POS_WIDE
    
    rock_dict = {}
    rock_dict_wide = {}
    map_list = []
    map_list_wide = []
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
                map_list_wide.append([])
                for x, el in enumerate(row) :
                    x_w = x_wide_from_x(x)
                    if el == 'O' :
                        rock_dict[len(rock_dict)] = (x,y)
                        rock_dict_wide[len(rock_dict)] = (x_w[0], y)
                        map_list_wide[y] += ['[',']']
                    elif el == '@' :
                        ROBOT_POSITION = (x,y)
                        ROBOT_POS_WIDE = (x_w[0],y)
                        map_list_wide[y] += ['@','.']
                    else:
                        map_list_wide[y] += [el,el]

            else :
                move_inst += line.rstrip()
    
    init_global_variables(map_list,map_list_wide,H,L,rock_dict,rock_dict_wide,move_inst)
                
def pos_from_xy(x: int, y: int) -> int:
    return y*H_MAP + x

def x_wide_from_x(x:int) -> tuple:
    return 2*x, 2*x+1

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

def list_rocks_to_move(xn, yn, dx, dy, map_obj, map_list):
    move_list = []
    while True:
        xn += dx
        yn += dy
        obj = map_obj[yn][xn]
        if type(obj) != int and type(obj) != float :
            break
        if int(obj) == obj:
            move_list.insert(0,obj)
    
    if map_list[yn][xn] == '#': 
        return None
    
    return move_list

def update_rocks_and_robot(move_list, xr, yr, dx, dy):
    for rock in move_list :
        x_old, y_old = ROCK_DICT[rock]
        x_new, y_new = x_old+dx, y_old+dy
        update_global_variables(rock, 'O', x_old, y_old, x_new, y_new)
    update_global_variables('.', '@', xr, yr, xr+dx, yr+dy)

def make_move(ins: str):

    x , y  = ROBOT_POSITION
    xn, yn = x , y
    
    dx, dy = DELTA_DICT[ins]
    
    move_list = list_rocks_to_move(xn, yn, dx, dy, MAP_OBJ_LOC, MAP_LIST)
    if move_list is None : 
        return
    
    update_rocks_and_robot(move_list, x, y, dx, dy)

def check_move(x,y,dy,move_list) :
    
    x_next, y_next = x , y+dy
    obj = MAP_LIST_WIDE[y_next][x_next]
    
    if obj == '#':
        return False, []
    if obj == '.':
        return True, move_list
    
    move_list.append(int(MAP_OBJ_LOC_WIDE[y_next][x_next]))
    #if obj == '[':
    #    move_list.append(int(MAP_OBJ_LOC_WIDE[y_next][x_next]))
    
    dx_box = DELTA_DICT[obj]
    
    check, move_list = check_move(x_next,y_next,dy,move_list)
    if not check :
        return False, []
    check, move_list = check_move(x_next+dx_box,y_next,dy,move_list)
    
    return check, move_list

def update_global_variables_wide(r, sym, xo, yo, xn, yn):
    MAP_LIST_WIDE[yo][xo] = '.'
    MAP_OBJ_LOC_WIDE[yo][xo] = '.'
    
    MAP_LIST_WIDE[yn][xn] = sym
    if   sym == '[': MAP_OBJ_LOC_WIDE[yn][xn] = float(r)
    elif sym == ']': MAP_OBJ_LOC_WIDE[yn][xn] = float(r) + 0.5
    else           : MAP_OBJ_LOC_WIDE[yn][xn] = r

    if sym == '[' :
        ROCK_DICT_WIDE[r] = (xn,yn)
        
    if sym == '@' :
        global ROBOT_POS_WIDE
        ROBOT_POS_WIDE = (xn, yn)

def update_rocks_and_robot_wide(move_list, x, y, dx, dy):
    rock_list = list(set(move_list))
    
    if dy != 0:
        rock_list.sort(key=lambda k: ROCK_DICT_WIDE[k][1],reverse=dy>0)
    
    if dx != 0:
        rock_list.sort(key=lambda k: ROCK_DICT_WIDE[k][0],reverse=dx>0)
    
    if DEBUG_FLAG_WIDE: 
            print(f"List of rocks to move: {rock_list}")
            
    for rock in rock_list :
        xL_old, yL_old = ROCK_DICT_WIDE[rock]
        xL_new, yL_new = xL_old+dx, yL_old+dy
        if DEBUG_FLAG_WIDE: 
            print(f"Moving: {int(rock)} from")
            print(f"   Left: {xL_old}, {yL_old} to {xL_new}, {yL_new}")
            print(f"   Right: {xL_old+1}, {yL_old} to {xL_new+1}, {yL_new}")
        if dx > 0 :
            update_global_variables_wide(rock, ']', xL_old+1, yL_old, xL_new+1, yL_new)
            update_global_variables_wide(rock, '[', xL_old, yL_old, xL_new, yL_new)
        else :
            update_global_variables_wide(rock, '[', xL_old, yL_old, xL_new, yL_new)
            update_global_variables_wide(rock, ']', xL_old+1, yL_old, xL_new+1, yL_new)
        
    update_global_variables_wide('.', '@', x, y, x+dx, y+dy)

def make_move_wide(ins):

    x , y  = ROBOT_POS_WIDE
    xn, yn = x , y
    
    dx, dy = DELTA_DICT[ins]
    
    if dx != 0:
        move_list = list_rocks_to_move(xn, yn, dx, dy, MAP_OBJ_LOC_WIDE, MAP_LIST_WIDE)
        if move_list is None : 
            return
        update_rocks_and_robot_wide(move_list, x, y, dx, dy)
    
    else:
        check, move_list = check_move(x,y,dy,[])
        if check:
            update_rocks_and_robot_wide(move_list, x, y, dx, dy)

def execute_instructions():
    
    for N, instruction in enumerate(MOVE_INSTRUCTIONS): 
        if DEBUG_FLAG or DEBUG_FLAG_WIDE: 
            print(f"\nMove number {N+1}: {instruction}")
        
        rocks_before = len(set(ROCK_DICT_WIDE.values()))
        make_move(instruction)
        make_move_wide(instruction)
        rocks_after = len(set(ROCK_DICT_WIDE.values()))
        
        if DEBUG_FLAG: 
            print(f"\nOriginal Map:")
            print_map(MAP_LIST)
        if DEBUG_FLAG_WIDE: 
            print(f"\nWide Map:")
            print_map(MAP_LIST_WIDE)
            print()
            print_map(MAP_OBJ_LOC_WIDE)
            if (N+1)%20 == 0:
                input("Continue?")
        
        if rocks_before != rocks_after : 
            raise RuntimeError("Number of rocks changed!")

def get_total_GPS(rock_dict):
    total_GPS = 0
    for x,y in rock_dict.values():
        total_GPS += get_GPS_coordinates(x,y)
    return total_GPS

if __name__ == "__main__" :
    file_path = CASE_FILE
    #file_path = TEST_FILE
    
    DEBUG_FLAG = False
    DEBUG_FLAG_WIDE = False
    
    process_file(file_path)

    print(f"\nInitial State:")
    print_map(MAP_LIST_WIDE)
    print()
    print_map(MAP_OBJ_LOC_WIDE)
    
    execute_instructions()
    
    print(f"\nFinal State:")
    print_map(MAP_LIST_WIDE)
    print()
    print_map(MAP_OBJ_LOC_WIDE)
    
    ans_1 = get_total_GPS(ROCK_DICT)
    ans_2 = get_total_GPS(ROCK_DICT_WIDE)
    
    print(ans_1)
    print(ans_2)
    