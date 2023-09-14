import pandas as pd
import numpy as np
import locale
import json
import mysql.connector
import ast

mydb = mysql.connector.connect(
  host="109.232.71.246",
  user="prova",
  password="123456789",
  database="elecciones23j"
)

def get_color(codigo_candidatura):
    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM partidos WHERE codigo_agrupacion={codigo_candidatura} LIMIT 1")
    myresult = mycursor.fetchall()  
    for x in myresult:
        return x[2]
    

# read the file, obligatorio con sep
df = pd.read_excel(r"C:\\Users\\Andrew\\Desktop\\Generales23\\candidatos_al_sen.xlsx")

codigo_de_la_candidatura = {}
siglas_de_la_candidatura = {}
nombre_del_candidato = {}
senadores_electos = {}
colores_candidaturas = []
array_carrosel = []

for i in range(len(df)):
    key = df.iloc[i:i+1, 3::7].values.tolist()
    codigo_de_la_candidatura[i] = key[0]
    key = df.iloc[i:i+1, 4::7].values.tolist()
    siglas_de_la_candidatura[i] = key[0]
    key = df.iloc[i:i+1, 6::7].values.tolist()
    nombre_del_candidato[i] = key[0]
    key = df.iloc[i:i+1, 9::7].values.tolist()
    senadores_electos[i] = key[0]
    





for y in range(len(codigo_de_la_candidatura)):
    z = []
    for x in range(len(codigo_de_la_candidatura[y])):
        z.append(get_color(codigo_de_la_candidatura[y][x]))
    colores_candidaturas.append(z)


dictionario_final = []
for x in range(len(df)):
    new_colores = []
    new_siglas = []
    new_nombres = []
    for y in range(len(senadores_electos[x])):
        if senadores_electos[x][y]:
            new_colores.append(colores_candidaturas[x][y])
            new_siglas.append(siglas_de_la_candidatura[x][y])
            new_nombres.append(nombre_del_candidato[x][y])
    d ={
        'backgroundColor': new_colores,
        'siglas' : new_siglas, 
        'nombre' : new_nombres
    }
    dictionario_final.append(d)
        




#for i in range(len(codigo_de_la_candidatura)):
#    dictionario_diputados={
#        'backgroundColor': colores_candidaturas[i],
#        'siglas' : siglas_de_la_candidatura[i], 
#        'nombre' : nombre_del_candidato[i]
#        
#    }
#
#    array_carrosel.append(dictionario_diputados)


json_object_porcentaje = json.dumps(dictionario_final, indent=4)
with open(f"Candidatos_al_senado.json", "w") as outfile:
    outfile.write(json_object_porcentaje)