import pandas as pd
import numpy as np
import locale
import json
import mysql.connector



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
df_congreso = pd.read_csv(r"C:\\Users\\Andrew\\Desktop\\fibwi\\Generales23\\totales_escrutinio_2_119 (1).csv", sep=";", index_col=False, header=None)
df_senato = pd.read_csv(r"C:\\Users\\Andrew\\Desktop\\fibwi\\Generales23\\totales_escrutinio_3_0.csv", sep=";", index_col=False, header=None)


# make the column name from 0 to len de columns
df_congreso.columns = range(len(df_congreso.columns))
df_senato.columns = range(len(df_senato.columns))

# Shows all the code with TO(Total Estatal)
df_congreso = df_congreso[df_congreso[1] == 'TO']
df_senato = df_senato[df_senato[1] == 'TO']


# Eliminar todo despues de los primeros 6 mas votados
# 1 voto mas +5
df_congreso = df_congreso.iloc[:, :59]
df_senato = df_senato.iloc[:, :68]


# delete empty spaces
df_congreso = df_congreso.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df_senato = df_senato.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# apply precentages to the columns percentaje de votos a la candidatura
df_congreso.iloc[:, 9:10] = df_congreso.iloc[:, 9:10].apply(lambda x: round((x / 10000)*100, 2))
df_congreso.iloc[:, 11:12] = df_congreso.iloc[:, 11:12].apply(lambda x: round((x / 10000)*100, 2))


codigo_de_la_candidatura = {}
siglas_de_la_candidatura = {}
colores_candidaturas = []

for i in range(len(df_senato)):
    key = df_congreso.iloc[i:i+1, 19::5].values.tolist()
    codigo_de_la_candidatura[i] = key[0]
    key = df_congreso.iloc[i:i+1, 20::5].values.tolist()
    siglas_de_la_candidatura[i] = key[0]

escrutado_congreso = float(df_congreso.iat[0,9])
escrutado_senato = float(df_senato.iat[0,9])
porcentaje_votantes = float(df_congreso.iat[0,11])

z = []
for x in range(8):
    z.append(get_color(codigo_de_la_candidatura[0][x]))
colores_candidaturas.append(z)


dictionario_final = {}
dictionario_final['backgroundColor'] = colores_candidaturas[0]
dictionario_final['orden'] = siglas_de_la_candidatura[0]
dictionario_final['escrutado_congreso'] = escrutado_congreso
dictionario_final['escrutado_senato'] = escrutado_senato
dictionario_final['porcentaje_votantes'] = porcentaje_votantes

dictionario_siglas = {}
dictionario_siglas['siglas'] = siglas_de_la_candidatura[0]

json_object_porcentaje = json.dumps(dictionario_final, indent=4)
with open("escrutado_espania.json", "w") as outfile:
    outfile.write(json_object_porcentaje)

json_object = json.dumps(dictionario_siglas, indent=4)
with open("siglas_congreso.json", "w") as outfile:
    outfile.write(json_object)

#df_congreso.to_excel(r"C:\\Users\\Andrew\\Desktop\\fibwi\\Generales23\\df_congreso.xlsx", index=False)
#df_senato.to_excel(r"C:\\Users\\Andrew\\Desktop\\fibwi\\Generales23\\df_senato.xlsx", index=False)
