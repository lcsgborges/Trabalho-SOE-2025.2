#initialization
import tensorflow as tf
import pandas as pd
import numpy as np
MODELPATH = 't24v1.keras'
TESTCSV   = '../tratamento_de_dados/dataset1.csv'

#loadings
model = tf.keras.model.load_model(MODELPATH)
df = pd.read_csv(TARGET, parse_dates=[0], date_format="%Y-%m-%d")

#next, we reformat data so the model understands and we may compare 
#what we got.

inp = df['Temp. Ins. (C)'][1:49].to_numpy()
inp.shape = (2,24)

#get predictions
predictions = model.predict(inp[0])

counter = 0
print("--------")
for a,b in zip(predictions, inp[1]):
	print("|", counter, "|", a, "|", b, "|")


