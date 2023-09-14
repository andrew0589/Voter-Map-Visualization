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
    if myresult:
        for x in myresult:
            return x[2]
    else:
         return 'rgba(0, 0, 0 ,0.8)'
         
         

# read the file, obligatorio con sep
df = pd.read_csv(r"C:\\Users\\Andrew\\Desktop\\fibwi\\Generales23\\totales_escrutinio_3_0.csv", sep=";", index_col=False, header=None)



# make the column name from 0 to len de columns
df.columns = range(len(df.columns))

# Shows all the code without PR(Provincia)
df = df[df[1] == 'TO']

df.to_excel(r"C:\\Users\\Andrew\\Desktop\\fibwi\\Generales23\\senato_prova.xlsx", index=False)
# Eliminar unneccessary column
column_index = [0, 2, 3, 6, 7,8, 9,10,11,12,13,14,15,16,17,18]
df = df.drop(df.columns[column_index], axis=1)


# Eliminar todo despues de ....
df = df.iloc[:, :45]

# delete empty spaces
df_selected_without_spaces = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


codigo_de_la_candidatura = {}
siglas_de_la_candidatura = {}
senadores_electos_de_la_candidatura = {}
colores_candidaturas = []
array_carosel_senadores_electos = []
df_selected_without_spaces.to_excel(r"C:\\Users\\Andrew\\Desktop\\fibwi\\Generales23\\senato_prova.xlsx", index=False)
for i in range(len(df_selected_without_spaces)):
    key = df_selected_without_spaces.iloc[i:i+1, 3::7].values.tolist()
    codigo_de_la_candidatura[i] = key[0]
    key = df_selected_without_spaces.iloc[i:i+1, 4::7].values.tolist()
    siglas_de_la_candidatura[i] = key[0]
    key = df_selected_without_spaces.iloc[i:i+1, 9::7].values.tolist()
    senadores_electos_de_la_candidatura[i] = key[0]



z = []
for x in range(len(codigo_de_la_candidatura[0])):
    z.append(get_color(codigo_de_la_candidatura[0][x]))

colores_candidaturas.append(z)
print(len(codigo_de_la_candidatura[0]))
dictionar_interior = {}
datasets = []
dictionari = {}

dictionar_interior['backgroundColor'] = colores_candidaturas
dictionar_interior['data'] = senadores_electos_de_la_candidatura
dictionar_interior['borderWidth'] = 0
datasets.append(dictionar_interior)
dictionari['labels'] = siglas_de_la_candidatura
dictionari['datasets'] = datasets

json_object = json.dumps(dictionari, indent=4)
with open(f"senatoindividual.json", "w") as outfile:
        outfile.write(json_object)



df_selected_without_spaces.to_excel(r"C:\\Users\\Andrew\\Desktop\\fibwi\\Generales23\\senato_prova.xlsx", index=False)
