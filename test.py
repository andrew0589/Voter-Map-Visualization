import pandas as pd
import numpy as np
import locale
import json



# read the file, obligatorio con sep
df = pd.read_csv(r"C:\\Users\\Andrew\\Desktop\\Generales23\\totales_escrutinio_2_119 (1).csv", sep=";", index_col=False, header=None)

# make the column name from 0 to len de columns
df.columns = range(len(df.columns))

# Eliminar unneccessary column
column_index = [0,3,4,6,7,8,10,11,12,13,14,15,16,17,18]
df = df.drop(df.columns[column_index], axis=1)

# Eliminar todo despues de los primeros 6 mas votados
df = df.iloc[:, :34]

# Delete rows where  value is 'PR'
df = df[df[1] != 'PR']



# Select columns Siglas de la candidadura and votos de la candidatura
column_positions = [5 + 5*i for i in range(len(df.columns)//5)]
df_selected = df.iloc[:, sum([[pos, pos+1] for pos in column_positions], [])]


# delete empty spaces
df_selected_without_spaces = df_selected.applymap(lambda x: x.strip() if isinstance(x, str) else x)




dictionario = {}
partidos = {}
votos ={}
array_carosel = []


for i in range(len(df_selected_without_spaces)):
    key = str(df_selected_without_spaces.iloc[i:i+1, 0::2].values.tolist())
    partidos[i] = key
    values = str(df_selected_without_spaces.iloc[i:i+1, 1::2].values.tolist())
    
    votos[i] = values
    


for i in range(len(partidos)):
    dictionario={
        'data' : votos[i],
        'labels' : partidos[i]
    }
    array_carosel.append(dictionario)

print(array_carosel)


json_object = json.dumps(dictionario, indent=4)

#print(json_object)




df_selected.to_excel(r"C:\\Users\\Andrew\\Desktop\\Generales23\\totales_escruti.xlsx", index=False)


#df_selected_without_spaces.to_json(r"C:\\Users\\Andrew\\Desktop\\Generales23\\File Name.json", orient='values')