# written by l0c!

# this script is a proof of concept on how to load correctly some data into the
# model in a well behaved manner.

# as this is a very small model, it will probably not consume much memory
# overall, so we're not very worried about this.

#initialization
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

MODELPATH = './t120v1.keras'
TARGET    = './../tratamento_de_dados/dataset2.csv'
TARGET2   = './mini.csv'
CONV_WIDTH = 3
OUT_STEPS = 120
MAX_EPOCHS = 20
INSTEMP   = 'TEMPERATURA DO AR - BULBO SECO, HORARIA (C)'
MINTEMP   = 'TEMPERATURA MINIMA NA HORA ANT. (AUT) (C)'
MAXTEMP   = 'TEMPERATURA MAXIMA NA HORA ANT. (AUT) (C)'

INSTEMP2   = 'ins'
MINTEMP2   = 'min'
MAXTEMP2   = 'max'

FIGUREPATH = None

def custom(x):
	return x[:, -CONV_WIDTH:, : ]

def gen_plot24(values, path="fig"):
  #side effects: will change import name to plt, will change 
  values = values.reshape(3, 24)
  x1 = values[0]
  x2 = values[1]
  x3 = values[2]
  plt.plot(x1)
  plt.plot(x2)
  plt.plot(x3)
  plt.savefig(path)

def gen_plot120(values):
  #side effects: will change import name to plt, will change 
  values = values.reshape(3, 120)
  x1 = values[0]
  x2 = values[1]
  x3 = values[2]
  plt.plot(x1)
  plt.plot(x2)
  plt.plot(x3)
  plt.savefig(path)

#loadings
tf.keras.config.enable_unsafe_deserialization()
model = tf.keras.models.load_model(MODELPATH)
#df = pd.read_csv(TARGET, parse_dates=[0], date_format="%Y-%m-%d")
df = pd.read_csv(TARGET2)
print(df.info())
#next, we reformat data so the model understands and we may compare
#what we got.

#normalize and reshape steps

#inp = df[[INSTEMP, MINTEMP, MAXTEMP]][1:121].to_numpy()
inp = df[[INSTEMP2, MINTEMP2, MAXTEMP2]][1:121].to_numpy()
mean = inp.mean()
std = inp.std()
inp = (inp - inp.mean())/ inp.std()
npinp = inp.reshape(1,120,3)

#get predictions
CONV_WIDTH = 3 #MAGIC NUMBER!
predictions = model.predict(npinp)

#denormalize
predictions = (predictions * mean) + std

if(FIGUREPATH == None):
	gen_plot120(predictions)
else:
	gen_plot120(predictions, FIGUREPATH)



