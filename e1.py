import os

# Global variables

cwd = os.getcwd()
test_file = os.path.join(cwd,'in_test_e1.txt')
case_file = os.path.join(cwd,'in_e1.txt')

def read_inputs(file_path):
    with open(file_path, 'r') as file:
        l_list = []
        r_list = []
        for line in file:
            el = line.split()
            l_list.append(int(el[0]))
            r_list.append(int(el[1]))
    return l_list, r_list

if __name__ == "__main__":
    in_f = case_file
    left_list, right_list = read_inputs(in_f)
    left_list.sort()
    right_list.sort()
    diff_list = [ abs(left_list[i]-right_list[i]) for i in range(len(left_list)) ]
    
    sim_list = [ left_list[i]*right_list.count(left_list[i]) for i in range(len(left_list)) ]
    
    ans_1 = sum(diff_list)
    ans_2 = sum(sim_list)
    print(ans_1)
    print(ans_2)
