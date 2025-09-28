"""
    Written by BCl0c, whose data will produce
    the worst models ever devised by mankind.

    1. INTRODUCTION
        The expectative is that this is able to output 
        a single clean .csv from the file provided.

        This will be hardcoded for simplicity's sake.
        Since most probably you'd need to do this 
        differently for every dataset, there's 
        no actual advantage to try to make this 
        general. Pandas is already general enough.

        Anyway, given a good dataset, we need to extract
        temperature, humidity and pressure, which is the
        same data our sensor will provide. 

        That all said, IF THERE'S A MIKEFOXTROT
        INSIDE THIS SCRIPT, it's FOXTROT OVER! Our 
        model is just as good as the data provided.

        ALPHASIERRA data means an ALPHASIERRA model. 

        As for the data, it was gathered via
        https://tempo.inmet.gov.br/TabelaEstacoes/A001 
    2. THE SCRIPT
        This works (or is planned to work) as following:
            1. The data must be located inside the pwd.
            2. We load everyone inside a dataframe. very good.
            3. For every file loaded, clean anything but the


"""

import pandas as pd
import numpy as np

FILE1 = "./data1-01012023-29062023.csv"
FILE2 = "./data2-30062023-30122023.csv"
FILE3 = "./data3-01012024-29062024.csv"
FILE4 = "./data4-30062024-30122024.csv"

def dropper(df: pd.DataFrame) -> None:
    """
        drops select columns which 
        will most certainly not
        be useful. 

        at all.
    """
    
    pass

def nanhandler(df: pd.DataFrame) -> None:
    """
        passes through every single record
        inside the dataframe and handles 
        nans.

        If it is unable to gracefully handle
        a record missing, it WILL erase 
        the record. 

        if there's a nan in radiation, the first
        pass will set it to 0.

        if there's nan inside a temperature or
        anything else, it will set it to the 
        mean between the before and after re-
        cords. 
    """

    for i in range(len(df)):
        for j in df.loc[i].index:
            pass

def nanfinder(i: int, df: pd.DataFrame):
    itter = df.loc[0].index
    foundkeys = []
    for key in itter:
            zed = str(df.loc[0][key])
            if zed == "nan":
                foundkeys.append(key)

    return foundkeys
    
    
    

def main():
    # 1. the loading.
    # for whatever reason, prolly because these
    # jackasses thought it would be a good idea to 
    # use SEMICOLONS in the COMMA SEPARATED VALUES
    # format, sep needs to be ; or else.
    df1 = pd.read_csv(FILE1, sep=";")
    df2 = pd.read_csv(FILE2, sep=";")
    df3 = pd.read_csv(FILE3, sep=";")
    df4 = pd.read_csv(FILE4, sep=";")

    # inspecting inspecting :>
    # imported fine.
    """
    print(df1.head())
    print(df1.tail())
    print(df2.head())
    print(df2.tail())
    print(df3.head())
    print(df3.tail())
    print(df4.head())
    print(df4.tail())
    """

    #this step is to devise some test functions for the 

    
    for key in df1.loc[0].index:
        zed = str(df1.loc[0][key])
        if zed == "nan":
            print("found nan in key", key)

    print(df1.head())
    print(df1.loc[1])
    df1.loc[1]["Radiacao (KJ/m²)"] = 0
    print(df1.loc[1])
    

    
    


    # the processing
    #nanhandler(df1)
    # the merging

    # the saving

    # done :>
    exit(0)
    
 

if __name__ == "__main__":
    #print("DATA TREATMENT SCRIPT RUNNNING")
    main()
    




