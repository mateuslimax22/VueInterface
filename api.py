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


@app.route('/SelectSepse', methods=['GET'])
def home():
    try:
      con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
    except:
      print("Não foi possivel acessar o banco de dados")

    cur = con.cursor()

    sql = """ WITH Teste AS ( SELECT subjectid, icustayid, itemid, charttime, value1 FROM public.chartevents)
                  SELECT c1.subjectid, c1.icustayid, c1.itemid, c1.charttime, c1.value1, c2.value1, c3.value1, c4.value1, c5.value1
                  FROM Teste c1, Teste c2, Teste c3, Teste c4, Teste c5
                  WHERE c1.subjectid = c2.subjectid AND c1.subjectid = c3.subjectid AND c1.subjectid = c4.subjectid AND c1.subjectid = c5.subjectid
                  AND c1.icustayid = c2.icustayid AND c1.icustayid = c3.icustayid AND c1.icustayid = c4.icustayid AND c1.icustayid = c5.icustayid
                  AND c1.charttime = c2.charttime AND c1.charttime = c3.charttime AND c1.charttime = c4.charttime AND c1.charttime = c5.charttime
                  AND (c1.itemid = 679 OR c1.itemid = 678 OR c1.itemid = 677 OR c1.itemid = 676)
                  AND (c2.itemid = 615 or c2.itemid = 618 or c2.itemid = 653 or c2.itemid = 1884 or c2.itemid = 3603 or c2.itemid = 3337)
                  AND c3.itemid = 51
                  AND c4.itemid = 52
                  AND c5.itemid = 211
                  LIMIT 5
                  """
    cur.execute(sql)
    rv = cur.fetchall()
    payload = []
    content = {}
    for result in rv:
       content = {'subjectid': result[0], 'icustayid': result[1], 'charttime': result[2], 'itemid': result[3], 'value1': result[4],'value2': result[5],'value3': result[6],'value4': result[7],'value5': result[8]}
       payload.append(content)
       content = {}
    return jsonify(payload)

@app.route('/GetAllLabels', methods=['GET'])
def getAllLabels():
	try:
	  con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
	except:
	  print("Não foi possivel acessar o banco de dados")

	cur = con.cursor()

	sql= '''SELECT subjectid, hadmid, code from public.icd9'''

	cur.execute(sql)
	rv = cur.fetchall()
	labels = []
	for row in rv:
		labels.append(dict(row))
	return jsonify(labels)

@app.route('/GetAllSepesisLabels', methods=['GET'])
def getAllSepesisLabels():
	try:
	  con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
	except:
	  print("Não foi possivel acessar o banco de dados")

	cur = con.cursor()

	sql= ''' SELECT subject_id from public.icd9 WHERE code = '785.52' '''

	cur.execute(sql)
	rv = cur.fetchall()
	labels = []
	for row in rv:
		labels.append(dict(row))
	return jsonify(labels)

@app.route('/AddPatient', methods=['POST'])
def AddUser():
  try:
      con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
      print("conect")
  except:
      print("Não foi possivel acessar o banco de dados")

  _json = request.json
  _subjectid = _json['subjectid']
  _sex = _json['sex']
  _dod = _json['dod']
  _hospitalexpireflg = _json['hospitalexpireflg']
  # validate the received values
  if _subjectid and _sex and _dod and _hospitalexpireflg and request.method == 'POST':
    cur = con.cursor()
    data = (_subjectid, _sex, _dod,_hospitalexpireflg)
    print(data)
    cur.execute("INSERT INTO public.dpatients(subjectid, sex, dob, hospitalexpireflg)VALUES (%s, %s, %s, %s)",data)
    con.commit()
    resp = jsonify('User added successfully!')
    resp.status_code = 200
    return resp
  else:
    return not_found()

@app.route('/Patient/<int:id>', methods=['GET'])
def SelectUser(id):
	try:
	  con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
	except:
	  print("Não foi possivel acessar o banco de dados")

	cur = con.cursor()

	sql= '''SELECT * FROM public.dpatients WHERE subjectid = %s'''

	cur.execute(sql,[id])
	rv = cur.fetchall()
	resp = jsonify(rv)
	return resp

@app.route('/Patient', methods=['GET'])
def SelectPatient():
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

@app.route('/DeletePatientEcg/<int:id>', methods=['GET'])
def DeleteEcg(id):
  try:
    con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
  except:
    print("Não foi possivel acessar o banco de dados")

  cur = con.cursor()
  sql= '''DELETE FROM public.ecgpat WHERE subjectid = %s'''
  cur.execute(sql,[id])
  con.commit()
  resp = jsonify('User deleted successfully!')
  resp.status_code = 200
  return resp

@app.route('/AddBlock', methods=['POST'])
def AddBlock():
  try:
      con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
      print("conect")
  except:
      print("Não foi possivel acessar o banco de dados")

  _json = request.json
  _hadmid = _json['hadmid']
  _collectiondate = _json['collectiondate']
  _ppeak = _json['ppeak']
  _qpeak = _json['qpeak']
  _rpeak = _json['rpeak']
  _speak = _json['speak']
  _tpeak = _json['tpeak']
  _prsegment = _json['prsegment']
  _rrsegment = _json['rrsegment']
  _qtsegment = _json['qtsegment']
  _stsegment = _json['stsegment']
  _qrssegment = _json['qrssegment']
  _temperature = _json['temperature']
  _respiratoryrate = _json['respiratoryrate']
  _systolicbloodpress= _json['systolicbloodpress']
  _meanbloodpressure= _json['meanbloodpressure']
  _heartrate= _json['heartrate']
  _oxygensaturation= _json['oxygensaturation']
  _subjectid= _json['subjectid']
  # validate the received values
  if _hadmid and _collectiondate and  _ppeak and _qpeak and _rpeak and _speak and _tpeak and _prsegment and _rrsegment and _qtsegment and _stsegment and _qrssegment and _temperature and _respiratoryrate and _systolicbloodpress and _meanbloodpressure and _heartrate and _oxygensaturation and _subjectid and request.method == 'POST':
    cur = con.cursor()
    data = (_hadmid, _collectiondate, _ppeak, _qpeak, _rpeak, _speak, _tpeak, _prsegment, _rrsegment, _qtsegment, _stsegment, _qrssegment, _temperature, _respiratoryrate, _systolicbloodpress, _meanbloodpressure, _heartrate, _oxygensaturation, _subjectid)
    print(data)
    cur.execute('''INSERT INTO public.block(
      hadmid, collectiondate, ppeak, qpeak, rpeak, speak, tpeak, prsegment, rrsegment, qtsegment, stsegment, qrssegment, temperature, respiratoryrate, systolicbloodpress, meanbloodpressure, heartrate, oxygensaturation, subjectid)
    	VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''',data)
    con.commit()
    resp = jsonify('Block added successfully!')
    resp.status_code = 200
    return resp
  else:
    return not_found()



@app.route('/UpdatePatientEcg/<string:date>/<int:id>', methods=['PUT'])
def UpdateEcg(id ,date):
  try:
    con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
  except:
    print("Não foi possivel acessar o banco de dados")

  cur = con.cursor()
  sql= '''UPDATE public.ecgpat set flag = 'N' WHERE collectiondate = %s and subjectid = %s '''
  cur.execute(sql,[date,id])
  con.commit()
  resp = jsonify('ECG update successfully!')
  resp.status_code = 200
  return resp

@app.route('/PatientEcgNot', methods=['GET'])
def SelectEcgPats():
	try:
	  con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
	except:
	  print("Não foi possivel acessar o banco de dados")

	cur = con.cursor()

	sql= '''SELECT * FROM public.ecg where flag ='N' '''

	cur.execute(sql)
	rv = cur.fetchall()
	resp = jsonify(rv)
	return resp

@app.route('/AddEcg', methods=['POST'])
def AddEcg():
  try:
      con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
      print("conect")
  except:
      print("Não foi possivel acessar o banco de dados")

  _json = request.json
  _id = _json['id']
  _valor = _json['valor']
  _flag = _json['flag']
  # validate the received values
  if _id and _valor and _flag and  request.method == 'POST':
    cur = con.cursor()
    data = (_id, _valor, _flag)
    cur.execute("INSERT INTO public.ecg(id, valor, flag)VALUES (%s, %s,%s)",data)
    con.commit()
    resp = jsonify('ecg adicionado')
    resp.status_code = 200
    return resp
  else:
    return not_found()

@app.route('/AtualizarFlag/<int:id>', methods=['POST'])
def AttFlag(id):
  try:
      con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
      print("conect")
  except:
      print("Não foi possivel acessar o banco de dados")

  # validate the received values
  if  id or request.method == 'POST':
    cur = con.cursor()
    cur.execute('''UPDATE public.ecg SET  flag='Y' WHERE idecg = %s;''',[id])
    con.commit()
    resp = jsonify('flag att')
    resp.status_code = 200
    return resp
  else:
    return not_found()

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

@app.route('/PressSys/<int:id>', methods=['GET'])
def SelectPressSys(id):
  try:
    con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
  except:
    print("Não foi possivel acessar o banco de dados")

  cur = con.cursor()
  sql= '''SELECT value2num FROM public.chartevents where itemid = '57' or itemid = '51' and subjectid = %s; '''
  cur.execute(sql,[id])
  row_headers=[x[0] for x in cur.description]
  rv = cur.fetchall()
  json_data=[]
  for result in rv:
      json_data.append(dict(zip(row_headers,result)))


  df = pd.DataFrame(json_data, columns=['value2num'])
  pontos = df["value2num"]
  linhaPontos=np.array(pontos)
  PontosInt =list(map(float, linhaPontos))
  listIndice = np.arange(len(linhaPontos))
  c = np.vstack((listIndice, PontosInt)).T
  d = c.tolist()
  dt = pd.DataFrame(c, columns=['Time','Pressâo'])
  result = dt.to_json(orient="records")
  parsed = json.loads(result)
  op = json.dumps(parsed, indent=4)

  return op

@app.route('/PressMain/<int:id>', methods=['GET'])
def SelectPressMain(id):
  try:
    con = psycopg2.connect("dbname='api' user='postgres' host='localhost' password='1502'")
  except:
    print("Não foi possivel acessar o banco de dados")

  cur = con.cursor()
  sql= '''SELECT value1num FROM public.chartevents where itemid = '58' or itemid = '52' and subjectid = %s; '''
  cur.execute(sql,[id])
  row_headers=[x[0] for x in cur.description]
  rv = cur.fetchall()
  json_data=[]
  for result in rv:
      json_data.append(dict(zip(row_headers,result)))


  df = pd.DataFrame(json_data, columns=['value1num'])
  pontos = df["value1num"]
  linhaPontos=np.array(pontos)
  PontosInt =list(map(float, linhaPontos))
  listIndice = np.arange(len(linhaPontos))
  c = np.vstack((listIndice, PontosInt)).T
  d = c.tolist()
  dt = pd.DataFrame(c, columns=['Time','Pressâo'])
  result = dt.to_json(orient="records")
  parsed = json.loads(result)
  op = json.dumps(parsed, indent=4)

  return op





@app.route('/', methods=['GET'])
def welcome():
  return render_template("index.html")
app.run(host="localhost", debug=True)
