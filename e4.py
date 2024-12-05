# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 07:55:23 2024

@author: RB0F337L
"""
import os
import re

cwd = os.getcwd()
wd = r'X:\Winpython.385\AoC'

case_file = os.path.join(wd,'in_e4.txt')
test_file = os.path.join(wd,'in_test_e4.txt')

def read_soup(bowl):
    soup = []
    with open(bowl, 'r') as broth:
        for noodle in broth:
            soup.append(noodle.rstrip())
    return soup

def get_noodle_xy_from_loc(noodle_loc,soup_width):
    return noodle_loc // soup_width, noodle_loc % soup_width

def scan_neighbour_noodles_for_XMAS(broth, noodle_bit_loc):
    
    yummy_noodles_found = 0
    broth_height = len(broth)
    broth_width = len(broth[0])
    
    i, j = get_noodle_xy_from_loc(noodle_bit_loc,broth_width)
    
    up_condition = i > 2
    down_condition = i < broth_height-3
    left_condition = j > 2
    right_condition = j < broth_width-3
    
    # Vertical noodle going up
    if up_condition :
        noodle_letters = "".join([broth[i-k][j] for k in range(0,4)])
        if noodle_letters == "XMAS":
            yummy_noodles_found += 1
    
    # Vertical noodle going down
    if down_condition :
        noodle_letters = "".join([broth[i+k][j] for k in range(0,4)])
        if noodle_letters == "XMAS":
            yummy_noodles_found += 1
    
    # Horizontal noodle going right
    if right_condition :
        noodle_letters = "".join([broth[i][j+k] for k in range(0,4)])
        if noodle_letters == "XMAS":
            yummy_noodles_found += 1
    
    # Horizontal noodle going left
    if left_condition :
        noodle_letters = "".join([broth[i][j-k] for k in range(0,4)])
        if noodle_letters == "XMAS":
            yummy_noodles_found += 1
    
    # Diagonal noodle going up-right
    if up_condition and right_condition :
        noodle_letters = "".join([broth[i-k][j+k] for k in range(0,4)])
        if noodle_letters == "XMAS":
            yummy_noodles_found += 1
    
    # Diagonal noodle going down-right
    if down_condition and right_condition :
        noodle_letters = "".join([broth[i+k][j+k] for k in range(0,4)])
        if noodle_letters == "XMAS":
            yummy_noodles_found += 1
    
    # Diagonal noodle going down-left
    if down_condition and left_condition :
        noodle_letters = "".join([broth[i+k][j-k] for k in range(0,4)])
        if noodle_letters == "XMAS":
            yummy_noodles_found += 1
    
    # Diagonal noodle going up-left
    if up_condition and left_condition :
        noodle_letters = "".join([broth[i-k][j-k] for k in range(0,4)])
        if noodle_letters == "XMAS":
            yummy_noodles_found += 1
    
    return yummy_noodles_found

def scan_neighbour_noodles_for_CROSSMAS(broth, noodle_bit_loc):
    
    yummy_noodles_found = 0
    broth_height = len(broth)
    broth_width = len(broth[0])
    
    i, j = get_noodle_xy_from_loc(noodle_bit_loc,broth_width)
    
    up_condition = i > 0
    down_condition = i < broth_height-1
    left_condition = j > 0
    right_condition = j < broth_width-1
    
    if up_condition and down_condition and left_condition and right_condition:
        noodle_letters_diag1 = "".join([broth[i+k][j+k] for k in range(-1,2)])
        noodle_letters_diag2 = "".join([broth[i-k][j+k] for k in range(-1,2)])
        
        diag1_check = noodle_letters_diag1 == "MAS" or noodle_letters_diag1 == "SAM"
        diag2_check = noodle_letters_diag2 == "MAS" or noodle_letters_diag2 == "SAM"
        
        if diag1_check and diag2_check :
            yummy_noodles_found += 1
            #print(i,j)
            #print(broth[i-1][j-1:j+2])
            #print(broth[i][j-1:j+2])
            #print(broth[i+1][j-1:j+2])
            #print(noodle_letters_diag1, noodle_letters_diag2)
    
    return yummy_noodles_found

if __name__ == "__main__":
    broth = case_file
    #broth = test_file
    
    soup = read_soup(broth)
    total_yummy_XMAS_noodles = 0
    total_yummy_CROSSMAS_noodles = 0
    noodle_differential_loc = 0
    
    for noodle in soup :
        for noodle_differential in noodle :
            
            if noodle_differential == "X" :
                #print("noodle found! ", noodle_differential_loc)
                
                yummy_noodles = scan_neighbour_noodles_for_XMAS(soup, noodle_differential_loc)
                
                total_yummy_XMAS_noodles += yummy_noodles
            
            if noodle_differential == "A" :
                #print("noodle found! ", noodle_differential_loc)
                
                yummy_noodles = scan_neighbour_noodles_for_CROSSMAS(soup, noodle_differential_loc)
                
                total_yummy_CROSSMAS_noodles += yummy_noodles
            
            noodle_differential_loc +=1
    
    print(total_yummy_XMAS_noodles)
    print(total_yummy_CROSSMAS_noodles)
    