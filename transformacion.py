import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import wbgapi as wb


def transformacion():
    paises = ['ATG','ARG','BRB','BLZ','BOL','BRA','CAN','CHL','COL','CRI','CUB','DMA','DOM','ECU','SLV','GRD','GTM','GUY','HTI','HND','JAM','MEX','NIC','PAN','PRY','PER','KNA','LCA','VCT','SUR','BHS','TTO','USA','URY','VEN']

    #
    #
    #
    #tbl_paises
    tbl_paises = pd.read_csv('Extraccion/tbl_paises.csv')
    #Datos ya están completos
    tbl_paises.to_csv('Limpiados/tbl_paises.csv', index = False)

    #
    #
    #
    #tbl_esperanza_vida
    tbl_esperanza_vida = pd.read_csv('Extraccion/tbl_esperanza_vida.csv')
    #Datos ya están completos

    tbl_esperanza_vida = tbl_esperanza_vida[(tbl_esperanza_vida["year"] >= 2000) & (tbl_esperanza_vida["year"] <= 2020)]

    tbl_esperanza_vida.to_csv("Limpiados/tbl_esperanza_vida.csv", index = False)


    #
    #
    #
    #tbl_poblacion
    tbl_poblacion = pd.read_csv('Extraccion/tbl_poblacion.csv')
    #Datos ya están completos
    tbl_poblacion.to_csv('Limpiados/tbl_poblacion.csv', index = False)  

    #
    #
    #
    #tbl_anios_medio_escolaridad
    tbl_anios_medio_escolaridad = pd.read_csv('Extraccion/tbl_anios_medios_escolaridad.csv')
    #Datos ya están completos
    tbl_anios_medio_escolaridad.to_csv('Limpiados/tbl_anios_medios_escolaridad.csv', index = False)   

    #
    #
    #
    #tbl_acceso_electricidad
    tbl_acceso_electricidad = pd.read_csv('Extraccion/tbl_acceso_electricidad.csv')
    #Datos ya están completos
    tbl_acceso_electricidad.to_csv('Limpiados/tbl_acceso_electricidad.csv', index = False)

    #
    #
    #
    #tbl_densidad_poblacion
    tbl_densidad_poblacional = pd.read_csv('Extraccion/tbl_densidad_poblacional.csv')
    #Datos ya están completos
    tbl_densidad_poblacional.to_csv('Limpiados/tbl_densidad_poblacional.csv', index = False)

    #
    #
    #
    #tbl_produccion_alimentos
    tbl_produccion_alimentos = pd.read_csv('Extraccion/tbl_produccion_alimentos.csv')
    #Datos ya están completos
    tbl_produccion_alimentos.to_csv('Limpiados/tbl_produccion_alimentos.csv', index = False)


    #
    #
    #
    #tbl_consumo_tabaco
    tbl_consumo_tabaco = pd.read_csv('Extraccion/tbl_consumo_tabaco.csv')
    # Todos los paises tienen datos nulos. Vamos a interpolar en ambas direcciones
    for i in paises:
        temp = tbl_consumo_tabaco[tbl_consumo_tabaco['id_pais'] == i]
        temp = temp.interpolate(method="linear",limit_direction="both")
        tbl_consumo_tabaco[tbl_consumo_tabaco['id_pais'] == i] = temp
    #Completamos los datos de las pequeñas islas del caribe con barbados
    años=range(2000,2021)
    pais_caribe=["ATG", "DMA", "GRD", "KNA", "LCA", "VCT"]
    for e in pais_caribe:
        for i in años:
            mask1 = (tbl_consumo_tabaco["id_pais"] == e) & (tbl_consumo_tabaco["year"] == i)
            mask2 = (tbl_consumo_tabaco["id_pais"] == "BRB") & (tbl_consumo_tabaco["year"] == i)
            tbl_consumo_tabaco.loc[mask1, "tabaco"] = round((tbl_consumo_tabaco.loc[mask2, "tabaco"].values[0]),2)
    #Completamos los datos de centro america con guatemala
    años=range(2000,2021)
    pais_caribe=["HND", "NIC"]
    for e in pais_caribe:
        for i in años:
            mask1 = (tbl_consumo_tabaco["id_pais"] == e) & (tbl_consumo_tabaco["year"] == i)
            mask2 = (tbl_consumo_tabaco["id_pais"] == "GTM") & (tbl_consumo_tabaco["year"] == i)
            tbl_consumo_tabaco.loc[mask1, "tabaco"] = round((tbl_consumo_tabaco.loc[mask2, "tabaco"].values[0]),2)
    #Completamos los datos de la costa norte de Sudamerica con colombia
    años=range(2000,2021)
    pais_caribe=["SUR", "TTO","VEN"]
    for e in pais_caribe:
        for i in años:
            mask1 = (tbl_consumo_tabaco["id_pais"] == e) & (tbl_consumo_tabaco["year"] == i)
            mask2 = (tbl_consumo_tabaco["id_pais"] == "COL") & (tbl_consumo_tabaco["year"] == i)
            tbl_consumo_tabaco.loc[mask1, "tabaco"] = round((tbl_consumo_tabaco.loc[mask2, "tabaco"].values[0]),2)
    tbl_consumo_tabaco.to_csv('Limpiados/tbl_consumo_tabaco.csv', index = False)

    #
    #
    #
    #tbl_contaminacion_aire
    tbl_contaminacion_aire = pd.read_csv('Extraccion/tbl_contaminacion_aire.csv')
    #Todos los paises tienen datos nulos. Vamos a interpolar en ambas direcciones
    for i in paises:
        temp = tbl_contaminacion_aire[tbl_contaminacion_aire['id_pais'] == i]
        temp = temp.interpolate(method="linear",limit_direction="backward")
        tbl_contaminacion_aire[tbl_contaminacion_aire['id_pais'] == i] = temp
    años=range(2000,2021)
    for i in años:
        mask1 = (tbl_contaminacion_aire["id_pais"] == "KNA") & (tbl_contaminacion_aire["year"] == i)
        mask2 = (tbl_contaminacion_aire["id_pais"] == "ATG") & (tbl_contaminacion_aire["year"] == i)
        tbl_contaminacion_aire.loc[mask1, " contaminacion_aire"] = tbl_contaminacion_aire.loc[mask2, " contaminacion_aire"].values[0]
    tbl_contaminacion_aire.to_csv('Limpiados/tbl_contaminacion_aire.csv', index = False)

    #
    #
    #
    #tbl_acceso_agua_potable
    """
    Para este dataset faltan datos en los mismos años para todos los países.
    Se observa que la variable sigue una tendencia lineal a través del tiempo.
    Se procederá a hacer una interpolación y luego los valores faltantes se llenarán con un bfill
    """
    agua = pd.read_csv('Extraccion/tbl_acceso_agua_potable.csv')

    for pais in paises:
        temp = agua[agua['id_pais']==pais]
        temp = temp.interpolate()
        agua[agua['id_pais']==pais] = temp

    for pais in paises:
        temp = agua[agua['id_pais']==pais]
        temp = temp.fillna(method = 'bfill')
        agua[agua['id_pais']==pais] = temp

    agua.to_csv('Limpiados/tbl_acceso_agua_potable.csv', index = False)

    
    #tbl_agotamiento_recursos_naturales
    """
    En este dataset hay 3 países que no tienen datos. A partir del 2015 VEN deja de presentar datos
    y en el 2019 CUB deja de presentar datos.
    """

    #
    #
    #
    #tbl_alfabetizacion_porc
    tbl_alfabetizacion_porc = pd.read_csv('Extraccion/tbl_alfabetizacion_porc.csv')
    # ['CAN', 'DMA', 'KNA', 'LCA', 'VCT', 'BHS', 'USA'] paises que tienen todos sus datos nulos
    paises_nulos=[]
    for i in paises:
        mask = tbl_alfabetizacion_porc["id_pais"] == i
        df_filtrada = tbl_alfabetizacion_porc[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)
    """
    Imputaremos un valor para cada uno de ellos, para luego predecir el resto de la tabla<br>
    Fuente: https://worldpopulationreview.com/country-rankings/literacy-rate-by-country<br>

    CAN = Canada, Año 2003, Ind. Alfabetizacion: 99.00% <br>
    DMA = Dominica, Año 2003, Ind. Alfabetizacion: 94.00%<br>
    KNA = Saint Kitts and Nevis, Año 2003, Ind. Alfabetizacion: 97.80%<br>
    LCA = Santa Lucia, Año 2003, Ind. Alfabetizacion: 90.10%<br>
    VCT = Saint Vincent and the Grenadines, Año: 2003, Ind. Alfabetizacion: 93.00%<br>
    BHS = Bahamas, Año: 2003, Ind. Alfabetizacion: 95.60%<br>
    USA = Estados Unidos, Año: 2003, Ind. Alfabetizacion: 99.00%
    """
    imp=[99.00, 94.00, 97.80, 90.10, 93.00, 95.60, 99.00]
    df_carga=pd.DataFrame(list(zip(paises_nulos, imp)), columns= ["Pais","IND"])

    #Cargamos los valores en cada celda correspondiente al pais y año
    for i in paises_nulos:
        mask1 = (tbl_alfabetizacion_porc["id_pais"] == i) & (tbl_alfabetizacion_porc["year"] == 2003)
        mask2 = df_carga["Pais"] == i
        tbl_alfabetizacion_porc.loc[mask1, "alfabetizacion"] = df_carga["IND"].loc[mask2].values[0]

    #Se aplicará interpolacion para llenar los datos faltantes por país:
    for i in paises:
        temp = tbl_alfabetizacion_porc[tbl_alfabetizacion_porc['id_pais'] == i]
        temp = temp.interpolate()
        tbl_alfabetizacion_porc[tbl_alfabetizacion_porc['id_pais'] == i] = temp

    #Solo hay datos faltantes para los ultimos años, aplicaremos nuevamente interpolacion pero con direccion de atras hacia adelante
    # para que llene los valores faltantes
    for i in paises:
        temp = tbl_alfabetizacion_porc[tbl_alfabetizacion_porc['id_pais'] == i]
        temp = temp.interpolate(method="linear",limit_direction="backward")
        tbl_alfabetizacion_porc[tbl_alfabetizacion_porc['id_pais'] == i] = temp
    tbl_alfabetizacion_porc.to_csv('Limpiados/tbl_alfabetizacion_porc.csv', index = False)

    #
    #
    #
    # tbl_srv_sanit_bas
    """
    VEN, ARG: Hay valores faltantes en inicio de período, los valores van en crecimiento
    se aplicará interpolación o bfill

    BHS: Solo hay un valor faltante. Se aplicará bfill, ya que se ve que los valores
    de los años cercanos son iguales

    VCT, KNA, GRD, DMA, ATG: Caso similar a BHS. Se aplicará bfill
    """
    tbl_srv_sanit_bas = pd.read_csv('Extraccion/tbl_srv_sanit_bas.csv')
    for pais in paises:
        temp = tbl_srv_sanit_bas[tbl_srv_sanit_bas['id_pais']==pais]
        if pais == 'VEN':
            temp = temp.interpolate()
            tbl_srv_sanit_bas[tbl_srv_sanit_bas['id_pais']==pais] = temp
        else:
            temp = tbl_srv_sanit_bas[tbl_srv_sanit_bas['id_pais']==pais]
            temp = temp.fillna(method = 'bfill')
            tbl_srv_sanit_bas[tbl_srv_sanit_bas['id_pais']==pais] = temp
    tbl_srv_sanit_bas.to_csv('Limpiados/tbl_srv_sanit_bas.csv', index = False)

    #
    #
    #
    #tbl_emisiones_co2
    # Falta solo el valor de un año. Se predice el valor por regresion lineal
    co2 = pd.read_csv('Extraccion/tbl_emisiones_co2.csv')
    for pais in paises:
        lr = LinearRegression()
        temp = co2[co2['id_pais']==pais]
        temp_na = temp[temp['emisiones_co2'].isna()]
        temp_x_train = temp.dropna()
        temp_x_train = temp_x_train['year']
        temp_y_train = temp.dropna()
        temp_y_train = temp_y_train['emisiones_co2']
        lr.fit(pd.DataFrame(temp_x_train),temp_y_train)
        pred = float(lr.predict(pd.DataFrame(temp_na['year'])))
        temp = temp.fillna(pred)
        co2[co2['id_pais']==pais] = temp
    co2.to_csv('Limpiados/tbl_emisiones_co2.csv', index = False)

    #
    #
    #
    #tbl_fuerza_laboral
    tbl_fuerza_laboral = pd.read_csv('Extraccion/tbl_fuerza_laboral.csv')
    #CONTAMOS VALORES NULOS
    """
    tbl_fuerza_laboral.isnull().sum() 
    HaY 84 datos faltantes, algunos paises tienen todos sus datos faltantes<br>
    Vamos a identificarlos
    """
    paises_nulos=[]
    for i in paises:
        mask = tbl_fuerza_laboral["id_pais"] == i
        df_filtrada = tbl_fuerza_laboral[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)
    """
    LOS 84 DATOS FALTANTES CORRESPONDEN A CUATROS PAISES:<br>
    ATG, DMA, GRD, KNA<br>
    VAMOS A LLENARLOS POR MEDIO DE COMPARACION CON PAISES SIMILARES<br>
    ADEMAS, VAMOS A USAR LA TABLA DE POBLACION

    ATG, DMA, GRD y KNA son paises muy similares entre si. <br>
    Paises pequeños del caribe, con poca poblacion. Sus PIB son similares y estan ranqueados entre los últimos paises por su volumen de PIB.<br>
    El indice de desarrollo humano los hubica en las posiciones, 78, 79, 74 y 75, respectivamente.<br>
    Usaremos a LCA como referencia para completar los valores faltantes<br>

    FUENTE: https://datosmacro.expansion.com/
    """
    wb.db= 2
    pob = wb.data.DataFrame('SP.POP.TOTL', ["ATG","DMA","GRD","KNA","LCA"], time=range(2000, 2021), labels=True, columns="economy").reset_index()
    pob.drop(["time"], axis=1, inplace=True)

    """CALCULAREMOS QUE PORCENTAJE DE LA POBLACION DE "LCA" CORRESPONDE A LA FUERZA LABORAL DEL PAIS 
    Y USAREMOS ESTE DATO PARA COMPLETAR LA DEL RESTO DE LOS PAISES"""
    #Creamos un data frame con la Fuerza Laboral de LCA
    df1=(tbl_fuerza_laboral[tbl_fuerza_laboral["id_pais"] == "LCA"]).reset_index()
    #Creamos otro DataFrame que divida la fuerza laboral de LCA por su poblacion
    df2 = round((df1[' fuerza_laboral'] / pob["LCA"]),2)

    for i in paises_nulos:
        df_prov=pob[i]*df2
        year=2020
        for e in range(0, len(df_prov)):
            mask1= (tbl_fuerza_laboral["id_pais"] == i) & (tbl_fuerza_laboral["year"] == year)
            tbl_fuerza_laboral.loc[mask1, ' fuerza_laboral'] = df_prov.values[e]
            year= int(year)
            year = year-1
    tbl_fuerza_laboral.to_csv('Limpiados/tbl_fuerza_laboral.csv', index = False)

    #
    #
    #
    #tbl_desempleo_fl
    tbl_desempleo_fl = pd.read_csv('Extraccion/tbl_desempleo_fl.csv')
    #Vemos que paises tienen TODOS sus datos faltantes
    paises_nulos=[]
    for i in paises:
        mask = tbl_desempleo_fl["id_pais"] == i
        df_filtrada = tbl_desempleo_fl[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)
    tbl_desempleo_fl[tbl_desempleo_fl["id_pais"] == "LCA"]
    #creamos un dataframe con los valores a cargar en el año 2020
    imp=[11.00, 23.00, 24.00, 4.50]
    df_carga=pd.DataFrame(list(zip(paises_nulos, imp)), columns= ["id_pais","desempleo"])
    df_carga
    #Cargamos los valores en cada celda correspondiente al pais y año
    for i in paises_nulos:
        mask1 = (tbl_desempleo_fl["id_pais"] == i) & (tbl_desempleo_fl["year"] == 2020)
        mask2 = df_carga["id_pais"] == i
        tbl_desempleo_fl.loc[mask1, "desempleo"] = df_carga["desempleo"].loc[mask2].values[0]
        #print (tbl_desempleo_fl[mask1])
    #Creamos un dataframe con la tasa de desempleo de LCA
    df1=tbl_desempleo_fl[tbl_desempleo_fl["id_pais"] == "LCA"].reset_index()
    df1.drop(["index","id_pais","year"], axis=1, inplace=True)
    #Creamos una lista que indique la variacion inter anual comenzando con el año 2020 para LCA para abajo
    var_anual=[]
    for i in range (1, len(df1)):
        val_ant=df1.loc[i-1,"desempleo"]
        val_act=df1.loc[i,"desempleo"]
        var_anual.append(round((val_act/val_ant),2))

    for i in paises_nulos:
        year_act=2019
        year_prev=2020
        for e in var_anual:
            mask1= (tbl_desempleo_fl["id_pais"] == i) & (tbl_desempleo_fl["year"] == year_act)
            mask2= (tbl_desempleo_fl["id_pais"] == i) & (tbl_desempleo_fl["year"] == year_prev)
            val=tbl_desempleo_fl["desempleo"].loc[mask2].values[0] * e
            tbl_desempleo_fl.loc[mask1, "desempleo"] = round(val, 3)
            year_act= int(year_act)
            year_act = year_act-1
            year_prev= int(year_prev)
            year_prev = year_prev-1

    tbl_desempleo_fl[tbl_desempleo_fl["id_pais"] == "ATG"]

    tbl_desempleo_fl[tbl_desempleo_fl["id_pais"] == "DMA"]
    
    tbl_desempleo_fl.to_csv('Limpiados/tbl_desempleo_fl.csv', index = False)
    
    #
    #
    #
    #tbl_consumo_alcohol_pc
    # Importación
    alcohol= pd.read_csv('Extraccion/tbl_consumo_alcohol_pc.csv',
                        sep =';',
                        usecols = ['YEAR (code)','COUNTRY (code)','ALCOHOLTYPE (code)','SA_0000001400 (numeric)'],
                        encoding ='latin-1',
                        )
    # Renombrar
    alcohol = alcohol.rename({'YEAR (code)'             : 'Year',
                            'COUNTRY (code)'          : 'Country',
                            'ALCOHOLTYPE (code)'      : 'Types' ,
                            'SA_0000001400 (numeric)' : 'Alcohol_pc'
                            }, axis=1)

    alcohol = alcohol.drop(alcohol[(alcohol['Types']=='SA_TOTAL')==False].index).drop(['Types'],axis=1)
    alcohol = alcohol.pivot(index='Year', columns='Country', values='Alcohol_pc')

    # filtro paises
    for p in alcohol.columns:
        if ( p in paises ) == False :
            alcohol = alcohol.drop(p,axis=1)                   
        continue
    alcohol = alcohol.reset_index()  
    # Valores nulos reemplazados con media
    alcohol = alcohol.apply(lambda x: x.fillna(x.mean()),axis=0)    

    # NOTA: SOLO 'CAN' PRESENTABA 5 VALORES NULO (20=0-2005)

    # --- TRATAMIENTO DE VALORES NULOS MEDIANTE FORECAST (MEDIA MOVIL) ----
    # años a proyectar (filas)
    forecast= 1
    for i in range(forecast):
        alcohol.loc[len(alcohol)+i]=[np.nan]*(len(alcohol.columns))
        #obesidad['Year'].loc[len(obesidad)-1]==obesidad.iloc[len(obesidad)-1][0]+1

    # Nuevas variables (columnas)
    for e in alcohol.columns.drop('Year'):
        alcohol1= alcohol[e].to_frame()
        alcohol1['Year'] = alcohol['Year']
        alcohol[e] = alcohol1[e].rolling(3).mean().shift(forecast)

    # Tabla resultado
    alcohol = alcohol.drop(range(0,10),axis=0).reset_index( drop=True)
    alcohol['Year']=list(range(2000,2021))
    alcohol = pd.melt(alcohol, id_vars='Year', value_vars= alcohol.columns[1:],value_name='Alcohol_pc')
    alcohol.to_csv('Limpiados/tbl_consumo_alcohol_pc.csv', index = False)

    #
    #
    #
    #tbl_obesidad
    # Importación
    obesidad= pd.read_csv('Extraccion/tbl_obesidad.csv',
                        sep =';',
                        usecols = ['YEAR (code)','COUNTRY (code)','SEX (code)','NCD_BMI_30A (numeric)'],
                        encoding ='latin-1',
                        )
    # Renombrar
    obesidad = obesidad.rename({'YEAR (code)'             : 'Year',
                            'COUNTRY (code)'          : 'Country',
                            'SEX (code)'              : 'Both' ,
                            'NCD_BMI_30A (numeric)'   : 'Indice_mc' # Indice de masa corporal
                            }, axis=1)
    obesidad = obesidad.drop(obesidad[(obesidad['Both']=='BTSX')==False].index).drop(['Both'],axis=1)
    obesidad = obesidad.pivot(index='Year', columns='Country', values='Indice_mc')

    # filtro de paises
    for p in obesidad.columns:
        if ( p in paises ) == False :
            obesidad = obesidad.drop(p,axis=1)                   
        continue
    obesidad = obesidad.reset_index()  

    # --- TRATAMIENTO DE VALORES NULOS MEDIANTE FORECAST (MEDIA MOVIL) ----
    # años a proyectar (filas)
    forecast= 4
    for i in range(forecast):
        obesidad.loc[len(obesidad)+i]=[np.nan]*(len(obesidad.columns))
        #obesidad['Year'].loc[len(obesidad)-1]==obesidad.iloc[len(obesidad)-1][0]+1

    # Nuevas variables (columnas)
    for e in obesidad.columns.drop('Year'):
        obesidad1= obesidad[e].to_frame()
        obesidad1['Year'] = obesidad['Year']
        obesidad[e] = obesidad1[e].rolling(3).mean().shift(forecast)

    # Tabla resultado
    obesidad = obesidad.drop(range(0,25),axis=0).reset_index( drop=True)
    obesidad['Year']=list(range(2000,2021))
    obesidad = pd.melt(obesidad, id_vars='Year', value_vars= obesidad.columns[1:],value_name='Indice_mc')
    obesidad.columns = ['year','id_pais','obesidad']
    obesidad.to_csv('Limpiados/tbl_obesidad.csv', index = False)

    #
    #
    #
    #tbl_ingreso_medio_pc
    tbl_ingreso_medio_pc = pd.read_csv('Extraccion/tbl_ingreso_medio_pc.csv')
    #tbl_ingreso_medio_pc
    #tbl_ingreso_medio_pc.info()
    #CONTAMOS VALORES NULOS
    #tbl_ingreso_medio_pc.isnull().sum()
    #Hay 8 valores faltantes
    
    #Vemos que paises tienen datos faltantes
    #print("Paises con datos nulos")
    paises_nulos=[]
    for i in paises:
        mask = tbl_ingreso_medio_pc["id_pais"] == i
        df_filtrada = tbl_ingreso_medio_pc[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a > 0:
            paises_nulos.append(i)
    #print(paises_nulos)
    tbl_ingreso_medio_pc[tbl_ingreso_medio_pc["id_pais"] == "CUB"]
    tbl_ingreso_medio_pc[tbl_ingreso_medio_pc["id_pais"] == "VEN"]

    #interpolaremos los datos faltantes
    #Sola hay datos faltantes para los ultimos años, aplicaremos interpolacion lineal con direccion de atras hacia adelante
    # para que llene los valores faltantes
    for i in paises:
        temp = tbl_ingreso_medio_pc[tbl_ingreso_medio_pc['id_pais'] == i]
        temp = temp.interpolate(method="linear",limit_direction="backward")
        tbl_ingreso_medio_pc[tbl_ingreso_medio_pc['id_pais'] == i] = temp
    
    tbl_ingreso_medio_pc[tbl_ingreso_medio_pc["id_pais"] == "CUB"]
    tbl_ingreso_medio_pc[tbl_ingreso_medio_pc["id_pais"] == "VEN"]
    tbl_ingreso_medio_pc.to_csv('Limpiados/tbl_ingreso_medio_pc.csv', index = False)
    ####



    #tbl_inversion_educacion
    #CREACION DE DATAFRAME
    tbl_inversion_educacion = pd.read_csv('Extraccion/tbl_inversion_educacion.csv')
    #tbl_inversion_educacion.info()
    #CONTAMOS VALORES NULOS
    #tbl_inversion_educacion.isnull().sum()
    #Hay 267 valores faltantes, vamos a identificarlos
    #Vemos que paises tienen TODOS sus datos faltantes
    #print("Paises con TODOS datos nulos")
    paises_nulos=[]
    for i in paises:
        mask = tbl_inversion_educacion["id_pais"] == i
        df_filtrada = tbl_inversion_educacion[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)
    #print(paises_nulos)
    #Vemos que paises tienen datos faltantes
    #print("Paises con datos nulos")
    paises_nulos=[]
    for i in paises:
        mask = tbl_inversion_educacion["id_pais"] == i
        df_filtrada = tbl_inversion_educacion[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a > 0:
            paises_nulos.append(i)

    #Interpolaremos los datos faltantes
    #Todos los paises tienen datos nulos. Vamos a interpolar en ambas direcciones
    for i in paises:
        temp = tbl_inversion_educacion[tbl_inversion_educacion['id_pais'] == i]
        temp = temp.interpolate(method="linear",limit_direction="both")
        tbl_inversion_educacion[tbl_inversion_educacion['id_pais'] == i] = temp
    #CORROBORAMOS VALORES NULOS
    #tbl_inversion_educacion.isnull().sum()
    #vemos el resultado final
    #for i in paises:
    #    print(tbl_inversion_educacion[tbl_inversion_educacion["id_pais"] == i])
    #tbl_inversion_educacion
    #tbl_inversion_educacion.columns=["id_pais", "year","educacion"]
    tbl_inversion_educacion.to_csv('Limpiados/tbl_inversion_educacion.csv', index = False)

    ##############################

    ## LIMPIEZA tbl_pib

    tbl_pib = pd.read_csv("Extraccion/tbl_pib.csv")
    # Contamos los valores nulos:
    """
    tbl_pib.isnull().sum()
    Aqui vemos 6 valores nulos
    """
    
    """
    Vemos que paises tienen TODOS sus datos faltantes
    Paises con TODOS datos nulos
    """
    paises_nulos=[]
    for i in paises:
        mask = tbl_pib["id_pais"] == i
        df_filtrada = tbl_pib[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)
    
    """
    No hay paises con TODOS los datos nulos, procedemos.
    vemos como se distribuyen los datos nulos
    """

    for i in paises_nulos:
        print(tbl_pib[tbl_pib["id_pais"] == i])

    #Vamos a interpolar hacia arriba
    for i in paises:
        temp = tbl_pib[tbl_pib['id_pais'] == i]
        temp = temp.interpolate(method="linear",limit_direction="backward")
        tbl_pib[tbl_pib['id_pais'] == i] = temp
    #CORROBORAMOS VALORES NULOS
    tbl_pib.isnull().sum()
    tbl_pib.to_csv('Limpiados/tbl_pib.csv', index = False)


    ### LIMPIEZA tbl_valor_industria

    tbl_valor_industria = pd.read_csv("Extraccion/tbl_valor_industria.csv")

    """
    CONTAMOS VALORES NULOS
    tbl_valor_industria.isnull().sum()
    son 14 valores faltantes
    """

    """
    Vemos que paises tienen TODOS sus datos faltantes

    print("Paises con TODOS datos nulos")
    paises_nulos=[]
    for i in paises:
        mask = tbl_valor_industria["id_pais"] == i
        df_filtrada = tbl_valor_industria[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)
    print(paises_nulos)
    Ningun país tiene valores faltantes
    """

    #Vamos a interpolar en ambas direcciones
    for i in paises:
        temp = tbl_valor_industria[tbl_valor_industria['id_pais'] == i]
        temp = temp.interpolate(method="linear",limit_direction="both")
        tbl_valor_industria[tbl_valor_industria['id_pais'] == i] = temp
    
    """
    CORROBORAMOS VALORES NULOS
    tbl_valor_industria.isnull().sum()
    Ahora no existen valores nulos.
    """

    tbl_valor_industria.to_csv('Limpiados/tbl_valor_industria.csv', index = False)

    #
    #
    #
    #tbl_renta_recursos_naturales
    # LIMPIEZA tbl_renta_recursos_naturales

    tbl_renta_recursos_naturales = pd.read_csv("Extraccion/tbl_renta_recursos_naturales.csv")

    """
    CONTAMOS VALORES NULOS
    tbl_renta_recursos_naturales.isnull().sum()
    En total son 6
    """

    """
    Vemos que paises tienen datos faltantes
    print("Paises con datos nulos")
    paises_nulos=[]
    for i in paises:
        mask = tbl_renta_recursos_naturales["Pais_ID"] == i
        df_filtrada = tbl_renta_recursos_naturales[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a > 0:
            paises_nulos.append(i)
    print(paises_nulos)
    [VEN] tiene valores faltantes
    """

    #Solo venezuela tiene datos nulos, vamos a interpolarlos
    
    temp = tbl_renta_recursos_naturales[tbl_renta_recursos_naturales['id_pais'] == "VEN"]
    temp = temp.interpolate(method="linear",limit_direction="backward")
    tbl_renta_recursos_naturales[tbl_renta_recursos_naturales['id_pais'] == "VEN"] = temp

    tbl_renta_recursos_naturales.to_csv('Limpiados/tbl_renta_recursos_naturales.csv', index = False)

    #
    #
    #
    #tbl_camas_hospitales
    tbl_camas_hospitales = pd.read_csv("Extraccion/tbl_camas_hospitales.csv")
    
    """
    CONTAMOS VALORES NULOS
    tbl_camas_hospitales.isnull().sum()
    son 270 valores faltantes
    """

    """
    #Vemos que paises tienen datos faltantes
    print("Paises con datos nulos")
    paises_nulos=[]
    for i in paises:
        mask = tbl_camas_hospitales["Pais_ID"] == i
        df_filtrada = tbl_camas_hospitales[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a > 0:
            paises_nulos.append(i)
    print(paises_nulos)

    ['ATG', 'ARG', 'BRB', 'BLZ', 'BOL', 'BRA', 'CAN', 'CHL', 'COL', 'CRI', 'CUB', 'DMA', 'DOM', 'ECU', 'SLV', 'GRD', 'GTM', 'GUY', 'HTI',
    'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'PRY', 'PER', 'KNA', 'LCA', 'VCT', 'SUR', 'BHS', 'TTO', 'USA', 'URY', 'VEN']
    Son los paises con valores faltantes
    """

    #Todos los paises tienen datos nulos. Vamos a interpolar en ambas direcciones
    for i in paises:
        temp = tbl_camas_hospitales[tbl_camas_hospitales['id_pais'] == i]
        temp = temp.interpolate(method="linear",limit_direction="both")
        tbl_camas_hospitales[tbl_camas_hospitales['id_pais'] == i] = temp

    tbl_camas_hospitales.to_csv('Limpiados/tbl_camas_hospitales.csv', index = False)
    #
    #
    ## tbl_inversion_salud

    tbl_inversion_salud = pd.read_csv("Extraccion/tbl_inversion_salud.csv")
    tbl_inversion_salud= tbl_inversion_salud.interpolate(method='linear',limit_direction='forward', axis=0)
    tbl_inversion_salud.to_csv('Limpiados/tbl_inversion_salud.csv', index = False)
    
    #
    #
    ## tbl_agotamiento_recursos_naturales

    tbl_agotamiento_recursos_naturales = pd.read_csv("Extraccion/tbl_agotamiento_recursos_naturales.csv")

    tbl_agotamiento_recursos_naturales = tbl_agotamiento_recursos_naturales.interpolate(method='linear',limit_direction='forward', axis=0)

    for pais in paises:
        temp = tbl_agotamiento_recursos_naturales[tbl_agotamiento_recursos_naturales['id_pais']==pais]
        temp = temp.fillna(method = 'bfill')
        tbl_agotamiento_recursos_naturales[tbl_agotamiento_recursos_naturales['id_pais']==pais] = temp

    tbl_agotamiento_recursos_naturales.to_csv('Limpiados/tbl_agotamiento_recursos_naturales.csv', index = False)

    #
    #
    # tbl_inversion_desarrollo

    tbl_inversion_desarrollo = pd.read_csv("Extraccion/tbl_inversion_desarrollo.csv")

    tbl_inversion_desarrollo = tbl_inversion_desarrollo.interpolate(method='linear',limit_direction='forward', axis=0)

    for pais in paises:
        temp = tbl_inversion_desarrollo[tbl_inversion_desarrollo['id_pais']==pais]
        temp = temp.fillna(method = 'bfill')
        tbl_inversion_desarrollo[tbl_inversion_desarrollo['id_pais']==pais] = temp
    
    tbl_inversion_desarrollo.to_csv('Limpiados/tbl_inversion_desarrollo.csv', index = False)

    #
    #
    # tbl_gini
    #CREACION DE DATAFRAME
    tbl_gini = pd.read_csv('Extraccion/tbl_gini.csv')
    paises_nulos=[]
    for i in paises:
        mask = tbl_gini["id_pais"] == i
        df_filtrada = tbl_gini[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)
    paises_nulos2=[]
    for i in paises:
        mask = tbl_gini["id_pais"] == i
        df_filtrada = tbl_gini[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a > 0:
            paises_nulos2.append(i)

    #Cargamos la tabla con otro formato para tener una mejor visualizacion
    wb.db= 2
    tbl_gini2 = tbl_gini.pivot(index='year', columns=['id_pais'], values='gini')
    tbl_gini2

    #Todos los paises tienen datos nulos. Vamos a interpolar en ambas direcciones
    for i in paises:
        temp = tbl_gini[tbl_gini['id_pais'] == i]
        temp = temp.interpolate(method="linear",limit_direction="both")
        tbl_gini[tbl_gini['id_pais'] == i] = temp

    paises_nulos=[]
    for i in paises:
        mask = tbl_gini["id_pais"] == i
        df_filtrada = tbl_gini[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)
    """
    Podemos dividir los paises con datos faltantes en grupos:<br>
    ### Islas pequeñas del caribe<br>
    ATG: Antigua y Barbuda<br>
    BRB: Barbados<br>
    DMA: Dominica<br>
    GRD: Granada<br>
    KNA: St. Kitts and Nevis<br>
    VCT: St. Vincent and the Grenadines<br>

    ### Islas medias y grandes del caribe
    BHS: Bahamas<br>
    CUB: Cuba<br>

    ### Centro América:<br>
    BLZ: Belize<br>

    ### Costa Norte de Sud America:<br>
    TTO: Trinidad y Tobago<br>
    GUY: Guyana<br>
    SUR: Suriname<br>
    """
    #creamos la lista de las islas pequeñas
    islas_p=["ATG","BRB","DMA","GRD","KNA","VCT"]
    #Modificamos los valores nulos
    for i in islas_p:
        year=2020
        for e in range(0, 22):
            mask1= (tbl_gini["id_pais"] == i) & (tbl_gini["year"] == year)
            tbl_gini.loc[mask1, "gini"] = 51.2
            year= int(year)
            year = year-1
    #Vemos que paises tienen TODOS sus datos faltantes
    paises_nulos=[]
    for i in paises:
        mask = tbl_gini["id_pais"] == i
        df_filtrada = tbl_gini[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)
    #Para CUBA imputaremos el valor 44.0
    year=2020
    for e in range(0, 22):
            mask1= (tbl_gini["id_pais"] == "CUB") & (tbl_gini["year"] == year)
            tbl_gini.loc[mask1, "gini"] = 44.0
            year= int(year)
            year = year-1
    #Para BAHAMAS imputaremos el valor 40.7
    year=2020
    for e in range(0, 22):
            mask1= (tbl_gini["id_pais"] == "BHS") & (tbl_gini["year"] == year)
            tbl_gini.loc[mask1, "gini"] = 40.7
            year= int(year)
            year = year-1

    paises_nulos=[]
    for i in paises:
        mask = tbl_gini["id_pais"] == i
        df_filtrada = tbl_gini[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)

    #Ingresaremos el valor 53.3 en Belize en el año 2000
    mask1= (tbl_gini["id_pais"] == "BLZ") & (tbl_gini["year"] == 2000)
    tbl_gini.loc[mask1, "gini"] = 53.3
    #Creamos un dataframe con el Indice GINI de GTM
    df1=tbl_gini[tbl_gini["id_pais"] == "GTM"].reset_index()
    df1.drop(["index","id_pais","year"], axis=1, inplace=True)
    #Creamos una lista que indique la variacion inter anual comenzando con el año 2000 para GTM para arriba
    var_anual=[]
    for i in reversed(range(len(df1)-1)):
        val_ant=df1.loc[i+1,"gini"]
        val_act=df1.loc[i,"gini"]
        var_anual.append(round((val_act/val_ant),4))
    
    #Reemplazamos los nulos en Belize multiplicados por la variacion calculada de GTM
    year_act=2001
    year_prev=2000
    for e in var_anual:
        mask1= (tbl_gini["id_pais"] == "BLZ") & (tbl_gini["year"] == year_act)
        mask2= (tbl_gini["id_pais"] == "BLZ") & (tbl_gini["year"] == year_prev)
        val=tbl_gini["gini"].loc[mask2].values[0] * e
        tbl_gini.loc[mask1, "gini"] = round(val, 4)
        year_act= int(year_act)
        year_act = year_act+1
        year_prev= int(year_prev)
        year_prev = year_prev+1
    
    paises_nulos=[]
    for i in paises:
        mask = tbl_gini["id_pais"] == i
        df_filtrada = tbl_gini[mask]
        a = df_filtrada.iloc[:,2].isnull().sum()
        if a == 21:
            paises_nulos.append(i)
    
    #Ingresaremos el valor 57.9 en Suriname en el año 2000
    mask1= (tbl_gini["id_pais"] == "SUR") & (tbl_gini["year"] == 2000)
    tbl_gini.loc[mask1, "gini"] = 57.9

    #Ingresaremos el valor 45.1 en Guyana en el año 2000
    mask1= (tbl_gini["id_pais"] == "GUY") & (tbl_gini["year"] == 2000)
    tbl_gini.loc[mask1, "gini"] = 45.1

    #Ingresaremos el valor 40.3 en Trinidad y Tobago en el año 2000
    mask1= (tbl_gini["id_pais"] == "TTO") & (tbl_gini["year"] == 2000)
    tbl_gini.loc[mask1, "gini"] = 40.3

    #Creamos un dataframe con el Indice GINI de VEN
    df1=tbl_gini[tbl_gini["id_pais"] == "VEN"].reset_index()
    df1.drop(["index","id_pais","year"], axis=1, inplace=True)

    #Creamos una lista que indique la variacion inter anual comenzando con el año 2000 para VEN para arriba
    var_anual=[]
    for i in reversed(range(len(df1)-1)):
        val_ant=df1.loc[i+1,"gini"]
        val_act=df1.loc[i,"gini"]
        var_anual.append(round((val_act/val_ant),4))

    #Creamos la lista de los paises de la costa norte SA
    costa_NSA=["SUR","GUY","TTO"]

    #Reemplazamos los nulos
    for i in costa_NSA:
        year_act=2001
        year_prev=2000
        for e in var_anual:
            mask1= (tbl_gini["id_pais"] == i) & (tbl_gini["year"] == year_act)
            mask2= (tbl_gini["id_pais"] == i) & (tbl_gini["year"] == year_prev)
            val=tbl_gini["gini"].loc[mask2].values[0] * e
            tbl_gini.loc[mask1, "gini"] = round(val, 4)
            year_act= int(year_act)
            year_act = year_act+1
            year_prev= int(year_prev)
            year_prev = year_prev+1
    tbl_gini.to_csv('Limpiados/tbl_gini.csv', index = False)