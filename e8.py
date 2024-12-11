import os

cwd = os.getcwd()
wd = cwd

case_file = os.path.join(wd,'in_e8.txt')
test_file = os.path.join(wd,'in_test_e8.txt')

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

def print_map_sets(map_info, keys = ['main']):
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
            row += 1
        
        H = row
        L = len(line_clean)
        map_info = { 'H' : H , 'L' : L , 'main' : map_str }
    
    return map_info

def get_frequency_list(map_info,key='main'):
    return [ freq for freq in set(map_info[key]) if freq != '.' ]

def build_frequency_dictionary(map_info,key='main') :
    
    frequency_list = get_frequency_list(map_info)
    frequency_dict = { frq:[] for frq in frequency_list}
    
    map_str = map_info[key]
    for i in range(0, len(map_str)) :
        node = map_str[i]
        if node != '.':
            frequency_dict[node].append(i)
    
    return frequency_dict

def find_antinodes_from_pair_no_resonance(n1,n2,H,L):

    x1,y1 = get_xy_from_pos(n1,L)
    x2,y2 = get_xy_from_pos(n2,L)

    xa1, ya1 = 2*x1 - x2, 2*y1 - y2
    xa2, ya2 = 2*x2 - x1, 2*y2 - y1

    antinode_list = []
    if ( 0 <= xa1 < L ) and ( 0 <= ya1 < H ) : 
        antinode_list.append(get_pos_from_xy(xa1,ya1,L))
    
    if ( 0 <= xa2 < L ) and ( 0 <= ya2 < H ) : 
        antinode_list.append(get_pos_from_xy(xa2,ya2,L))

    return antinode_list

def check_branch(x1,y1,x2,y2,H,L):
    node_list = []
    K = 1
    while True :
        xa = (K+1)*x1 - K*x2
        ya = (K+1)*y1 - K*y2

        in_map = ( 0 <= xa < L ) and ( 0 <= ya < H )
        if not in_map :
            break
        
        node_list.append(get_pos_from_xy(xa,ya,L))
        K += 1
    return node_list

def find_antinodes_from_pair_with_resonance(n1,n2,H,L):

    x1,y1 = get_xy_from_pos(n1,L)
    x2,y2 = get_xy_from_pos(n2,L)
    antinode_list = []

    # Branch 1
    antinode_list += check_branch(x1,y1,x2,y2,H,L)
    antinode_list += check_branch(x2,y2,x1,y1,H,L)
    
    return antinode_list
    
def find_antinodes_for_frequency_no_resonance(nodes,H,L):
    antinode_locations = []
    for i in range(0,len(nodes)-1) :
        n1 = nodes[i]
        for j in range(i+1, len(nodes)) :
            n2 = nodes[j]
            for antinodes in find_antinodes_from_pair_no_resonance(n1,n2,H,L): 
                antinode_locations.append(antinodes)
    return list(set(antinode_locations))

def find_antinodes_for_frequency_with_resonance(nodes,H,L):
    antinode_locations = []
    for i in range(0,len(nodes)) :
        n1 = nodes[i]
        antinode_locations.append(n1)
        for j in range(i+1, len(nodes)) :
            n2 = nodes[j]
            for antinodes in find_antinodes_from_pair_with_resonance(n1,n2,H,L): 
                antinode_locations.append(antinodes)
    return list(set(antinode_locations))

def get_unique_node_locations(node_dict):
    node_locations = []
    for node_list in node_dict.values() :
        node_locations += node_list
    return len(set(node_locations))

if __name__ == "__main__" :

    in_f = case_file
    #in_f = test_file

    antenna_map = read_file(in_f)
    H = antenna_map['H']
    L = antenna_map['L']
    frequency_dictionary = build_frequency_dictionary(antenna_map)

    antinode_no_resonance_dict = {}
    antinode_with_resonance_dict = {}
    
    for frequency in frequency_dictionary.keys():
        nodes_at_frequency = frequency_dictionary[frequency]
        antinode_loc_no_resonance = find_antinodes_for_frequency_no_resonance(nodes_at_frequency,H,L)
        antinode_loc_with_resonance = find_antinodes_for_frequency_with_resonance(nodes_at_frequency,H,L)
        antinode_no_resonance_dict[frequency] = antinode_loc_no_resonance
        antinode_with_resonance_dict[frequency] = antinode_loc_with_resonance
        
    ans_1 = get_unique_node_locations(antinode_no_resonance_dict)
    ans_2 = get_unique_node_locations(antinode_with_resonance_dict)
    print(ans_1)
    print(ans_2)
    
    