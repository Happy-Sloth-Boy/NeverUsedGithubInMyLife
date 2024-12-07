
import os
import numpy as np

# Global variables

cwd = os.getcwd()
wd = cwd
test_file = os.path.join(wd,'in_test_e7.txt')
case_file = os.path.join(wd,'in_e7.txt')


def read_line(line) :
    result, numbers = line.rstrip().split(":")
    return int(result), [ int(n) for n in numbers.split() ]
    

def read_file(file_path) :
    with open(file_path, 'r') as file:
        eqtn_list = []
        for eqtn in file :
            test_value, numbers_list = read_line(eqtn)
            eqtn_list.append( (test_value, numbers_list) )
    return eqtn_list

def check_eqtn_nc(result, numbers):

    if len(numbers) > 2 :
        last_num = numbers[-1]
        # Case operator *: Check only if result is divisible by last number
        if result%last_num == 0 :
            sub_result = result//last_num
            sub_numbers = numbers[:-1]
            sub_eqtn_possible = check_eqtn_nc(sub_result,sub_numbers)

            if sub_eqtn_possible :
                return True
        
        # Case operator +: Check only if result is larger than or equal to the last number
        if result >= last_num :
            sub_result = result-last_num
            sub_numbers = numbers[:-1]
            sub_eqtn_possible = check_eqtn_nc(sub_result,sub_numbers)

            if sub_eqtn_possible :
                return True
    
    if result == sum(numbers) or result == np.prod(numbers) :
        return True
    return False

def concatenate_numbers(n1,n2):
    return int(str(n1) + str(n2))

def concatenate_first_numbers(numbers_list):
    n1 = numbers_list[0]
    n2 = numbers_list[1]
    return concatenate_numbers(n1,n2)

def check_eqtn_wc(result, numbers):

    if len(numbers) > 2 :
        last_num = numbers[-1]
        # Case operator *: Check only if result is divisible by last number
        if result%last_num == 0 :
            sub_result = result//last_num
            sub_numbers = numbers[:-1]
            sub_eqtn_possible = check_eqtn_wc(sub_result,sub_numbers)

            if sub_eqtn_possible :
                return True
        
        # Case operator +: Check only if result is larger than or equal to the last number
        if result >= last_num :
            sub_result = result-last_num
            sub_numbers = numbers[:-1]
            sub_eqtn_possible = check_eqtn_wc(sub_result,sub_numbers)

            if sub_eqtn_possible :
                return True

        result_str = str(result)
        result_dig = len(result_str)
        last_num_str = str(last_num)
        last_num_dig = len(last_num_str)
        # Case operator ||: only check if end of number is equal to last number
        if result_str[-last_num_dig:] == last_num_str and result_dig > last_num_dig:
            try:
                sub_result = int(result_str[:-last_num_dig])
            except:
                print(result_str, last_num_dig)
                raise RuntimeError("Puto loser!")
            sub_numbers = numbers[:-1]
            sub_eqtn_possible = check_eqtn_wc(sub_result,sub_numbers)

            if sub_eqtn_possible :
                return True
        
        return False
    
    if result == sum(numbers) or result == np.prod(numbers) \
        or result == concatenate_first_numbers(numbers) :
        return True
    return False
        

if __name__ == "__main__" :

    in_f = case_file
    #in_f = test_file
    
    all_equations = read_file(in_f)
    
    calibrations_nc = []
    calibrations_wc = []
    for equation in all_equations :
        eqtn_possible_nc = check_eqtn_nc(equation[0],equation[1])
        if eqtn_possible_nc :
            calibrations_nc.append(equation[0])
        
        eqtn_possible_wc = check_eqtn_wc(equation[0],equation[1])
        if eqtn_possible_wc :
            calibrations_wc.append(equation[0])
    
    ans_1 = sum(calibrations_nc)
    ans_2 = sum(calibrations_wc)
    
    print(ans_1)
    print(ans_2)