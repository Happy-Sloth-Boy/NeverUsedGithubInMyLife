# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 08:12:27 2024

@author: RB0F337L
"""
import os


cwd = os.getcwd()
wd = r'X:\Winpython.385\AoC'

excercise = 10

case_file = os.path.join(wd,'in_e' + str(excercise) + '.txt')
test_file = os.path.join(wd,'in_test_e' + str(excercise) + 'h.txt')

'''
FUNCTIONS HERE
'''

def read_file(inp_file: str):
    global TRAIL_MAP, H , L, MAP_SIZE
    
    TRAIL_MAP = ""
    with open(inp_file) as f:
        for i, line in enumerate(f):
            TRAIL_MAP += line.rstrip()
    H = i + 1
    L = len(line.rstrip())
    MAP_SIZE = H*L
    

def create_aux_var():
    global SCORE_MAP, RATING_MAP, LOC_DICT, DELTA_LIST, TRAILHEADS_PATHS
    SCORE_MAP = []
    for i in range(MAP_SIZE) :
        SCORE_MAP.append([])
    
    LOC_DICT = {}
    for i in range(10):
        LOC_DICT[i] = []
    
    for i, el in enumerate(TRAIL_MAP) :
        if el == "." :
            continue
        LOC_DICT[int(el)].append(i)
        
    DELTA_LIST = [ +1, -1, +L, -L]
    
    TRAILHEADS_PATHS = {}
    for i in LOC_DICT[0]:
        TRAILHEADS_PATHS[i] = []
        
    RATING_MAP = [0]*MAP_SIZE

def get_row_col(i):
    return i//L, i%L

def get_neighbours(i: int) -> list:
    
    neighbours = []
    
    for delta in DELTA_LIST :
        j = i + delta
        i_row,i_col = get_row_col(i)
        j_row,j_col = get_row_col(j)
        if -1 < j < MAP_SIZE and (i_row==j_row or i_col==j_col):
            neighbours.append(j)
    
    return neighbours

def add_trailhead_scores() -> int :
    return sum([ len(SCORE_MAP[i]) for i in LOC_DICT[0] ])

def add_trailhead_ratings() -> int :
    return sum([ RATING_MAP[i] for i in LOC_DICT[0] ])

def efficient_way():
    for i in LOC_DICT[9]:
        SCORE_MAP[i].append(i)
        RATING_MAP[i] = 1
    
    for height in reversed(range(9)):
        
        height_indices = LOC_DICT[height]
        
        for i in height_indices :
            
            i_neighbours = get_neighbours(i)
            for j in i_neighbours :
                if TRAIL_MAP[j] == str(height + 1) :
                    RATING_MAP[i] += RATING_MAP[j]
                    if DEBUGGING_FLAG : 
                        print("Currently at {}, adding neighbour {}, rating of {}".format(i,j,RATING_MAP[j]))
                    for k in SCORE_MAP[j] :
                        SCORE_MAP[i].append(k)
                        
                SCORE_MAP[i] = list(set(SCORE_MAP[i]))
            if DEBUGGING_FLAG : 
                print(chr(10) + "Current height: {}".format(height) + chr(10))
                print_map(RATING_MAP)
                input(chr(10) + "Press key to continue..." + chr(10))
    
    return add_trailhead_scores(), add_trailhead_ratings()

def process_node(i: int, current_height: int, origin_i: int) :
    
    if current_height == 9:
        if origin_i not in TRAILHEADS_PATHS[i]:
            TRAILHEADS_PATHS[i].append(origin_i)
        return
    
    next_height = current_height + 1
    
    neighbours_list = get_neighbours(i)
    
    for neighbour_i in neighbours_list:
        neighbour_height = int(TRAIL_MAP[neighbour_i])
        if neighbour_height == next_height :
            process_node(neighbour_i, next_height, origin_i)
            

def inefficient_way() :
    
    for origin_node in LOC_DICT[0]:
        process_node(origin_node, 0, origin_node)

def print_map(map_var):
    
    for i in range(0,H):
        print(map_var[i*L: (i+1)*L])

if __name__ == "__main__" :
    file_path = case_file
    #file_path = test_file
    
    global DEBUGGING_FLAG
    DEBUGGING_FLAG = False
    
    read_file(file_path)
    create_aux_var()
    
    ans_1, ans_2 = efficient_way()
                
    print(ans_1)
    print(ans_2)
    
    if DEBUGGING_FLAG : 
        print("")
        print_map(TRAIL_MAP)
        print("")
        print_map(SCORE_MAP)
        print("")
        print_map(RATING_MAP)