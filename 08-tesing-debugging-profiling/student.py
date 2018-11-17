import sys
import numpy as np
import pandas as pd
import json
from scipy import stats
#import matplotlib.pyplot as plt
from datetime import date, timedelta
import math

def make_json(file, mode):
    # to do average
    columns_fonud = []
    student_id = int(mode)

    # student ids column
    s = file.take([0], axis=1)
    line = 0
    for i in range(0, len(s)):
        # print (int(s[:][:].values[i]))
        if int(s[:][:].values[i]) == student_id:
            line = i
            break

    row_tmp = file.take([line], axis=0)
    row_tmp = row_tmp[:][:].values[0]
    #print (row_tmp)
    row_tmp = row_tmp[1:]
    #print (row_tmp)

    array = row_tmp

    mean = np.mean(array)
    median = np.median(array)
    total = sum(array)

    passed = 0
    x = [0]
    y = [0]
    i = 1
    dates = {}
    for item in array:
        if item > 0:
            passed += 1
        x.append(i)
        y.append(y[-1] + item)

        actual = file.columns[i].split("/")[0]
        if actual.strip() in dates:
            dates[actual.strip()] = dates[actual.strip()] + item
        else:
            dates[actual.strip()] = + item

        i += 1
    # print(x)
    # print(y)
    # print(dates)

    semestr_start = "2018-09-17"
    tmp = semestr_start.split("-")
    semestr_start = date(int(tmp[0]), int(tmp[1]), int(tmp[2]))

    max_date = semestr_start

    for column in file.columns:
        if column == "student":
            continue
        actual_date = date(int(column.split("/")[0].split("-")[0]), int(column.split("/")[0].split("-")[1]),
                           int(column.split("/")[0].split("-")[2]))
        if actual_date > max_date:
            max_date = actual_date

    days = (max_date - semestr_start).days

    # print(max_date, days)

    x = [0]
    y = [0]

    for i in range(1, days):
        actual = semestr_start + timedelta(days=i)
        str = '{:%Y-%m-%d}'.format(actual)
        # print (str)
        if str in dates:
            # print ("test")
            x.append(i)
            y.append(y[i - 1] + dates[str])
        else:
            x.append(i)
            y.append(y[i - 1])

    x = np.array(x)
    y = np.array(y)
    x = x[:, np.newaxis]

    a, _, _, _ = np.linalg.lstsq(x, y, rcond=-1)
    # print (a)
    # plt.plot(x, y, 'bo')
    # plt.plot(x, a * x, 'r-')
    # plt.show()
    # slope, intercept, r_value, p_value, std_err = stats.linregress(x[1:], y[1:])
    # print(slope, intercept, r_value, p_value, std_err)

    regression = float(a)
    if a <= 0:
        date_16 = "inf"
        date_20 = "inf"
    else:
        date_16 = '{:%Y-%m-%d}'.format(semestr_start + timedelta(days=math.ceil(16 / regression)))
        date_20 = '{:%Y-%m-%d}'.format(semestr_start + timedelta(days=math.ceil(20 / regression)))

    row = {}
    row["mean"] = mean
    row["median"] = median
    row["total"] = total
    row["passed"] = passed
    row["regression slope"] = regression
    row["date 16"] = date_16
    row["date 20"] = date_20

    dataForJson = row

    json.dump(dataForJson, sys.stdout, indent=4, ensure_ascii=False)


def main():
    # otevreni souboru
    filename= sys.argv[1]
    mode = sys.argv[2]

    file = pd.read_csv(filename)


    if mode=="average":
        avg_student = {}
        for column in file.columns:
            if column == "student":
                avg_student["student"] = [-1]
                continue

            array = file[column][:].values
            avg_student[column] = [np.mean(array)]
        file = pd.DataFrame.from_dict(avg_student)

        make_json(file, -1)

    else:
        make_json(file, mode)

main()
