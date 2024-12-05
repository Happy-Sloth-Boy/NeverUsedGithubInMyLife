# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:09:35 2024

@author: RB0F337L
"""

import os

cwd = os.getcwd()
wd = r'X:\Winpython.385\AoC'

case_file = os.path.join(wd,'in_e5.txt')
test_file = os.path.join(wd,'in_test_e5.txt')

def read_rules(in_file):
    rules_before = { key : [] for key in range(10,100) }
    rules_after  = { key : [] for key in range(10,100) }
    
    # rules_before: dict[x] = [y,z], where x must go before y and z
    # rules_after : dict[x] = [y,z], where x must go after  y and z
    
    with open(in_file, 'r') as f:
        for line in f:
            if "|" not in line:
                return rules_before, rules_after
            
            b,a = line.rstrip().split("|")
            rules_before[int(b)].append(int(a))
            rules_after[int(a)].append(int(b))
            

def clean_rules(rule_book) :
    return { key : list(set(rule_book[key])) for key in rule_book.keys()}


def process_update_list(in_file, rules_before):
    
    total_val_1 = 0
    total_val_2 = 0
    
    with open(in_file, 'r') as f:
        for line in f:
            if "," not in line:
                continue
            
            update_str = line.rstrip().split(",")
            
            add_val = process_update(update_str, rules_before)
            
            total_val_1 += add_val
            
            if add_val == 0 :
                total_val_2 += correct_update(update_str, rules_before)
    
    return total_val_1, total_val_2


def process_update(update_list, rules_before):
    
    len_list = len(update_list)
    
    update = [int(x) for x in update_list]
    
    for i in range(0,len_list-1) : 
        x = update[i]
        y_array = update[i+1:]
        
        for y in y_array :
            if x in rules_before[y] :
                return 0
    
    middle_index = len_list // 2
    return update[middle_index]

def correct_update(update_list, rules_before):
    
    len_list = len(update_list)
    
    update = [int(x) for x in update_list]
    sorted_update = sort_list(update, rules_before, len_list)
    middle_index = len_list // 2
    return sorted_update[middle_index]
    

def sort_list(update, rules_before, len_list):
    sorted_update = update.copy()
    for i in range(1, len_list) :
        bubble = sorted_update[i]
        for j in range(i-1, -1,-1):
            val_above = sorted_update[j]
            if val_above in rules_before[bubble] : 
                sorted_update[j+1] = sorted_update[j]
                sorted_update[j] = bubble
            else :
                continue
    return sorted_update
            

if __name__ == "__main__":
    file_path = case_file
    #file_path = test_file
    
    rules_b, rules_a = read_rules(file_path)
    rules_b = clean_rules(rules_b)
    rules_a = clean_rules(rules_a)
    ans_1, ans_2 = process_update_list(file_path, rules_b)
    
    print(ans_1)
    print(ans_2)