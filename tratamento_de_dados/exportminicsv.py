"""
    this exports 240 values for testing.
"""

import pandas as pd
DEBUG   = 1
INSPECT = 1

TARGET  = "./dataset2.csv"
EXPORT  = "./mini.csv"

INSTEMPKEY = "TEMPERATURA DO AR - BULBO SECO, HORARIA (C)"
MAXTEMPKEY = "TEMPERATURA MAXIMA NA HORA ANT. (AUT) (C)"
MINTEMPKEY = "TEMPERATURA MINIMA NA HORA ANT. (AUT) (C)"

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
    df = df[[INSTEMPKEY, MINTEMPKEY, MAXTEMPKEY]][:240]
    df.to_csv(EXPORT, index=False)
    exit(0)

if __name__ == "__main__":
    #choose one. comment the other. don't run both.
    #testmain()
    mainII()