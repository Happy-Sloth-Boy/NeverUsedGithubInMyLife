# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 08:12:27 2024

@author: RB0F337L
"""
import os
import sys

cwd = os.getcwd()
wd = r'X:\Winpython.385\AoC'
sys.path.append(wd)


excercise = 9

case_file = os.path.join(wd,'in_e' + str(excercise) + '.txt')
test_file = os.path.join(wd,'in_test_e' + str(excercise) + '.txt')

'''
FUNCTIONS HERE
'''

def main_param():
    
    global TOTAL_ITEMS, TOTAL_SPACES, TOTAL_FILES
    global TOTAL_BLOCKS, TOTAL_FILES_BLOCKS, TOTAL_SPACES_BLOCKS
    
    TOTAL_ITEMS         = len(LAYOUT_STR)
    TOTAL_SPACES        = TOTAL_ITEMS // 2
    TOTAL_FILES         = TOTAL_ITEMS // 2 + 1
    TOTAL_BLOCKS        = sum( [ int(l)             
                             for l in LAYOUT_STR ] ) 
    TOTAL_FILES_BLOCKS  = sum( [ int(LAYOUT_STR[i]) 
                             for i in range(TOTAL_ITEMS)
                             if  i%2 == 0 ] )
    TOTAL_SPACES_BLOCKS = sum( [ int(LAYOUT_STR[i]) 
                             for i in range(TOTAL_ITEMS)
                             if  i%2 == 1 ] )
    
    create_injection_list_fragmenting()
    
    create_injection_list_whole()

def create_injection_list_fragmenting():
    
    global INJECTION_LIST_FRAG, FIRST_INJECTION_FILE_ID_FRAG
    
    blocks_scanned = 0
    block_is_file = False
    for j_items in range(TOTAL_ITEMS):
        block_is_file = not block_is_file
        blocks_scanned += int(LAYOUT_STR[j_items])
        
        if blocks_scanned >= TOTAL_FILES_BLOCKS :
            FIRST_INJECTION_FILE_ID_FRAG = (j_items+1)//2
            break
    
    INJECTION_LIST_FRAG = []
    if block_is_file :
        offset = blocks_scanned - TOTAL_FILES_BLOCKS
        INJECTION_LIST_FRAG.append( (FIRST_INJECTION_FILE_ID_FRAG, int(offset) ) )
        j_items += 2
    
    if not block_is_file :
        j_items += 1
        
    for j_file in range(j_items, TOTAL_ITEMS, 2) :
        file_id = (j_file+1)//2
        INJECTION_LIST_FRAG.append( (file_id, int(LAYOUT_STR[j_file])) )
    
def create_injection_list_whole():
    
    global INJECTION_LIST_WHOLE, CALC_DICT_WHOLE
    global SPACE_LIST_WHOLE    , SPACE_DICT_WHOLE
    
    INJECTION_LIST_WHOLE = []
    SPACE_LIST_WHOLE = []
    CALC_DICT_WHOLE = {}
    SPACE_DICT_WHOLE = {}
    
    i_block_pos = 0
    for j_layout_pos in range(TOTAL_ITEMS) :
        item_size = int(LAYOUT_STR[j_layout_pos])
        item_id = (j_layout_pos)//2
        if j_layout_pos%2 == 0 :
            CALC_DICT_WHOLE[item_id] = [ item_size , i_block_pos ]
            INJECTION_LIST_WHOLE.append(item_id)
        if j_layout_pos%2 == 1 :
            SPACE_DICT_WHOLE[item_id] = [ item_size , i_block_pos ]
            SPACE_LIST_WHOLE.append(item_id)
        
        i_block_pos += item_size
    
    if DEBUGGING_FLAG_2 == True: 
        print("Injection list prepared:", INJECTION_LIST_WHOLE)
        

def read_file(in_file: str) -> int:
    with open(in_file, 'r') as f:
        file_str = f.read().rstrip()
    return file_str

def checksum_file(f_id: int, f_size: int, i: int) -> int:
    return int( f_id*( 2*i + f_size - 1 )*f_size/2 )

def checksum_str(f_id: int, f_size: int, i: int) -> str:
    return "{f_id} * ( 2*{i} + {f_size} - 1) * {f_size} / 2".format(f_id=f_id, f_size=f_size, i=i)

def treat_file_fragmenting(i_block: int,j_layout: int) -> int:
    
    if DEBUGGING_FLAG_1 == True: 
        print("Processing item {} (file), starting in block {}".format(j_layout, i_block))
    
    file_id = j_layout//2
    file_size = int( LAYOUT_STR[j_layout] )
    
    if i_block + file_size > TOTAL_FILES_BLOCKS :
        file_size = TOTAL_FILES_BLOCKS - i_block
    
    file_sum = checksum_file(file_id, file_size, i_block)
    
    if DEBUGGING_FLAG_1 == True: 
        calc_str = checksum_str(file_id, file_size, i_block)
        print("   File ID:       {}".format(str(file_id))   + chr(10) +
              "   File size:     {}".format(str(file_size)) + chr(10) +
              "   First block i: {}".format(str(i_block))   + chr(10) +
              "   Calculation:   {}".format(calc_str)       + chr(10) +
              "   Result:        {}".format(str(file_sum))  )
    
    return file_sum

def treat_space_fragmenting(i_block: int,j_layout: int) -> int:
    
    if DEBUGGING_FLAG_1 == True: 
        print("Processing item {} (space), starting in block {}".format(j_layout, i_block))
    
    space_sum = 0
    
    space_size = int( LAYOUT_STR[j_layout] )
    next_file_id, next_file_size = INJECTION_LIST_FRAG[-1]
    
    while space_size > next_file_size :
        file_sum = checksum_file(next_file_id, next_file_size, i_block)
        if DEBUGGING_FLAG_1 == True: 
            calc_str = checksum_str(next_file_id, next_file_size, i_block)
            print("   Space size left:        {}".format(str(space_size))      + chr(10) +
                  "   File ID to inject:      {}".format(str(next_file_id))    + chr(10) +
                  "      File size to inject: {}".format(str(next_file_size))  + chr(10) +
                  "      First block i:       {}".format(str(i_block))         + chr(10) +
                  "      Calculation:         {}".format(calc_str)             + chr(10) +
                  "      Result:              {}".format(str(file_sum))        ) 
        
        space_sum += file_sum
        
        
        space_size -= next_file_size
        i_block += next_file_size
        del INJECTION_LIST_FRAG[-1]
        next_file_id, next_file_size = INJECTION_LIST_FRAG[-1]
    
    file_sum = checksum_file(next_file_id, space_size, i_block)
    if DEBUGGING_FLAG_1 == True: 
        calc_str = checksum_str(next_file_id, space_size, i_block)
        print("   Space size left:        {}".format(str(space_size))   + chr(10) +
              "   File ID to inject:      {}".format(str(next_file_id)) + chr(10) +
              "      File size to inject: {}".format(str(space_size))   + chr(10) +
              "      First block i:       {}".format(str(i_block))      + chr(10) +
              "      Calculation:         {}".format(calc_str)          + chr(10) +
              "      Result:              {}".format(str(file_sum))        ) 
    
    space_sum += file_sum
    #space_sum += int( next_file_id * ( 2*i_block + space_size - 1 )*next_file_size/2 )
    
    if space_size == next_file_size :
        del INJECTION_LIST_FRAG[-1]
    else :
        INJECTION_LIST_FRAG[-1] = (next_file_id,next_file_size-space_size)
    
    if DEBUGGING_FLAG_1 == True: 
        print("   Result: {}".format(space_sum))
    
    return int(space_sum)

def move_blocks_fragmenting() -> int:
    
    total_sum = 0
    i_block_position = 0
    j_layout_position = 0
    while i_block_position < TOTAL_FILES_BLOCKS : # still have to move items :
        
        if j_layout_position%2 == 0 :
            total_sum += treat_file_fragmenting(i_block_position,j_layout_position)
        if j_layout_position%2 == 1 :
            total_sum += treat_space_fragmenting(i_block_position,j_layout_position)
        
        i_block_position += int( LAYOUT_STR[j_layout_position] )
        j_layout_position += 1
    
    return total_sum

def look_for_space_dst(f_size: int, i_src: int) -> int:
    
    for space_id in SPACE_LIST_WHOLE :
        space_size , i_dst = SPACE_DICT_WHOLE[space_id]
        
        if f_size <= space_size :
            return space_id, i_dst
        
    return -1, -1

def update_dicts(f_id: int, f_size: int, sp_id: int, i_dst: int) :
    
    CALC_DICT_WHOLE[f_id][1] = i_dst 
    
    SPACE_DICT_WHOLE[sp_id][0] -= f_size
    
    SPACE_DICT_WHOLE[sp_id][1] += f_size
    
    if SPACE_DICT_WHOLE[sp_id][0] == 0:
        SPACE_LIST_WHOLE.remove(sp_id)

def move_blocks_whole() -> int:
    
    i_block_position = 0
    j_layout_position = 0
    
    for file_id in reversed(INJECTION_LIST_WHOLE):
        
        file_size, i_original = CALC_DICT_WHOLE[file_id]
        
        space_id, i_space = look_for_space_dst(file_size, i_original)
        
        if space_id != -1 and i_space < i_original: 
            update_dicts(file_id, file_size, space_id, i_space)
    total_sum = 0
    for file_id in CALC_DICT_WHOLE.keys():
        file_size, i = CALC_DICT_WHOLE[file_id]
        file_sum = checksum_file(file_id, file_size, i)
        total_sum += file_sum
    
    return total_sum
    

if __name__ == "__main__" :
    file_path = case_file
    #file_path = test_file
    
    DEBUGGING_FLAG_1 = False
    DEBUGGING_FLAG_2 = False
    
    LAYOUT_STR = read_file(file_path)
    
    main_param()
    
    ans_1 = move_blocks_fragmenting()
    ans_2 = move_blocks_whole()
    
    print(ans_1)
    print(ans_2)