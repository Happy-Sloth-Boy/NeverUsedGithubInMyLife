# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 08:12:27 2024

@author: RB0F337L
"""
import os


cwd = os.getcwd()
wd = r'X:\Winpython.385\AoC'

case_file = os.path.join(wd,'in_e6.txt')
test_file = os.path.join(wd,'in_test_e6.txt')

turn_dictionary = {'^':'>', '>':'v', 'v':'<', '<':'^'}

def get_pos_from_xy(x,y,L) :
    return y*L + x

def get_xy_from_pos(pos,L) :
    return pos%L, pos//L 

def print_map(map_info, key):
    H = map_info['H']
    L = map_info['L']
    map_str = map_info[key]
    for i in range(0,H):
        print(map_str[i*L:(i+1)*L])

def print_map_sets(map_info, keys = ['main', 'pos', '^', 'v', '>', '<']):
    H = map_info['H']
    L = map_info['L']
    for i in range(0,H):
        lin_str = ''
        for k in keys :
            lin_str += map_info[k][i*L:(i+1)*L]
            lin_str += '   '
        print(lin_str)

def read_file(in_file):
    with open(in_file, 'r') as f:
        map_str = ''
        row = 0
        
        for line in f:
            line_clean = line.rstrip()
            map_str += line_clean
            for symbol in turn_dictionary.keys() :
                col = line_clean.find(symbol)
                if col != -1 :
                    L = len(line_clean)
                    start_position = get_pos_from_xy(col,row,L) 
                    start_direction = symbol
            row += 1
        
        H = row
        map_info = { 'H' : H , 'L' : L , 'pos' : map_str }
    
    return map_info, start_position, start_direction

def initialize_patrol_map(map_info, start_position) :
    H = map_info['H']
    L = map_info['L']
    map_str = map_info['pos']
    
    out_map_info = { 'H' : H , 'L' : L }
    
    out_map_info['pos'] = map_str
    
    out_map_info['main'] = map_str[:start_position] + 'X' + map_str[start_position+1:]
    
    for direction in ['^', 'v', '>', '<'] :
        out_map_info[direction] = map_str.replace(direction,'X')
    
    return out_map_info

def create_steps_dict(L):
    
    return {'^':-L, '>':1, 'v':L, '<':-1}

def patrol_and_update(map_info_out, position, direction, steps_dict):
    H = map_info_out['H']
    L = map_info_out['L']
    
    x_start, y_start = get_xy_from_pos(position,L)
    x_edge, y_edge = x_start, y_start
    
    if direction == '<' :
        x_edge = 0
    if direction=='>' :
        x_edge = L-1
    if direction=='^' :
        y_edge = 0
    if direction=='v' :
        y_edge = H-1
    position_edge = get_pos_from_xy(x_edge,y_edge,L)
    
    rest_of_line_ind = []
    rest_of_line_val = []
    
    step = steps_dict[direction]
    
    map_info_out[direction] = map_info_out[direction][:position] + 'X' \
                            + map_info_out[direction][position+1:]
    for i in range(position + step, position_edge+step, step) :
        #print(i)
        val = map_info_out['main'][i]
        
        if val == '#': 
            i -= step
            break
        
        map_info_out['main'] = map_info_out['main'][:i] + 'X' \
                             + map_info_out['main'][i+1:]
        map_info_out[direction] = map_info_out[direction][:i] + 'X' \
                                + map_info_out[direction][i+1:]
        
    return map_info_out, i

def check_if_leaving(map_info, position, direction):
    H = map_info['H']
    L = map_info['L']
    
    x, y = get_xy_from_pos(position,L)
    #print(position, x,y ,direction)
    
    if x==0 and direction=='<' :
        return True
    if x==L-1 and direction=='>' :
        return True
    if y==0 and direction=='^' :
        return True
    if y==H-1 and direction=='v' :
        return True
    
    return False

def check_if_in_loop(map_info, pos, next_dir):
    
    if map_info[next_dir][pos] == 'X' :
        return True
    
    return False

def update_location(map_info, current_dir, next_pos, next_dir):
    map_str = map_info['pos']
    map_str = map_str.replace(current_dir, '.')
    map_str = map_str[:next_pos] + next_dir + map_str[next_pos+1:]
    map_info['pos'] = map_str
    return map_info

def draw_patrol_map(map_info, current_pos, current_dir, max_ranges=10000) :
    
    out_map = initialize_patrol_map(map_info, current_pos)
    
    steps_dictionary = create_steps_dict(out_map['L'])
    in_loop = False
    
    for range_counter in range(0,max_ranges+1):
        out_map, next_pos = patrol_and_update(out_map, current_pos, current_dir, steps_dictionary)
        next_dir = turn_dictionary[current_dir]
        
        leaving = check_if_leaving(out_map, next_pos, current_dir)
        if leaving :
            return out_map, in_loop
        
        in_loop = check_if_in_loop(out_map, next_pos, next_dir)
        if in_loop :
            return out_map, in_loop
        
        out_map = update_location(out_map, current_dir, next_pos, next_dir)
        #print('')
        #print_map(out_map, 'pos')
        
        current_pos = next_pos
        current_dir = next_dir
        
        if range_counter == max_ranges:
            print('Warning: Max ranges analyzed')
    
    raise RuntimeError("Maxed out paths!")

def get_candidates(map_str, locs):
    
    candidates = []
    
    for i in range(0,locs) :
        candidates.append(map_str.find('X'))
        map_str = map_str.replace('X','.',1)
        
    return candidates

def put_obstacle(map_info, pos):
    new_map = map_info.copy()
    new_map['pos'] = new_map['pos'][:pos] + '#' \
                            + new_map['pos'][pos+1:]
    
    return new_map

if __name__ == "__main__" :
    file_path = case_file
    #file_path = test_file
    
    inp_map, start_pos, start_dir = read_file(file_path)
    
    out_map, in_loop = draw_patrol_map(inp_map, start_pos, start_dir, max_ranges=10000)
    
    passed_locations = out_map['main'].count('X')
    
    candidates_list = get_candidates(out_map['main'],passed_locations)
    candidates_list.remove(start_pos)
    
    #input("Press Enter to continue...")
    
    successful_obstables = 0
    for obstacle_position in candidates_list :
        new_map = put_obstacle(inp_map, obstacle_position)
        
        #print('')
        #print_map(new_map, 'pos')
        #input("Next candidate: {} - Press Enter to continue...".format(obstacle_position))
        #print('')
        
        out_map, in_loop = draw_patrol_map(new_map, start_pos, start_dir, max_ranges=10000)
        if in_loop :
            successful_obstables += 1
        #print('')
        #input("Press Enter to continue...")
        #print('')
        
    
    ans_1 = passed_locations
    ans_2 = successful_obstables
    
    print(ans_1)
    print(ans_2)