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
df = pd.read_csv(r"C:\\Users\\Andrew\\Desktop\\Generales23\\totales_escrutinio_3_0.csv", sep=";", index_col=False, header=None)

# make the column name from 0 to len de columns
df.columns = range(len(df.columns))

# Shows all the code without PR(Provincia)
df = df[df[1] == 'CI']

# Eliminar unneccessary column
column_index = [0, 1, 2, 3, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
df = df.drop(df.columns[column_index], axis=1)

# Eliminar todo despues de los primeros 6 mas votados
df = df.iloc[:, :59]

# delete empty spaces
df_selected_without_spaces = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


codigo_de_la_candidatura = {}
siglas_de_la_candidatura = {}
nombre_del_candidato = {}
colores_candidaturas = []
array_carrosel = []

for i in range(len(df_selected_without_spaces)):
    key = df_selected_without_spaces.iloc[i:i+1, 3::7].values.tolist()
    codigo_de_la_candidatura[i] = key[0]
    key = df_selected_without_spaces.iloc[i:i+1, 4::7].values.tolist()
    siglas_de_la_candidatura[i] = key[0]
    key = df_selected_without_spaces.iloc[i:i+1, 6::7].values.tolist()
    nombre_del_candidato[i] = key[0]
    


for y in range(len(codigo_de_la_candidatura)):
    z = []
    for x in range(len(codigo_de_la_candidatura[y])):
        z.append(get_color(codigo_de_la_candidatura[y][x]))
    colores_candidaturas.append(z)

for i in range(len(codigo_de_la_candidatura)):
    dictionario_diputados={
        'backgroundColor': colores_candidaturas[i],
        #'codigo_de_la_candidatura' : codigo_de_la_candidatura[i],
        #'data' : votos_de_la_candidatura[i], #Numero de votos
        #'data' : porcentaje_de_votos[i], #porcentaje_de_votos
        'siglas' : siglas_de_la_candidatura[i], #Numero de diputados
        'nombre' : nombre_del_candidato[i]
        
    }

    array_carrosel.append(dictionario_diputados)

json_object_porcentaje = json.dumps(array_carrosel, indent=4)
with open(f"Candidatos_al_senado.json", "w") as outfile:
    outfile.write(json_object_porcentaje)
df_selected_without_spaces.to_excel(r"C:\\Users\\Andrew\\Desktop\\Generales23\\candidatos_al_sen.xlsx", index=False)

