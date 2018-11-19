import sys
import numpy as np
import pandas as pd
import json

def main():
    # otevreni souboru
    filename = sys.argv[1]
    mode = sys.argv[2]

    file = pd.read_csv(filename)

    #print(file)


    #print(file.columns)

    if mode=="dates":
        rows = {}
        columns_fonud = []

        i = 0
        for column in file.columns:
            if column == "student":
                continue
            # print("actual", column)
            col = column.split("/")[0].strip()
            # print (col)
            i += 1
            #print (" k ")
            #print (col, columns_fonud)
            if not (col in columns_fonud):
                columns_fonud.append(col)

                array = file[column][:].values

                for j in range(i + 1, len(file.columns)):
                    colname = file.columns[j]
                    col_tmp = colname.split("/")[0].strip()
                    #print(j, colname, col_tmp, col)
                    if col_tmp == col:
                        array_tmp = file[colname][:].values
                        # print(array[1], array_tmp[1])
                        array = array + array_tmp
                        # print (array[1])

                    # print(colname)
                passed = 0
                for item in array:
                    if item > 0:
                        passed += 1
                        # print (item)

                mean = np.mean(array)
                median = np.median(array)
                first = np.percentile(array, 25)
                last = np.percentile(array, 75)

                row = {}
                row["mean"] = mean
                row["median"] = median
                row["first"] = first
                row["last"] = last
                row["passed"] = passed

                rows[col.strip()] = row

        dataForJson = rows

        json.dump(dataForJson, sys.stdout, indent=4, ensure_ascii=False)
        #to do dates
        pass
    elif mode=="deadlines":
        rows = {}
        for column in file.columns:
            if column == "student":
                continue

            array = file[column][:].values
            mean = np.mean(array)
            median = np.median(array)
            first = np.percentile(array, 25)
            last = np.percentile(array, 75)

            passed = 0
            for item in array:
                if item > 0:
                    passed += 1
                    #print (item)

            row = {}
            row["mean"] = mean
            row["median"] = median
            row["first"] = first
            row["last"] = last
            row["passed"] = passed

            rows[column.strip()] = row


        dataForJson = rows

        json.dump(dataForJson, sys.stdout, indent=4, ensure_ascii=False)
    elif mode=="exercises":
        rows = {}
        columns_fonud = []

        i = 0
        for column in file.columns:
            #print(" ")
            if column == "student":
                continue
            #print("actual", column)
            col = column.split("/")[-1]
            #print (col)
            i += 1
            #print(col, columns_fonud)
            if not (col in columns_fonud):
                columns_fonud.append(col)

                array = file[column][:].values
                j = 0
                for j in range(i+1,len(file.columns)):
                    colname = file.columns[j]
                    col_tmp = colname.split("/")[-1]
                    #print(j, colname, col_tmp, col)
                    if col_tmp == col:
                        array_tmp = file[colname][:].values
                        #print(array[1], array_tmp[1])
                        array = array + array_tmp
                        #print (array[1])
                        #print (array)

                    #print(colname)
                passed = 0
                for item in array:
                    if item > 0:
                        passed += 1
                        # print (item)

                mean = np.mean(array)
                median = np.median(array)
                first = np.percentile(array, 25)
                last = np.percentile(array, 75)

                row = {}
                row["mean"] = mean
                row["median"] = median
                row["first"] = first
                row["last"] = last
                row["passed"] = passed

                rows[col.strip()] = row

        dataForJson = rows

        json.dump(dataForJson, sys.stdout, indent=4, ensure_ascii=False)
    else:
        print("No mode selected!")


main()
