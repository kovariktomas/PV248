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
            col = column.split("/")[0]
            # print (col)
            if not (col in columns_fonud):
                columns_fonud.append(col)
                i += 1
                array = file[column][1:].values

                for j in range(i + 1, len(file.columns)):
                    colname = file.columns[j]
                    col_tmp = colname.split("/")[0]
                    if col_tmp == col:
                        array_tmp = file[colname][1:].values
                        # print(array[1], array_tmp[1])
                        array = array + array_tmp
                        # print (array[1])

                    # print(colname)

                mean = np.mean(array)
                median = np.median(array)
                first = np.percentile(array, 25)
                last = np.percentile(array, 75)

                row = {}
                row["mean"] = mean
                row["median"] = median
                row["first"] = first
                row["last"] = last

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

            array = file[column][1:].values
            mean = np.mean(array)
            median = np.median(array)
            first = np.percentile(array, 25)
            last = np.percentile(array, 75)

            row = {}
            row["mean"] = mean
            row["median"] = median
            row["first"] = first
            row["last"] = last

            rows[column.strip()] = row


        dataForJson = rows

        json.dump(dataForJson, sys.stdout, indent=4, ensure_ascii=False)
    elif mode=="exercises":
        rows = {}
        columns_fonud = []

        i = 0
        for column in file.columns:
            if column == "student":
                continue
            #print("actual", column)
            col = column.split("/")[-1]
            #print (col)
            if not (col in columns_fonud):
                columns_fonud.append(col)
                i += 1
                array = file[column][1:].values

                for j in range(i+1,len(file.columns)):
                    colname = file.columns[j]
                    col_tmp = colname.split("/")[-1]
                    if col_tmp == col:
                        array_tmp = file[colname][1:].values
                        #print(array[1], array_tmp[1])
                        array = array + array_tmp
                        #print (array[1])


                    #print(colname)

                mean = np.mean(array)
                median = np.median(array)
                first = np.percentile(array, 25)
                last = np.percentile(array, 75)

                row = {}
                row["mean"] = mean
                row["median"] = median
                row["first"] = first
                row["last"] = last

                rows[col.strip()] = row

        dataForJson = rows

        json.dump(dataForJson, sys.stdout, indent=4, ensure_ascii=False)
    else:
        print("No mode selected!")


main()
