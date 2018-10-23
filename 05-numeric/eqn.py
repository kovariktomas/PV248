import sys
import re
import numpy as np
import collections

def main():
    filename = sys.argv[1]

    file = open(filename, 'r')

    cnt = 1
    line = file.readline()

    left = []
    right = []
    left_ok = []

    while line:
        if cnt > 1:
            line = file.readline()
        if not line.strip() == "":
            row = line.split("=")
            left.append(row[0].strip())
            right.append(int(row[-1].strip()))
            cnt += 1

    variable_regex = re.compile("((\d*))((\w{1}))")

    cnt = 0
    for left_line in left:
        coef = left_line.split("+")
        left_ok.append({})
        for variable in coef:
            variable = variable.strip()

            if " - " not in variable:
                match = variable_regex.match(variable)
                if match:
                    left_ok[cnt][match.group(3).strip()] = 1 if match.group(1).strip() == ''else int(match.group(1).strip())
            else:
                coef1 = variable.split("-")
                cnt1 = 1
                for variable1 in coef1:
                    variable1 = variable1.strip()
                    if cnt1 > 1:
                        match1 = variable_regex.match(variable1)
                        if match1:
                            left_ok[cnt][match1.group(3).strip()] = -1 if match1.group(1).strip() == '' \
                                else int("-"+match1.group(1).strip())
                    else:
                        match1 = variable_regex.match(variable1)
                        if match1:
                            left_ok[cnt][match1.group(3).strip()] = 1 if match1.group(1).strip() == '' \
                                else int(match1.group(1).strip())
                    cnt1 += 1
        cnt +=1

    #nactena leva strana
    #print (left_ok)

    #promenne, ktere existuji v zadani
    variables_in_file = []
    for dict in left_ok:
        for k, v in dict.items():
            if k not in variables_in_file:
                variables_in_file.append(k)

    #print (sorted(variables_in_file))

    left_side = []

    for row in left_ok:
        set = []
        for key in sorted(variables_in_file):
            #print (key)
            try:
                value = row[key]
                set.append(value)
            except KeyError:
                set.append(0)

        left_side.append(set)

    #print(left_side)
    #print(right)

    #make copy of array
    dimensions_test = np.copy(left_side)
    coef_matrix = left_side
    augmented_matrix = np.c_[dimensions_test, right]
    # https://en.wikipedia.org/wiki/Rouché–Capelli_theorem
    if np.linalg.matrix_rank(coef_matrix) == np.linalg.matrix_rank(augmented_matrix):
        #print("ma reseni")
        n = len(variables_in_file)

        rank_a = np.linalg.matrix_rank(coef_matrix)

        if n == rank_a:
            #print ("prave jedno reseni")
            a = np.array(left_side)
            b = np.array(right)
            x = np.linalg.solve(a, b)

            print("solution:", end='')
            cnt = 0
            for var in sorted(variables_in_file):
                if cnt == 0:
                    print (" ", var, " = ", x[cnt], end='', sep='')
                else:
                    print (", ", var, " = ", x[cnt], end='', sep='')
                cnt += 1
            exit(0)
        else:
            print ("solution space dimension:", n-rank_a, end='')
            exit(0)
        #print (np.linalg.matrix_rank(coef_matrix))
        #print (np.linalg.matrix_rank(augmented_matrix))
    else:
        print("no solution", end='')
        exit(0)


main()
