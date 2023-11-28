import sqlite3
import pandas as pd
import numpy as np

def crear_bd():
    conexion = sqlite3.connect('bd.db')

    with open('script.sql') as f:
        script = f.read()
        
    conexion.executescript(script)
    conexion.close()

def insert(columns : list, values : list, table : str) -> None:
    if len(columns) == 0 or len(values) == 0 or len(columns) != len(values) or table.replace(' ', '') == '':
        return
    
    conexion = sqlite3.connect('bd.db')
    cursor = conexion.cursor()
    
    #Create the TABLE_NAME (COLUMNS) instruction
    c_script = "("
    questions = "("
    
    for i in range(len(columns) - 1):
        c_script += f'{columns[i]}, '
        questions += '?, '
    c_script += f'{columns[-1]})'
    questions += '?)'
    
    cursor.execute(f"INSERT INTO {table} {c_script} VALUES {questions}", tuple(values))
    conexion.commit()
    conexion.close()

def delete(column : str, key : str, table : str) -> None:
    if table.replace(' ', '') == '' or column.replace(' ', '') == '' or key.replace(' ', '') == '':
        return
    
    conexion = sqlite3.connect('bd.db')
    cursor = conexion.cursor()
    try:
        numeric_key = int(key)
        cursor.execute(f"DELETE FROM {table} WHERE {column} = {numeric_key}")
    except:
        cursor.execute(f'DELETE FROM {table} WHERE {column} LIKE "{key}"')
    
    conexion.commit()
    conexion.close()

def vehiculos_csv(df : pd.DataFrame) -> None:
    df = df.drop_duplicates(['AÑO','BF GLOBAL   MODEL'])
    df_aynos = df[['MARCA','MODELO','AÑO','CARROCERÍA']]
    df_aynos['MODELO'] = df_aynos['MODELO'].astype(str)
    df_aynos['AÑO'] = df_aynos['AÑO'].astype(str)
    df_aynos.sort_values(['MARCA','MODELO','AÑO'])
    
    models_df = df_aynos['MODELO'].to_list()
    aynos = df_aynos['AÑO'].to_list()
    carroceria = df_aynos['CARROCERÍA'].to_list()
    
    modelos_a = []
    
    str_modelos = models_df[0]
    index = 1
    for model in models_df:
        if model != str_modelos:
            index += 1
            str_modelos = model
        modelos_a.append(index)

    print(f"{len(aynos)} : ay")
    print(f"{len(modelos_a)} : md")
    print()
    
    aynos = pd.DataFrame({
            'Id_aynos': [x for x in range(1, len(modelos_a) + 1)],
            'Id_modelo': modelos_a,
            'Ayno': aynos,
            'Tipo_carroceria' : carroceria
    })
    
    df_modelos = df_aynos[['MARCA','MODELO']].drop_duplicates(subset = ['MARCA','MODELO'])
    
    modelos_mo = df_modelos['MODELO'].to_list()
    marcas_df = df_modelos['MARCA'].to_list()
    marcas_mo = []
    
    str_marca = marcas_df[0]
    index = 1
    for marca in marcas_df:
        if marca != str_marca:
            index += 1
            str_marca = marca
        marcas_mo.append(index)
    
    print(f"{len(marcas_mo)} : ma")
    print(f"{len(modelos_mo)} : md")
    print()
    
    modelos = pd.DataFrame({
            'Id_modelo':[x for x in range(1, len(modelos_mo) + 1)],
            'Id_marca_auto': marcas_mo,
            'Nombre': modelos_mo
    })
    
    df_marcas = df_modelos['MARCA'].drop_duplicates()
    descs = df_marcas.to_list()
    
    print(f"{len(descs)} : ma")
    print()
    
    marcas = pd.DataFrame({
            'Id_marca_auto': [x for x in range(1, len(descs) + 1)],
            'Descripcion': descs}
    )
    
    marcas.to_csv('datos/Marcas_autos.csv', index = None)
    modelos.to_csv('datos/Modelos.csv', index = None)
    aynos.to_csv('datos/Aynos.csv', index = None)
    
def medidas_csv(df : pd.DataFrame) -> None:
    df_medidas = df['IDENTIFICACIÓN BASICA'].drop_duplicates()
    meds = []
    for medida in df_medidas.to_list():
        if len(medida) > 9: #hay dos medidas
            meds.append(medida[0:9])
            meds.append(medida[12:21])
        else: meds.append(medida)
    meds.sort()
    medida = pd.DataFrame({
        'Id_medida' : [x for x in range(1, len(meds) + 1)],
        'Identificacion': meds
    })
    medida = medida.drop_duplicates(subset = 'Identificacion')
    medidas = pd.DataFrame({
        'Id_medida' : [x + 1 for x in range(medida.shape[0])],
        'Identificacion': medida['Identificacion'].to_list()
    })
    medidas.to_csv('datos/Medidas.csv', index = None)
    
def llantas_csv(df : pd.DataFrame,) -> None:    
    def participa(variedad : int) -> bool:
        num = np.random.randint(137*variedad, 1000)
        return num > 700
    
    def precio_random(diametro : int, ancho_neum : int, durabilidad : int, economicidad : int) -> int:
        precio_estandar = int(10000 * ((0.607* float(diametro) - 74.9) + (39/8 * float(ancho_neum) - 57.6)))
        if durabilidad == economicidad:
            return precio_estandar
        
        return precio_estandar - precio_estandar//((durabilidad - economicidad) * 8) #descuento
    
    df_propiedades = pd.read_excel('datos/Llantas_propiedades.xlsx')
    
    medidas = df['Identificacion'].to_list()
    marcas = []
    precios = []
    durabilidades = []
    id_medidas = []
    
    for j, medida in enumerate(medidas[:292]):
        for i in range(df_propiedades.shape[0]): #20 filas
            llanta = df_propiedades.iloc[i].to_list()
            if participa(int(llanta[2])): #variedad
                precio = precio_random(medida[0:3], medida[7:9], llanta[5], llanta[1])
                durabilidades.append(int(llanta[5]))
                marcas.append(llanta[0])
                id_medidas.append(j + 1)
                precios.append(precio)
                
    
    llantas = pd.DataFrame({
            'Id_llanta' : [x for x in range(1, len(marcas) + 1)],
            'Id_medida' : id_medidas,
            'Marca' : marcas,
            'Precio' : precios,
            'Durabilidad' : durabilidades
    })
    
    llantas.to_csv('datos/Llantas_v.csv', index = None)

def marcas_llantas_csv() -> None:
    df_propiedades = pd.read_excel('datos/Llantas_propiedades.xlsx')
    df_ll = pd.read_csv('datos/Llantas_v.csv')
    marcas_dict = dict()
    for i, marca in enumerate(df_propiedades['Marca'].to_list()):
        marcas_dict[marca] = i + 1
    llantas = df_ll[['Id_llanta','Id_medida','Marca','Precio']]
    llantas.rename(columns = {'Marca':'Id_marca_llanta'}, inplace = True)
    llantas['Id_marca_llanta'] = [marcas_dict[marca] for marca in llantas['Id_marca_llanta'].to_list()]
    
    llantas.to_csv('datos/Llantas.csv', index = None)
    
    marcas = pd.DataFrame({
            'Id_marca_llanta' : list(marcas_dict.values()),
            'Descripcion': list(marcas_dict.keys()),
            'Durabilidad': df_propiedades['Durabilidad'].to_list()
    })
    
    marcas.to_csv('datos/Marcas_llantas.csv', index = None)

def medidas_aynos_csv(df : pd.DataFrame) -> None:
    df_meds = pd.read_csv('datos/Medidas.csv')
    df_marc = pd.read_csv('datos/Marcas_autos.csv')
    df_aynos = pd.read_csv('datos/Aynos.csv')
    df_mods = pd.read_csv('datos/Modelos.csv')
    df = df.drop_duplicates(subset = ['BF GLOBAL   MODEL', 'AÑO'])
    df_ma = df[['IDENTIFICACIÓN BASICA', 'MODELO', 'AÑO', 'LOCALIZACIÓN','LOCALIZACIÓN Serie II', 'MARCA']]
    
    print(df.shape[0])
    
    modelos_dict = dict()
    aynos_dict = dict()
    medidas_dict = dict()
    marcas_dict = dict()
    
    for i, medida in enumerate(df_meds['Identificacion'].to_list()):
        medidas_dict[medida] = i + 1
        
    for i, marca in enumerate(df_marc['Descripcion'].to_list()):
        marcas_dict[marca] = i + 1

    for i, mod in enumerate(zip(df_mods['Nombre'].to_list(), df_mods['Id_marca_auto'].to_list())):
        modelos_dict[str(mod[0]) + str(mod[1])] = i + 1
    
    for i, aymo in enumerate(zip(df_aynos['Ayno'].to_list(), df_aynos['Id_modelo'].to_list())):
        aynos_dict[str(aymo[0]) + str(aymo[1])] = i + 1
        if  str(aymo[1]) == str(331):
            print(str(aymo[0]) + str(aymo[1]))
    
    id_aynm = []
    id_ayno = []
    id_medida = []
    localizacion = []
    
    j = 1
    for i in range(df_ma.shape[0]):
        fila = df_ma.iloc[i].to_list() #0 Medida, 1 modelo, 2 año, 3 loc (delantera;trasera), 4 loc opcional, 5 marca
        id_aynm.append(j)
        if len(fila[0]) > 9: #hay dos medidas
            try:
                id_ayno.append(aynos_dict[str(fila[2]) + str(modelos_dict[str(fila[1]) + str(marcas_dict[str(fila[5])])])])
                id_medida.append(medidas_dict[fila[0][0:9]])
                localizacion.append('D')
            except:
                j -= 1
                id_aynm.pop()
                continue
            j += 1
            id_aynm.append(j)
            id_ayno.append(aynos_dict[str(fila[2]) + str(modelos_dict[str(fila[1]) + str(marcas_dict[str(fila[5])])])])
            id_medida.append(medidas_dict[fila[0][12:21]])
            localizacion.append('T')
        else: #medida unica
            try:
                id_ayno.append(aynos_dict[str(fila[2]) + str(modelos_dict[str(fila[1]) + str(marcas_dict[str(fila[5])])])])
                id_medida.append(medidas_dict[fila[0]])
                localizacion.append('A')
            except:
                print(i)
                raise Exception()
                j -= 1
                id_aynm.pop()
        j += 1
        
        medidas_aynos = pd.DataFrame({
            'Id_aynm' : id_aynm,
            'Id_ayno' : id_ayno,
            'Id_medida' : id_medida,
            'Localizacion' : localizacion
        })
        
        medidas_aynos.to_csv('Datos/Medidas_aynos.csv', index = None)
    
crear_bd()
#df = pd.read_excel('datos/Base-vehículos-meno.xlsx')
#vehiculos_csv(df)
#medidas_csv(df)
#df_m = pd.read_csv('datos/Medidas.csv')
#llantas_csv(df_m)
#marcas_llantas_csv()
#medidas_aynos_csv(df)