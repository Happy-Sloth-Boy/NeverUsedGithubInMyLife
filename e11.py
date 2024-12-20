# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 08:12:27 2024

@author: RB0F337L
"""
import os

cwd = os.getcwd()
wd = r'X:\Winpython.385\AoC'

excercise = 11

global CASE_FILE, TEST_FILE
CASE_FILE = os.path.join(wd,'in_e' + str(excercise) + '.txt')
TEST_FILE = os.path.join(wd,'in_test_e' + str(excercise) + '.txt')

global STONE_LIST_TREE, STONE_LOC_DICT, STONE_CHILD_DICT, STONE_CHILD_LOC, TREE_DICT
global DEPTH


'''
FUNCTIONS HERE
'''

def read_file(in_file: str) -> list :
    with open(in_file, 'r') as f:
        input_list = [ int(n) for n in f.read().rstrip().split() ]
    return input_list

def split_int_in_two(n: int) -> list :
    str_n = str(n)
    n_digits = len(str_n)
    if n_digits % 2 == 0 :
        return [int(str_n[:n_digits//2]), int(str_n[n_digits//2:])]
    
    raise RuntimeError("Incorrect use of function attempting to split an integer in 2. Input: {}; Input type:".format(n, type(n)))


def init_inputs(flag: bool) :
    global FILE_PATH, TOTAL_BLINKS_1, TOTAL_BLINKS_2, DEPTH, TREE_DICT
    
    DEPTH = 10
    TREE_DICT = {}
    
    if flag:
        FILE_PATH = TEST_FILE
        TOTAL_BLINKS_1 = 6
        TOTAL_BLINKS_2 = 6
    else:
        FILE_PATH = CASE_FILE
        TOTAL_BLINKS_1 = 25
        TOTAL_BLINKS_2 = 75


def add_stone_to_tree_dict(n: int):
    tree_i = []
    stone_list = [n]
    for i in range(DEPTH):
        stone_list = blink(stone_list)
        tree_i.append(stone_list)
    TREE_DICT[n] = tree_i


def add_stone_to_tree_from_tree(n: int):
    j,k = split_int_in_two(n)
    tree_i = [[j,k]]
    stone_list = [n]
    for i in range(DEPTH-1):
        stone_list = TREE_DICT[j][i] + TREE_DICT[k][i]
        tree_i.append(stone_list)
    TREE_DICT[n] = tree_i


def initialize_tree_dict():
    
    odd_digit_ranges = [range(0,10),   range(100,1000),   range(10000,100000)  ]
    evn_digit_ranges = [range(10,100), range(1000,10000), range(100000,1000000)]
    
    for r in odd_digit_ranges :
        for i in r:
            add_stone_to_tree_dict(i)
        print("Range finished: ", r)
    
    for r in evn_digit_ranges :
        for i in r:
            add_stone_to_tree_from_tree(i)
        print("Range finished: ", r)


def blink_on_stone(n: int) -> list :
    
    if n == 0 :
        return [1]
    
    try : 
        result = split_int_in_two(n)
        return result
    except :
        return [n*2024]
    
    raise RuntimeError("Error in coding...")


def multiple_blink_on_stone(n: int, number_of_blinks: int) -> list :
    
    if n in TREE_DICT.keys() :
        return TREE_DICT[n][number_of_blinks-1]
    
    add_stone_to_tree_dict(n)
    return TREE_DICT[n][number_of_blinks-1]
    

def blink(stone_list: list) -> list :
    
    stone_list_after_blink = []
    
    for stone in stone_list:
        stone_list_after_blink += blink_on_stone(stone)
    
    return stone_list_after_blink


def multiple_blink(stone_list: list, number_of_blinks: int) -> list :
    
    stone_list_after_blink = []
    
    for stone in stone_list:
        stone_list_after_blink += multiple_blink_on_stone(stone, number_of_blinks)
    
    return stone_list_after_blink


if __name__ == "__main__" :
    test_flag = True
    test_flag = False
    init_inputs(test_flag)
    
    stone_list = read_file(FILE_PATH)
    
    part_1_only = False
    if part_1_only :
        TOTAL_BLINKS_2 = TOTAL_BLINKS_1
    
    '''
    for number_of_blinks in range(TOTAL_BLINKS_2):
        stone_list = blink(stone_list)
        print(number_of_blinks+1, "blinks. Number of stones:", len(stone_list))
        
        if number_of_blinks+1 == TOTAL_BLINKS_1 :
            ans_1 = len(stone_list)
        if number_of_blinks+1 == TOTAL_BLINKS_2 :
            ans_2 = len(stone_list)
    '''
    
    initialize_tree_dict()
    for batch_of_blinks in range(DEPTH,TOTAL_BLINKS_2+DEPTH,DEPTH):
        stone_list = multiple_blink(stone_list, DEPTH)
        print(batch_of_blinks, "blinks. Number of stones:", len(stone_list))
        
        if batch_of_blinks == TOTAL_BLINKS_1 :
            ans_1 = len(stone_list)
        if batch_of_blinks == TOTAL_BLINKS_2 :
            ans_2 = len(stone_list)
    
    print(ans_1)
    print(ans_2)