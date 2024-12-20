# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:07:21 2024

@author: RB0F337L
"""

import os

cwd = os.getcwd()
wd = r'X:\Winpython.385\AoC'

excercise = 13

global CASE_FILE, TEST_FILE
CASE_FILE = os.path.join(wd,'in_e' + str(excercise) + '.txt')
TEST_FILE = os.path.join(wd,'in_test_e' + str(excercise) + '.txt')

global MACHINES_LIST


'''
FUNCTIONS HERE
'''

'''
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400
'''

def process_file(in_file: str)  :
    global MACHINES_LIST
    MACHINES_LIST = []
    with open(in_file, 'r') as f:
        for line in f:
            if "Button A:" in line:
                A_inputs = [ int(el.split("+")[1]) for el in line.rstrip().split(",") ]
                
            if "Button B:" in line:
                B_inputs = [ int(el.split("+")[1]) for el in line.rstrip().split(",") ]
                
            if "Prize:" in line:
                prize_inputs = [ int(el.split("=")[1]) for el in line.rstrip().split(",") ]
                MACHINES_LIST.append(A_inputs + B_inputs + prize_inputs)
                

def get_price(nA: int, nB: int) -> int:
    return 3*nA + nB

def find_minimum(xA: int, xB: int,  xP: int) -> int:
    tokens, NA, NB = 0, 0, 0 
    
    mA = (3 - xA/xB)
    if mA >= 0 and xB != 0:
        while NB >= 0:
            NB = ( xP - NA*xA ) / xB
            if NB.is_integer() and NB >= 0:
                return get_price(NA, NB)
            NA += 1
    
    elif xA != 0:
        while NA >= 0:
            NA = ( xP - NB*xB ) / xA
            if NA.is_integer() and NA >= 0:
                tokens = 3*NA + NB
                return get_price(NA, NB)
            NB += 1
    
    return 0

def process_machine(dxA: int, dyA: int, 
                    dxB: int, dyB: int, 
                     xP: int,  yP: int) -> int :
    
    det_D = dxA*dyB - dxB*dyA
    
    if det_D != 0 :
        nA = (   xP*dyB - yP*dxB ) / det_D
        nB = ( - xP*dyA + yP*dxA ) / det_D
        
        if nA.is_integer() and nB.is_integer():
            return get_price(int(nA), int(nB))
        return 0
    
    det_DP = dxA*yp - xp*dyA
    
    if det_D != 0 :
        return 0
    
    return find_minimum()


if __name__ == "__main__" :
    file_path = CASE_FILE
    #file_path = TEST_FILE
    
    process_file(file_path)
    
    total_tokens_1 = 0
    total_tokens_2 = 0
    for dxA, dyA, dxB, dyB, xP, yP in MACHINES_LIST :
        tokens_part_1 = process_machine(dxA, dyA, dxB, dyB, xP, yP)
        
        dp = 10000000000000
        tokens_part_2 = process_machine(dxA, dyA, dxB, dyB, xP+dp, yP+dp)
        
        print("Machine 1:", tokens_part_1, tokens_part_2)
        total_tokens_1 += tokens_part_1
        total_tokens_2 += tokens_part_2
    
    ans_1 = total_tokens_1
    ans_2 = total_tokens_2
    
    print(ans_1)
    print(ans_2)