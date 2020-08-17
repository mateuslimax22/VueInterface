import flask
from flask import Flask, jsonify,request
import psycopg2
import json
from flask_cors import CORS
from django.core.serializers.json import DjangoJSONEncoder
import pandas as pd
import numpy as np

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/Patient', methods=['GET'])
def SelectClientes():
  try:
    con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
  except:
    print("Não foi possivel acessar o banco de dados")
  
  cur = con.cursor()
  sql= '''SELECT * FROM public.dpatients '''
  cur.execute(sql)
  row_headers=[x[0] for x in cur.description]
  rv = cur.fetchall()
  json_data=[]
  for result in rv:
      json_data.append(dict(zip(row_headers,result)))
  return json.dumps(json_data,sort_keys=True,indent=1,cls=DjangoJSONEncoder)

@app.route('/Result/<int:id>', methods=['GET'])
def SelectResult(id):
  try:
    con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
  except:
    print("Não foi possivel acessar o banco de dados")
  
  cur = con.cursor()
  sql= '''SELECT * FROM public.result WHERE subjectid = %s'''
  cur.execute(sql,[id])
  row_headers=[x[0] for x in cur.description]
  rv = cur.fetchall()
  json_data=[]
  for result in rv:
      json_data.append(dict(zip(row_headers,result)))
  return json.dumps(json_data,sort_keys=True,indent=1,cls=DjangoJSONEncoder)

@app.route('/Ecg/<int:id>', methods=['GET'])
def SelectEcg(id):
  try:
    con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
  except:
    print("Não foi possivel acessar o banco de dados")

  cur = con.cursor()
  sql= '''SELECT valor FROM public.ecg where id = %s '''
  cur.execute(sql,[id])
  row_headers=[x[0] for x in cur.description]
  rv = cur.fetchall()
  json_data=[]
  for result in rv:
      json_data.append(dict(zip(row_headers,result)))
  
  
      
  df = pd.DataFrame(json_data[0], columns=['valor'])
  
  pontos = df["valor"]
  linhaPontos=np.array(pontos)
  PontosInt =list(map(float, linhaPontos))
  listIndice = np.arange(len(linhaPontos))
  c = np.vstack((listIndice, PontosInt)).T
  d = c.tolist()
  dt = pd.DataFrame(c, columns=['Time','Ecg'])
  result = dt.to_json(orient="records")
  parsed = json.loads(result)
  op = json.dumps(parsed, indent=4) 
  
  return op

@app.route('/Temp/<int:id>', methods=['GET'])
def SelectTemp(id):
  try:
    con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
  except:
    print("Não foi possivel acessar o banco de dados")

  cur = con.cursor()
  sql= '''SELECT value1 FROM public.chartevents where itemid = '677' and subjectid = %s; '''
  cur.execute(sql,[id])
  row_headers=[x[0] for x in cur.description]
  rv = cur.fetchall()
  json_data=[]
  for result in rv:
      json_data.append(dict(zip(row_headers,result)))
  
      
  df = pd.DataFrame(json_data, columns=['value1']) 
  pontos = df["value1"]
  linhaPontos=np.array(pontos)
  PontosInt =list(map(float, linhaPontos))
  listIndice = np.arange(len(linhaPontos))
  c = np.vstack((listIndice, PontosInt)).T
  d = c.tolist()
  dt = pd.DataFrame(c, columns=['Time','Temperatura'])
  result = dt.to_json(orient="records")
  parsed = json.loads(result)
  op = json.dumps(parsed, indent=4) 
  
  return op
  

@app.route('/', methods=['GET'])
def welcome():
  return "Bem-vindo api python"

app.run(host="localhost", debug=True)

app.run()