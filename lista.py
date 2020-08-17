import pandas as pd
import numpy as np
import json

json_data=[[ { "valor": [ "0.8993157148361206", "0.9530791640281677", "1.1485825777053833", "1.3294233083724976", 
"1.3587487936019897", "1.2316715717315674", "1.0606060028076172", "0.9970674514770508", "1.099706768989563",] }]]

df = pd.DataFrame(json_data[0], columns=['valor'])

pontos = df["valor"]
linhaPontos=np.array(pontos[0])
PontosInt =list(map(float, linhaPontos))
listIndice = np.arange(len(linhaPontos))
c = np.vstack((listIndice, linhaPontos)).T
d = c.tolist()
dt = pd.DataFrame(c, columns=['Time','Ecg'])
op = dt.to_csv(index=False)
dt.set_index('Time', inplace=True)
op2= op.tolist()
print(op2)
 
