"""
    This is an altered version to handle 
    the data 2020-2024. The calling card 
    still holds up, though.    

    Written by BCl0c, whose data will produce
    the worst models ever devised by mankind.

    The initial parts of the .CSVs this script
    is built to handle are actually trash and were
    manually removed. They contained some identifying
    info and stuff, but nothing really useful.

    All one really needs to know is:
        1. The data comes from the automatic 
        weather station in Brasilia - DF, Brazil,
        our lackluster country.
        2. The data was gracefully provided for 
        free by the INMET, a government weather agency.
        3. The data contains some holes, which we'll
        interpolate and is the main purpose of this 
        script, since it is not a very good idea to
        train any statistical model with such good 
        values as NANs and NULLs. 
        4. Listening to aphex twin's "Music From The
        Merch Desk" during the construction or understan-
        ding of this script really helps!
"""

import pandas as pd

#radkey gets special treatment. It should be zeroed instead of 
#interp'd
RADKEY  = "Radiacao (KJ/m²)"

#these controls printings and inspections.
DEBUG   = 1
INSPECT = 1

#These are loaded files
FILE1   = "./INMET_CO_DF_A001_BRASILIA_01-01-2020_A_31-12-2020.csv"
FILE2   = "./INMET_CO_DF_A001_BRASILIA_01-01-2021_A_31-12-2021.csv"
FILE3   = "./INMET_CO_DF_A001_BRASILIA_01-01-2022_A_31-12-2022.csv"
FILE4   = "./INMET_CO_DF_A001_BRASILIA_01-01-2023_A_31-12-2023.csv"
FILE5   = "./INMET_CO_DF_A001_BRASILIA_01-01-2024_A_31-12-2024.csv"

# this controls the output. use a UNIQUE output name for every script
# of this type, else you'll have big ass trouble with overwriting.
TARGET  = "./dataset2.csv"


# Latter found out this is already implemented inside 
# pandas through interpolate and fillna. Not great.
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
    # go through every record
    for i in range(len(df)):
        #in every record, find the nans
        nankeys : list[str] = nanfinder(i, df)
        #if len(nankeys) > 1:
        #    print(nankeys)
        #    input("press enter")

        #hey, we've got some. Then,
        if len(nankeys) > 1 and DEBUG == 1:
                print("RUNNING FOR I = ", i)
                print("before processing:")
                ##
                print(df.loc[i-1])
                print(df.loc[i])
                print(df.loc[i+1])
        for key in nankeys:
            
            if key == RADKEY:
                #print("nan in rads")
                #rads get set to 0.
                df.loc[i, RADKEY] = 0
            # temps get set based on last and next 
            else: 
                if i > 0 and i < len(df) - 1 and key not in ["Data", "Hora (UTC)" ]:

                    df.loc[i, key] = (df.loc[i-1,key] + df.loc[i+1,key])/2

        if len(nankeys) > 1 and DEBUG == 1:
                print("RUNNING FOR I = ", i)
                print("after processing:")
                ##
                print(df.loc[i-1])
                print(df.loc[i])
                print(df.loc[i+1])
        #print(df.loc[i])



def nanfinder(i: int, df: pd.DataFrame) -> list[str]:
    """
        goes through a row and find every key which 
        got a nan.
        returns in a nice enough list. 
    """
    
    itter = df.loc[i].index
    foundkeys: list[str] = []
    for key in itter:
            zed = str(df.loc[i][key])
            if zed == "nan":
                foundkeys.append(key)
    
    return foundkeys


    
    
def runinspection(df1: pd.DataFrame) -> None:
    testindex = 1
    zed = nanfinder(testindex, df1)
    print("indexes with nans! ->", zed)

    print("!DF1HEAD!")
    print(df1.head())

    #THERE WE FUCKING GO!
    #print(df1.loc[1, "Radiacao (KJ/m²)"])
    #df1.loc[1, "Radiacao (KJ/m²)"] = 0
    #print(df1.loc[1, "Radiacao (KJ/m²)"])
    #print("---------------->THISLINEBLANKONPURPOSE")
    
    print("inspecting types!")

    print(df1.dtypes) #in the fucking hell, every damn thing here is a GODDAMN STRING!
    print(df1.info())
    #and as most of these FUCKINGVALUEs are stored as objects
    #we can't get a good describe out of them. not fucking great in the least...
    #most of these SHOULD BE DAMN FLOATS!
    print(df1.describe()) 


def testmain():
    """
        This function is another entrypoint,
        this time to test some functions and 
        stuff.  
    
    """
    df1 = pd.read_csv(FILE1, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")
    df2 = pd.read_csv(FILE2, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")
    df3 = pd.read_csv(FILE3, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")
    df4 = pd.read_csv(FILE4, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")

    print(df1.head())
    print(df1.info)
    newtemp = df1["Temp. Ins. (C)"]
    newtemp = pd.to_numeric(newtemp)
    df1.update(newtemp)
    print(df1.head())
    print(df1.info)
    

    exit(0)

def main():
    # 1. the loading.
    # for whatever reason, prolly because these
    # jackasses thought it would be a good idea to 
    # use SEMICOLONS in the COMMA SEPARATED VALUES
    # format, sep needs to be ; or else. Anyway,

    #THIS IS OUR DATA, THE TARGET OF THIS SCRIPT!
    df1 = pd.read_csv(FILE1, sep=";", decimal=",", parse_dates=[0], date_format="%Y/%m/%d")
    df2 = pd.read_csv(FILE2, sep=";", decimal=",", parse_dates=[0], date_format="%Y/%m/%d")
    df3 = pd.read_csv(FILE3, sep=";", decimal=",", parse_dates=[0], date_format="%Y/%m/%d")
    df4 = pd.read_csv(FILE4, sep=";", decimal=",", parse_dates=[0], date_format="%Y/%m/%d")
    df5 = pd.read_csv(FILE5, sep=";", decimal=",", parse_dates=[0], date_format="%Y/%m/%d")

    # 2. inspection step!
    if INSPECT == 1:
        print(df1.info())
        print(df2.info())
        print(df3.info())
        print(df4.info())
        print(df5.info())


    # 3. process
    #df1.fillna(axis=)

    # 4. second inspection.
    if INSPECT == 1:
        print(df1.info())
        print(df2.info())
        print(df3.info())
        print(df4.info())

    # the merging
    bigdf = pd.DataFrame(pd.concat([df1, df2, df3, df4]))
    #nanhandler(bigdf)

    # not bad!
    #values seem to be alright :>
    print(bigdf.info())
    # the saving
    #still some nans, but we'll bugger them out much faster with this saved to memory
    bigdf.to_csv(TARGET, index = False)
    #nanhandler(bigdf)

    # done :>
    #exit(0)

def mainII():
    """
        this one serves to process the big ones.
        send them here to inspect after saving
        to disk by changing the TARGET constant global.

        this main uses interpolation to fill invalids. 
        Very
        great.
    """
    df = pd.read_csv(TARGET, parse_dates=[0], date_format="%Y-%m-%d")
    df.info()
    df = df.interpolate()
    #That's the fucking way we do it :>
    df.info()
    df.to_csv(TARGET, index = False)
    nanhandler(df)

    exit(0)

def mainInspector():
    """
        This only loads the TARGET, prints
        info and gets out. 
    """
    df = pd.read_csv(TARGET, parse_dates=[0], date_format="%Y-%m-%d")
    #df.info()
    print(df.describe())

def Inspectfiles():
    """
        This only loads the TARGET, prints
        info and gets out. 
    """
    df1 = pd.read_csv(FILE1, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")
    df2 = pd.read_csv(FILE2, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")
    df3 = pd.read_csv(FILE3, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")
    df4 = pd.read_csv(FILE4, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")
    df5 = pd.read_csv(FILE5, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")

    print(df1.info())
    print(df2.info())
    print(df3.info())
    print(df4.info())
    print(df5.info())

    print(df1.describe())
    print(df2.describe())
    print(df3.describe())
    print(df4.describe())
    print(df5.describe())

if __name__ == "__main__":
    #choose one. comment the other. don't run both.
    #testmain()
    Inspectfiles()





