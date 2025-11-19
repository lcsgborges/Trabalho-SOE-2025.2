# written by l0c!

# this script is a proof of concept on how to load correctly some data into the
# model in a well behaved manner.

# as this is a very small model, it will probably not consume much memory
# overall, so we're not very worried about this.

#initialization
import tensorflow as tf
import pandas as pd
import numpy as np
MODELPATH = '../t24v1.keras'
TESTCSV   = '../../tratamento_de_dados/dataset2.csv'

#loadings
model = tf.keras.model.load_model(MODELPATH)
df = pd.read_csv(TARGET, parse_dates=[0], date_format="%Y-%m-%d")

#next, we reformat data so the model understands and we may compare
#what we got.

#normalize and reshape steps
inp = df['Temp. Ins. (C)'][1:121].to_numpy()
mean = inp.mean()
std = inp.std()
inp = (inp - inp.mean())/ inp.std()
npinp = inp.reshape(1,24,3)

#get predictions
predictions = model.predict(npinp)

#denormalize
predictions = (predictions * mean) + std

print(npinp)
print(predictions)

