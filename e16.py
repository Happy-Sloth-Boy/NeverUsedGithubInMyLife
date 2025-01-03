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

excercise = 16
tc = 'b'

global CASE_FILE, TEST_FILE
CASE_FILE = os.path.join(wd,'in_e' + str(excercise) + '.txt')
TEST_FILE = os.path.join(wd,'in_test_e' + str(excercise) + tc + '.txt')

global GRID, H, L
global START_POS, X_START, Y_START
global END_POS, X_END, Y_END
global STEP_COST, TURN_COST
global PF_QUEUE, VISITED_NODES
global PT_QUEUE
global DIR_DICT, OPP_DICT
global DEBUG_FLAG

'''
DIR_DICT = { dir : (dx,dy) }
PF_QUEUE = [ (node, optF, cost) ]

'''

'''
FUNCTIONS HERE
'''
def init_globals(in_file: str):
    global GRID, H, L
    global START_POS, X_START, Y_START
    global END_POS, X_END, Y_END
    global STEP_COST, TURN_COST
    global PF_QUEUE, VISITED_NODES
    global PT_QUEUE
    global DIR_DICT, OPP_DICT
    
    GRID = read_grid(in_file)
    H = len(GRID)
    L = len(GRID)
    find_xy_from_sym(GRID, 'S')
    X_END, Y_END = find_xy_from_sym(GRID, 'E')[0]
    END_POS = pos_from_xy(X_END, Y_END, H)
    X_START, Y_START = find_xy_from_sym(GRID, 'S')[0]
    START_POS = pos_from_xy(X_START, Y_START, H)
    
    VISITED_NODES = { }
    PF_QUEUE = []
    PT_QUEUE = []

    STEP_COST = 1
    TURN_COST = 1000

    #DIR_DICT: { dir : ( dx, dy) }
    DIR_DICT = { '>' : (  1,  0) ,
                 '<' : ( -1,  0) ,
                 'v' : (  0,  1) ,
                 '^' : (  0, -1) }
    OPP_DICT = { '>' : '<' ,
                 '<' : '>' ,
                 'v' : '^' ,
                 '^' : 'v' }

def read_grid(in_file: str) -> list :
    with open(in_file, 'r') as f:
        grid_list = [ list(line.rstrip()) for line in f ]
    return grid_list
      
def pos_from_xy(x: int, y: int, H_grid: int) -> int:
    return y*H_grid + x

def xy_from_pos(pos: int, L_grid: int) -> int:
    return pos%L_grid, pos//L_grid

def sym_at_pos(grid_list: list,pos: int) -> str:
    H_grid, L_grid = len(grid_list), len(grid_list[0])
    if pos < 0 or pos >= H_grid * L_grid :
        return ''
    return grid_list[pos//L_grid][pos%L_grid]

def node_from_pos(pos: int,dir: str) -> str:
    return str(pos) + dir

def pos_from_node(node: str) -> tuple:
    return int(node[:-1]), node[-1]

def traspose_map(map_var: list, H_grid: int, L_grid: int) -> list:
    return [ [ map_var[y][x] for y in range(H_grid) ] for x in range(L_grid) ]

def print_map(map_var: list):
    for row in map_var : print(''.join([str(el) for el in row]))

def find_xy_from_sym(grid_list: list, sym: str) -> list :
    return [ (row.index(sym),y) for y,row in enumerate(grid_list) if sym in row ]

def get_step_cost(prev_dir: str, dir: str) -> int:
    if prev_dir == dir :
        return STEP_COST
    return TURN_COST + STEP_COST

def get_heuristic_f(x: int,y: int,xe: int,ye: int, dir: str) -> int:
    dx = xe - x
    dy = ye - y
    x_dir, y_dir = DIR_DICT[dir]

    n_turns = -1
    if   ( dy == 0 and x_dir*dx > 0 ) or ( dx == 0 and y_dir*dy > 0 ) :
        n_turns = 0
    elif ( dy == 0 and x_dir*dx < 0 ) or ( dx == 0 and y_dir*dy < 0 ) :
        n_turns = 2
    elif x_dir*dx < 0 or y_dir*dy < 0 :
        n_turns = 2
    else :
        n_turns = 1
    
    if n_turns == -1 :
        print(x,y,xe,ye,dir)

    if  STEP_COST<TURN_COST:
        n_straight = abs(dx) + abs(dy)
        return STEP_COST*n_straight + TURN_COST*n_turns
    else:
        raise RuntimeError(f"The heuristic function used is not appropriate for this situation")

def get_queue_object(pos: int, dir:str, next_dir: str, prev_cost: int):
    x, y = xy_from_pos(pos, L)
    dx, dy = DIR_DICT[next_dir]
    xn, yn = x+dx, y+dy

    if xn<0 or xn>=L or yn<0 or yn>=H : return None
    if GRID[y][x] == '#' : return None
    
    node = node_from_pos(yn*L+xn, next_dir)
    cost = prev_cost + get_step_cost(dir, next_dir)
    heur = get_heuristic_f(xn, yn, X_END, Y_END, next_dir)
    optF = cost + heur

    if node in VISITED_NODES.keys(): return None

    return (node, optF, cost)

def find_neighbours(node: str, prev_cost: int) -> list:
    neighbours = []
    pos, dir = pos_from_node(node)
    for next_dir in DIR_DICT.keys() :
        q_obj = get_queue_object(pos, dir, next_dir, prev_cost)
        if q_obj is not None: neighbours.append(q_obj)
    
    return neighbours

def mark_node_as_visited(node: str,cost: int):
    VISITED_NODES[node] = cost

def insert_node_in_queue(q: tuple):
    for j in range(len(PF_QUEUE)) :
        if q[1] < PF_QUEUE[j][1] :
            PF_QUEUE.insert(j,q)
            return
    PF_QUEUE.append(q)

def add_neighbours_to_queue(neighbour_list: list):
    for node, optF, cost in neighbour_list :
        node_to_sub = [ (i,q[0],q[1]) for i, q in enumerate(PF_QUEUE) if q[0] == node ]
        
        for i_q, node_q, optF_q in node_to_sub :
            if optF <= optF_q :
                del PF_QUEUE[i_q]
                insert_node_in_queue( (node, optF, cost) )
                
        if len(node_to_sub) == 0 :
            insert_node_in_queue( (node, optF, cost) )

def choose_next_node() -> tuple:
    return PF_QUEUE.pop(0)

def init_alg():
    start_node = node_from_pos(START_POS,'>')
    PF_QUEUE.append( (start_node, 0, 0) )

def run_Astar():

    init_alg() 
    queue_obj = choose_next_node()
    node, cost = queue_obj[0], queue_obj[2]
    
    end_reached = False
    final_cost = 0

    while not end_reached or cost <= final_cost : 
        neighbour_list = find_neighbours(node, cost)
        mark_node_as_visited(node, cost)
        add_neighbours_to_queue(neighbour_list)
        queue_obj = choose_next_node()
        node, cost = queue_obj[0], queue_obj[2]

        if pos_from_node(node)[0] == END_POS :
            end_reached = True
            final_cost = cost
    
    mark_node_as_visited(node, cost)

    return final_cost

def init_path_tracing(fin_cost: int):
    global PT_QUEUE
    nodes_in_path = []
    for dir in DIR_DICT.keys():
        end_node = str(END_POS) + dir
        cost_list = [ cost for node, cost in VISITED_NODES.items() if node == end_node ]
        if fin_cost in cost_list:
            nodes_in_path.append(end_node)
            PT_QUEUE.append((end_node, fin_cost))
    return nodes_in_path

def get_previous_nodes(node: str) -> int:
    pos, dir = int(node[:-1]), node[-1]
    dir = node[-1]
    dx,dy = DIR_DICT[dir]
    prev_pos = pos - dy*L -dx 

    prev_nodes = []
    for prev_dir in OPP_DICT.keys():
        if OPP_DICT[dir] == prev_dir:
            continue
        elif dir == prev_dir:
            prev_nodes.append( (str(prev_pos)+prev_dir, STEP_COST) )
        else:
            prev_nodes.append( (str(prev_pos)+prev_dir, STEP_COST + TURN_COST) )
    
    return prev_nodes

def get_cost_from_node(in_node: int):
    cost_list = [ cost for node, cost in VISITED_NODES.items() if node == in_node ]
    if len(cost_list)>0:
        return cost_list[0]
    return None

def get_pos_list_from_nodes(nodes_list: list) -> list:
    pos_list = []
    for node in nodes_list:
        pos = int(node[:-1])
        if pos not in pos_list :
            pos_list.append(pos)
    return pos_list

def get_all_min_cost_paths(fin_cost: int):
    nodes_in_path = init_path_tracing(fin_cost)
    
    while len(PT_QUEUE) > 0 :
        node, cost = PT_QUEUE.pop(0)
        if node[:-1] == str(START_POS):
            continue
        prev_nodes = get_previous_nodes(node)
        for prev_node, exp_cost_diff in prev_nodes:
            prev_cost = get_cost_from_node(prev_node)
            if prev_cost is None:
                continue
            if prev_node not in nodes_in_path and cost - exp_cost_diff == prev_cost :
                nodes_in_path.append(prev_node)
                PT_QUEUE.append((prev_node, prev_cost))
    
    pos_list = get_pos_list_from_nodes(nodes_in_path)
    
    return pos_list


if __name__ == "__main__" :
    file_path = CASE_FILE
    #file_path = TEST_FILE
    
    init_globals(file_path)
    
    final_cost = run_Astar()
    all_min_cost_paths = get_all_min_cost_paths(final_cost)
    
    ans_1 = final_cost
    ans_2 = len(all_min_cost_paths)

    visited_grid = [[ '0' if y*L+x in all_min_cost_paths else GRID[y][x] for x in range(L)  ] for y in range(H)]
    print_map(visited_grid)
    
    print(ans_1)
    print(ans_2)

    n = 1*17+15
    for q in PF_QUEUE:
        if q[0][:-1] == str(n): print(q[0:-1])
    print(H,L,END_POS)
    for vn in VISITED_NODES.items():
        #print(n[0][:-1])
        if vn[0][:-1] == str(n): print(vn)
        #print(vn)
    
    '''
    PF_QUEUE = [ ('10v', 50, 23),
                 ('59^', 59, 30),
                 ('130^', 69, 3),
                 ('59>', 100, 40) ]

    n_list = [ ('59^', 60, 25) , ('5<', 2, 0) , ('59>', 40, 40) ]
    print(PF_QUEUE)
    add_neighbours_to_queue(n_list)
    x = PF_QUEUE.pop(0)
    print(x, PF_QUEUE)
    '''