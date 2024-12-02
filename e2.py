import os

# Global variables

cwd = os.getcwd()
wd = cwd
test_file = os.path.join(wd,'in_test_e2.txt')
case_file = os.path.join(wd,'in_e2.txt')

def read_inputs(file_path):
    with open(file_path, 'r') as file:
        all_reports = []
        for line in file:
            all_reports.append([ int(level) for level in line.split() ])
    return all_reports
 
def create_diff(report) :
    diff_list = [ report[i-1] - report[i] for i in range(1,len(report)) ]
    return diff_list
 
 
def check_line_safety(report) :
    diff_list = create_diff(report)
    monotone_ascending = all([el > 0 for el in diff_list])
    monotone_descending = all([el < 0 for el in diff_list])
    monotone = monotone_ascending or monotone_descending
    max_diff = max(diff_list) < 4 and min(diff_list) > -4
    return monotone and max_diff

def inefficient_method(report):
    if check_line_safety(report) :
        return True
    else :
        for i in range(0,len(report)):
            new_report = report[:i] + report[i+1:]
            if check_line_safety(new_report) :
                return True
    return False

if __name__ == "__main__":
    in_f = case_file
    #in_f = test_file
    
    report_list = read_inputs(in_f)
    #report_list = []
    ans_1 = 0
    ans_2 = 0
    for r in report_list:
        if check_line_safety(r):
            ans_1 += 1
        if inefficient_method(r) :
            ans_2 += 1
    
    print(ans_1)
    print(ans_2)
    