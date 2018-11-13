import sys
import numpy as np
import pandas as pd

def main():
    # otevreni souboru
    filename= sys.argv[1]
    mode = sys.argv[2]

    file = pd.read_csv(filename)


    if mode=="average":

        #to do average
        pass
    else:

        #to do student
        pass

main()
