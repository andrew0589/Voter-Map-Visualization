import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap
import mysql.connector
from pyproj import CRS



# sacar los colores del mysql
mydb = mysql.connector.connect(
  host="109.232.71.246",
  user="prova",
  password="123456789",
  database="elecciones23j"
)


mycursor = mydb.cursor()
mycursor.execute(f"SELECT * FROM partidos")
myresult = mycursor.fetchall()
test = pd.DataFrame(myresult)


    

# read the file, obligatorio con sep
df = pd.read_csv(r"C:\\Users\\Andrew\\Desktop\\Generales23\\totales_escrutinio_2_119 (1).csv", sep=";", index_col=False, header=None)

# make the column name from 0 to len de columns
df.columns = range(len(df.columns))

# Shows all the code without PR(Provincia)
df = df[df[1] != 'PR']


# Eliminar unneccessary column
column_index = [0,1,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18]
df = df.drop(df.columns[column_index], axis=1)

# Eliminar unneccessary column
df = df.iloc[:, :6]
df = df.drop(labels=[0], axis=0)



# delete empty spaces
df_selected_without_spaces = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


df_selected_without_spaces[5] = df_selected_without_spaces[5].replace(
    ['Illes Balears', 'Canarias', 'Comunitat Valenciana', 'Catalunya', 'Ciudad Autónoma de Ceuta'], ['Islas Baleares', 'Islas Canarias', 'Comunidad Valenciana', 'Cataluña', 'Ceuta y Melilla'])



# Read the shapefile of Spain's regions
shapefile_path = (r"C:\\Users\\Andrew\\Desktop\\Generales23\\gadm36_ESP_2.shp")
shape = gpd.read_file(shapefile_path)

shape = pd.merge(
    left = shape,
    right = df_selected_without_spaces,
    left_on = 'NAME_1',
    right_on = 5,
    how = 'left'
)





islas_canarias = shape[shape['NAME_1'] == 'Islas Canarias']
islas_ceuta_y_melilla = shape[shape['NAME_1'] == 'Ceuta y Melilla']





#shape = shape[shape['NAME_1'] != 'Ceuta y Melilla']
shape = shape[shape['NAME_1'] != 'Islas Canarias']

shape[22] = shape[22].apply(lambda x: round((x / 10000)*100, 2))


area_dict = dict(zip(test[0], test[3]))



shape['color'] = shape[19].map(area_dict)
islas_canarias['color'] = islas_canarias[19].map(area_dict)
islas_ceuta_y_melilla['color'] = islas_ceuta_y_melilla[19].map(area_dict)

# Reproject the shape GeoDataFrame to a projected CRS
projected_crs = CRS.from_epsg(3857)
shape = shape.to_crs(projected_crs)


# Create the map plot
fig, (ax1, ax2) = plt.subplots(nrows=2, figsize = (10,8))


# Add labels to each community
#for x, y, label in zip(shape['geometry'].centroid.x, shape['geometry'].centroid.y, shape.NAME_1):
#    ax1.annotate(label, xy=(x, y), xytext=(-20, 0), textcoords="offset points", fontsize=8)
#    
#for x, y, label in zip(shape['geometry'].centroid.x, shape['geometry'].centroid.y, islas_canarias.NAME_1):
#    ax2.annotate(label, xy=(x, y), xytext=(-20, 0), textcoords="offset points", fontsize=8)
    

shape.plot(color=shape['color'], linewidth=1, ax=ax1, edgecolor='0.8', legend=True, categorical=True)
#islas_canarias.plot(ax=ax1)

ax1.set_axis_off()

islas_canarias.plot(color=islas_canarias['color'], linewidth=1, ax=ax2, edgecolor='0.8')  # Example code to plot a second map
ax2.set_axis_off()

# Adjust the size of the second map
ax1.set_position([0.1, 0.3, 0.8, 0.6])
ax2.set_position([0.08, 0.05, 0.2, 0.2])


plt.show()

plt.savefig("output.jpg")


#islas_canarias.to_excel(r"C:\\Users\\Andrew\\Desktop\\Generales23\\total.xlsx", index=False)
