"""
    Written by BCl0c, whose data will produce
    the worst models ever devised by mankind.

    I find my relationship with my code much 
    related to the expectacle i see in rallying.
    I hope to one day be coding like mcrae did
    his driving -> FLAT OUT!
        Of course, while mcrae did all those things
        very fast, all I'm able to flat out is 
        sleeping very little. It is my own way
        of flatting out, i guess.

    There's little danger in a desk job, but we can
    find some in creative ways. Like coding 48 hours
    straight, finishing that deadline in the last 
    possible second, not sleeping and not eating. That
    takes some boldness. You keep pushing until you either
    solve whatever pulled you in or you DIE. That's a
    style of desk job working I find the closest to
    putting your life on the line. Like going to war. 
    Or driving in autosports. But there's something
    more akin to golfing in coding, since when things
    don't go your way, you usually find no one to blame
    but yourself. Its depressing, but you either hack 
    it or don't. but we keep coming back. Because 
    its fun. That and most programmers I've met 
    are hardcore caffeinated closet masochists.

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

        This script would NOT exist if it were not 
        for the fact we got a bunch of nulls (aka nan)
        inside the data. This is a FUCKING MESS of 
        a dataset, but we'll give it some love. And
        boy oh boy, you better hope love will be enough,
        else we're in shit deeper than deep. We fix it 
        OR ELSE!

    2. THE SCRIPT
        This works (or is planned to work) as following:
            1. The data must be located inside the pwd.
            2. We load everyone inside a dataframe. very good.
            3. For every file loaded, clean anything 
                nondesirable, like them FUCKING NANs
            4. merge and save to a new merged .csv
            5. be done with it!

    3. THE EVERY STEP DOCUMENTATION AND LOG.
        this is for the developer (l0c, that's me) to explain 
        what he's doing.

        3.1. the main function.
            if name is main, then we run main and that's our
            entrypoint. anything outside main WILL NOT be 
            called.

            testmain serves to move fast and break shit up.
            DO NOT run testmain if you plan on getting
            something useful, the purpose of testing
            is acquiring knowledge on operations of
            the libraries we're using!

        3.2. Loading the .csv's
            FOR SOME FUCKING REASON inmet decided they
            would export the COMMA SEPARATED VALUES
            using SEMICOLONS
            which is
            not 
            great...
            not at all!

            That said, its an easy fix. sep=";". 
            there, done.

            Also, new mikefoxtrot found -> 
                as the csv exported uses 
                COMMAS to indicate the 
                floats, we need to set
                the decimal variable to "," 
                so read_csv automatically
                recognizes values.
            
            Then setting date is simple task
            of indicatives. Set the format 
            and the correct column

        3.3. The inspection.
            Its an exploratory step to test
            new pandas functionalities and find out
            how to do our operations like sniffing for
            nans and treating them. The BIGSHAME is
            that there is no easy way of iterating 
            through the dataset and simply altering
            the nans. The !correct! way, it seems, 
            is to create a new series and overwrite
            it over the og dataframe. Not great, but 
            it will do. We are indeed handling 
            only about 12k records with about 13 vars
            in its domain. Not a big step, but i'd be
            already FUCKING DONE IF THIS WAS MYSQL FOR
            FUCK SAKE!

            The approach is simple -> every .csv we 
            got works about the same. Then, if they're
            quite similar, if we find an approach that
            works for one, the others may be handled 
            the same or mostly the same. 

        3.4. nan sniffing in a row
            Simple steps. We just return the keys with 
            nans found. The costs are not stratospheric.
            
            Don't be fooled, though. they will mount and
            this might be what kills us. Good thing 
            its a dataset of about a megabyte, not half a gig
            like last time. This means we got plenty of ram
            to throw around. Not as much time. Wish I had 
            about a month for this one. 

            
"""

import pandas as pd
import numpy as np

RADKEY  = "Radiacao (KJ/m²)"
DEBUG   = 1
INSPECT = 1
FILE1   = "./data1-01012023-29062023.csv"
FILE2   = "./data2-30062023-30122023.csv"
FILE3   = "./data3-01012024-29062024.csv"
FILE4   = "./data4-30062024-30122024.csv"
TARGET  = "./dataset1.csv"


# Latter found out this is already implemented inside 
# pandas through interpolate.Not great.
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
    df1 = pd.read_csv(FILE1, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")
    df2 = pd.read_csv(FILE2, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")
    df3 = pd.read_csv(FILE3, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")
    df4 = pd.read_csv(FILE4, sep=";", decimal=",", parse_dates=[0], date_format="%d/%m/%Y")

    # 2. inspection step!
    if INSPECT == 1:
        print(df1.info())
        print(df2.info())
        print(df3.info())
        print(df4.info())

    # 3. process
    nanhandler(df1)
    nanhandler(df2)
    nanhandler(df3)
    nanhandler(df4)

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
if __name__ == "__main__":
    #choose one. comment the other. don't run both.
    main()
    mainInspector()
    




