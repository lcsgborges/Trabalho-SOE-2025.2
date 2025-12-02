# written by l0c!

# this script is a proof of concept on how to load correctly some data into the
# model in a well behaved manner.

# as this is a very small model, it will probably not consume much memory
# overall, so we're not very worried about this.

#initialization
import tensorflow as tf
import pandas as pd
import numpy as np
MODELPATH = './t120v1.keras'
TARGET    = './../tratamento_de_dados/dataset2.csv'
CONV_WIDTH = 3
OUT_STEPS = 120
MAX_EPOCHS = 20
INSTEMP   = 'TEMPERATURA DO AR - BULBO SECO, HORARIA (C)'
MINTEMP   = 'TEMPERATURA MINIMA NA HORA ANT. (AUT) (C)'
MAXTEMP   = 'TEMPERATURA MAXIMA NA HORA ANT. (AUT) (C)'

def custom(x):
	return x[:, -CONV_WIDTH:, : ]
#loadings
tf.keras.config.enable_unsafe_deserialization()
model = tf.keras.models.load_model(MODELPATH)
df = pd.read_csv(TARGET, parse_dates=[0], date_format="%Y-%m-%d")
print(df.info())
#next, we reformat data so the model understands and we may compare
#what we got.

#normalize and reshape steps

inp = df[[INSTEMP, MINTEMP, MAXTEMP]][1:121].to_numpy()
mean = inp.mean()
std = inp.std()
inp = (inp - inp.mean())/ inp.std()
npinp = inp.reshape(1,120,3)

#get predictions
CONV_WIDTH = 3 #MAGIC NUMBER!
predictions = model.predict(npinp)

#denormalize
predictions = (predictions * mean) + std

print(npinp)
print(predictions)

