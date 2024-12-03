# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 07:55:23 2024

@author: RB0F337L
"""
import os
import re

cwd = os.getcwd()
wd = r'X:\Winpython.385\AoC'

case_file = os.path.join(wd,'in_e3.txt')
test_file = os.path.join(wd,'in_test_e3.txt')

def multiply_mul_instance(instance):
    n1,n2 = re.sub(r'^.*?\(', '', instance[:-1]).split(",")
    if int(n1)<1000 and int(n2)<1000:
        return int(n1) * int(n2)
    return 0

def update_enable_flag(in_str,flag):
    ## do_match = re.search("do\(\)", txt) ; dont_match = re.search("don't\(\)", txt)
    
    split_by_do = in_str.split("do()")
    split_by_dont = in_str.split("don't()")
    
    if len(split_by_do[-1]) == len(split_by_dont[-1]):
        return flag
    elif len(split_by_do[-1]) < len(split_by_dont[-1]):
        return True
    else:
        return False
        

if __name__ == "__main__":
    file_path = case_file
    #file_path = test_file
    with open(file_path, 'r') as file:
        txt = file.read()
    #txt = r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    
    ans_1 = 0
    enable = True
    part2 = True
    
    mul_match = re.search("mul\(\d+,\d+\)", txt)
    while mul_match is not None :
        start, end = mul_match.span()
        
        if part2 == True:
            enable = update_enable_flag(txt[:start],enable)
        
        if enable :
            ans_1 += multiply_mul_instance(txt[start:end])
        
        txt = txt[end:]
        mul_match = re.search("mul\(\d+,\d+\)", txt)
    
    print(ans_1)