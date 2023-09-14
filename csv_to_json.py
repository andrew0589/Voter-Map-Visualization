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
df = pd.read_csv(r"C:\\Users\\Andrew\\Desktop\\Generales23\\totales_escrutinio_2_119 (1).csv", sep=";", index_col=False, header=None)

# make the column name from 0 to len de columns
df.columns = range(len(df.columns))

# Shows all the code without PR(Provincia)
df = df[df[1] != 'PR']

# Eliminar unneccessary column
column_index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
df = df.drop(df.columns[column_index], axis=1)

# Eliminar todo despues de los primeros 6 mas votados
# 1 voto mas +5
df = df.iloc[:, :40]

# delete empty spaces
df_selected_without_spaces = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# apply precentages to the columns percentaje de votos a la candidatura
df_selected_without_spaces.iloc[:, 3::5] = df_selected_without_spaces.iloc[:, 3::5].apply(lambda x: round((x / 10000)*100, 2))


codigo_de_la_candidatura = {}
siglas_de_la_candidatura = {}
votos_de_la_candidatura = {}
porcentaje_de_votos = {}
diputados_electos = {}
array_carosel_porcentaje = []
array_carosel_diputados = []
array_carosel_votos = []
colores_candidaturas = []

for i in range(len(df_selected_without_spaces)):
    key = df_selected_without_spaces.iloc[i:i+1, 0::5].values.tolist()
    codigo_de_la_candidatura[i] = key[0]
    key = df_selected_without_spaces.iloc[i:i+1, 1::5].values.tolist()
    siglas_de_la_candidatura[i] = key[0]
    key = df_selected_without_spaces.iloc[i:i+1, 2::5].values.tolist()
    votos_de_la_candidatura[i] = key[0]
    key = df_selected_without_spaces.iloc[i:i+1, 3::5].values.tolist()
    porcentaje_de_votos[i] = key[0]
    key = df_selected_without_spaces.iloc[i:i+1, 4::5].values.tolist()
    diputados_electos[i] = key[0]



for y in range(len(codigo_de_la_candidatura)):
    z = []
    for x in range(len(codigo_de_la_candidatura[y])):
        z.append(get_color(codigo_de_la_candidatura[y][x]))
    colores_candidaturas.append(z)
print(codigo_de_la_candidatura)
for i in range(len(codigo_de_la_candidatura)):
    dictionario_diputados={
        'backgroundColor': colores_candidaturas[i],
        #'codigo_de_la_candidatura' : codigo_de_la_candidatura[i],
        #'data' : votos_de_la_candidatura[i], #Numero de votos
        #'data' : porcentaje_de_votos[i], #porcentaje_de_votos
        'data' : diputados_electos[i], #Numero de diputados
        'labels' : siglas_de_la_candidatura[i]
        
    }
    dictionario_porcentaje={
        'backgroundColor': colores_candidaturas[i],
        'data' : porcentaje_de_votos[i], #porcentaje_de_votos
        'labels' : siglas_de_la_candidatura[i]
        #'codigo_de_la_candidatura' : codigo_de_la_candidatura[i],
        #'data' : votos_de_la_candidatura[i], #Numero de votos
        #'data' : diputados_electos[i], #Numero de diputados
        
    }
    dictionario_votos={
        'backgroundColor': colores_candidaturas[i],
        #'codigo_de_la_candidatura' : codigo_de_la_candidatura[i],
        'data' : votos_de_la_candidatura[i], #Numero de votos
        'labels' : siglas_de_la_candidatura[i],
        #'data' : porcentaje_de_votos[i], #porcentaje_de_votos
        #'data' : diputados_electos[i], #Numero de diputados
        
    }
    array_carosel_porcentaje.append(dictionario_porcentaje)
    array_carosel_diputados.append(dictionario_diputados)
    array_carosel_votos.append(dictionario_votos)

background_color = []



#----------------------------------json individual----------------------------------------
dictionar_interior = {}
datasets = []
dictionari = {}
#

for x in range(3):
    lista = [array_carosel_votos, array_carosel_diputados, array_carosel_porcentaje]
    
    dictionar_interior['backgroundColor'] = colores_candidaturas[0]
    dictionar_interior['data'] = lista[x][0]['data']
    dictionar_interior['borderWidth'] = 0
    datasets.append(dictionar_interior)
    dictionari['labels'] = siglas_de_la_candidatura[0]
    dictionari['datasets'] = datasets

    names = ['votos', 'diputados', 'porcentaje']
    json_object = json.dumps(dictionari, indent=4)
    with open(f"individual_{names[x]}.json", "w") as outfile:
        outfile.write(json_object)

    dictionar_interior.clear()
    datasets.clear()

# ------------------- json carrosel para votos, diputados, porcentaje ------------------------
   
for x in range(3):
    lista = [array_carosel_votos, array_carosel_diputados, array_carosel_porcentaje]
    names = ['votos', 'diputados', 'porcentaje']
    json_object_porcentaje = json.dumps(lista[x], indent=4)
    with open(f"carrosel_{names[x]}.json", "w") as outfile:
        outfile.write(json_object_porcentaje)



df_selected_without_spaces.to_excel(r"C:\\Users\\Andrew\\Desktop\\Generales23\\totales_escruti.xlsx", index=False)
