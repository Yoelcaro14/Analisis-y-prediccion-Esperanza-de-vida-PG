import psycopg2
import pandas as pd
from fbprophet import Prophet
import numpy as np
from sqlalchemy import create_engine
import psycopg2

def Predicciones(pais_iso, p_kpi2 = 20, p_kpi3 = 20, p_kpi4 = 50):

    conexion = psycopg2.connect(
            host = "proyecto-final-henry.ctv6lgil6x7r.us-east-1.rds.amazonaws.com",
            port = 5432,
            user = "postgres",
            password = "lorussoasoc",
            database = "lorussoasoc"
        )

    with conexion as conn:
        sql = "SELECT * FROM tbl_esperanza_vida"
        df = pd.read_sql_query(sql, conn)

    #listado de paises miembros OEA
    paises = df['id_pais'].unique()

    # para predicciones, trabajamos con data completa o dividimos en train (primeros años) y test(ultimos años)?
    pais_eval = pais_iso
    df_train = df[df['id_pais']==pais_eval].copy() #probaremos solo con los datos de Argentina
    df_train['year'] = pd.to_datetime(df_train['year'], format='%Y')
    df_train.set_index('year',inplace=True)
    df_train = df_train[:-1] # Eliminamos 2020 para probar, ya que la pandemia afecta mucho el valor EDVAN
    df_train.drop(columns=['id_pais'],inplace=True)
    df_train.reset_index(inplace=True)


    db_string = "postgresql://postgres:lorussoasoc@proyecto-final-henry.ctv6lgil6x7r.us-east-1.rds.amazonaws.com:5432/lorussoasoc"
    db = create_engine(db_string)

    query = """
    SELECT a.id_pais "PAIS", paises.pais "NOMBRE PAIS", a.year "ANIO", paises.longitude "LONG", paises.latitude "LAT", paises.incomelevel "NIVEL INGRESOS", esperanza.edvan "ESPERANZA",
        a.agua "ACCESO AGUA", 
        b.acceso_electricidad "ACCESO ELECTRICIDAD", 
        c.agotamiento_recursos "AGOTAMIENTO RECURSOS",
        d.alfabetizacion "ALFABETIZACION",
        e.anios_escolares "ANIOS ESCOLARIDAD",
        f.camas_hospitales "CAMAS HOSPITALES",
        g.alcohol "CONSUMO ALCOHOL",
        h.densidad_poblacion "DENSIDAD POBLACION",
        i.desempleo "DESEMPLEO",
        j.emisiones_co2 "EMISIONES CO2",
        k.fuerza_laboral "FUERZA LABORAL",
        l.gini "GINI",
        m.ingreso_medio_pc "INGRESO MEDIO PC",
        n.desarrollo "INVERSION DESARROLLO",
        o.inversion_educacion "INVERSION EDUCACION",
        p.salud "INVERSION SALUD",
        q.obesidad "OBESIDAD",
        r.pib "PIB",
        s.poblacion "POBLACION",
        t.produccion_alimentos "PRODUCCION ALIMENTOS",
        u.renta_recursos "RENTA RECURSOS",
        v.srv_sanit_bas "SERV SANITARIOS",
        w.industria "INDUSTRIA",
        x.tabaco "CONSUMO TABACO",
        y.contaminacion_aire "CONTAMINACION AIRE"
    FROM tbl_acceso_agua_potable a

    LEFT JOIN tbl_esperanza_vida esperanza
    ON a.id_pais = esperanza.id_pais AND a.year = esperanza.year

    LEFT JOIN tbl_paises paises
    ON a.id_pais = paises.id_pais

    LEFT JOIN tbl_acceso_electricidad b
    ON a.id_pais = b.id_pais AND a.year = b.year

    LEFT JOIN tbl_agotamiento_recursos_naturales c
    ON a.id_pais = c.id_pais AND a.year = c.year

    LEFT JOIN tbl_alfabetizacion_porc d
    ON a.id_pais = d.id_pais AND a.year = d.year

    LEFT JOIN tbl_anios_medios_escolaridad e
    ON a.id_pais = e.id_pais AND a.year = e.year

    LEFT JOIN tbl_camas_hospitales f
    ON a.id_pais = f.id_pais AND a.year = f.year

    LEFT JOIN tbl_consumo_alcohol g
    ON a.id_pais = g.id_pais AND a.year = g.year

    LEFT JOIN tbl_densidad_poblacion h
    ON a.id_pais = h.id_pais AND a.year = h.year

    LEFT JOIN tbl_desempleo_fl i
    ON a.id_pais = i.id_pais AND a.year = i.year

    LEFT JOIN tbl_emisiones_co2 j
    ON a.id_pais = j.id_pais AND a.year = j.year

    LEFT JOIN tbl_fuerza_laboral k
    ON a.id_pais = k.id_pais AND a.year = k.year

    LEFT JOIN tbl_gini l
    ON a.id_pais = l.id_pais AND a.year = l.year

    LEFT JOIN tbl_ingreso_medio_pc m
    ON a.id_pais = m.id_pais AND a.year = m.year

    LEFT JOIN tbl_inversion_desarrollo n
    ON a.id_pais = n.id_pais AND a.year = n.year

    LEFT JOIN tbl_inversion_educacion o
    ON a.id_pais = o.id_pais AND a.year = o.year

    LEFT JOIN tbl_inversion_salud p
    ON a.id_pais = p.id_pais AND a.year = p.year

    LEFT JOIN tbl_obesidad q
    ON a.id_pais = q.id_pais AND a.year = q.year

    LEFT JOIN tbl_pib r
    ON a.id_pais = r.id_pais AND a.year = r.year

    LEFT JOIN tbl_poblacion s
    ON a.id_pais = s.id_pais AND a.year = s.year

    LEFT JOIN tbl_produccion_alimentos t
    ON a.id_pais = t.id_pais AND a.year = t.year

    LEFT JOIN tbl_renta_recursos_naturales u
    ON a.id_pais = u.id_pais AND a.year = u.year

    LEFT JOIN tbl_srv_sanit_bas v
    ON a.id_pais = v.id_pais AND a.year = v.year

    LEFT JOIN tbl_valor_industria w
    ON a.id_pais = w.id_pais AND a.year = w.year

    LEFT JOIN tbl_consumo_tabaco x
    ON a.id_pais = x.id_pais AND a.year = x.year

    LEFT JOIN tbl_contaminacion_aire y
    ON a.id_pais = y.id_pais AND a.year = y.year

    """

    df = pd.read_sql_query(query, con = db)
    paises = ['ATG','ARG','BRB','BLZ','BOL','BRA','CAN','CHL','COL','CRI','CUB','DMA','DOM','ECU','SLV','GRD','GTM','GUY','HTI','HND','JAM','MEX','NIC','PAN','PRY','PER','KNA','LCA','VCT','SUR','BHS','TTO','USA','URY','VEN']

    #nivel_ingresos=df[["PAIS","NOMBRE PAIS","NIVEL INGRESOS"]].drop_duplicates().reset_index()
    #nivel_ingresos.drop(["index"], axis=1, inplace=True)

    #
    #
    #EDUCACION
    educacion = df[['PAIS',"NOMBRE PAIS",'ANIO','ALFABETIZACION','ANIOS ESCOLARIDAD','ESPERANZA']].copy()
    educacion.insert(5, "ED.INDEX", ((educacion["ALFABETIZACION"]/100)*educacion["ANIOS ESCOLARIDAD"]))
    salida_educacion = educacion[['PAIS','NOMBRE PAIS','ANIO','ED.INDEX','ESPERANZA']].copy()
    #salida_educacion.to_csv('educacion.csv', index=False)

    #
    #
    #MEDIO AMBIENTE
    medio_ambiente = df[['PAIS','NOMBRE PAIS','ANIO','EMISIONES CO2','CONTAMINACION AIRE','ACCESO AGUA','PRODUCCION ALIMENTOS','AGOTAMIENTO RECURSOS','ESPERANZA']].copy()
    medio_ambiente.insert(8, "IND.AGUA", (medio_ambiente["ACCESO AGUA"]*df['POBLACION']/1000000000))

    for pais in paises:
        medio_ambiente2 = medio_ambiente[medio_ambiente['PAIS']==pais].copy()
        med1 = medio_ambiente2['IND.AGUA'].mean()
        std1 = medio_ambiente2['IND.AGUA'].std()
        med2 = medio_ambiente2['PRODUCCION ALIMENTOS'].mean()
        std2 = medio_ambiente2['PRODUCCION ALIMENTOS'].std()
        med2_deseada = std2 * med1 / std1
    if med2 < med2_deseada:
        delta = med2_deseada - med2
    else:
        delta = med2 - med2_deseada
    medio_ambiente2['PRODUCCION ALIMENTOS'] = medio_ambiente2['PRODUCCION ALIMENTOS'] + delta
    medio_ambiente.loc[medio_ambiente['PAIS']==pais, 'PRODUCCION ALIMENTOS'] = medio_ambiente2.loc[medio_ambiente2['PAIS']==pais,'PRODUCCION ALIMENTOS'].values

    medio_ambiente.insert(9,'Agua.Alim', medio_ambiente['IND.AGUA']*medio_ambiente['PRODUCCION ALIMENTOS'])

    for pais in paises:
        medio_ambiente2 = medio_ambiente[medio_ambiente['PAIS']==pais].copy()
        med1 = medio_ambiente2['Agua.Alim'].mean()
        std1 = medio_ambiente2['Agua.Alim'].std()
        med2 = medio_ambiente2['CONTAMINACION AIRE'].mean()
        std2 = medio_ambiente2['CONTAMINACION AIRE'].std()
        med2_deseada = std2 * med1 / std1
    if med2 < med2_deseada:
        delta = med2_deseada - med2
    else:
        delta = med2 - med2_deseada
    medio_ambiente2['CONTAMINACION AIRE'] = medio_ambiente2['CONTAMINACION AIRE'] + delta
    medio_ambiente.loc[medio_ambiente['PAIS']==pais, 'CONTAMINACION AIRE'] = medio_ambiente2.loc[medio_ambiente2['PAIS']==pais,'CONTAMINACION AIRE'].values

    medio_ambiente.insert(10,'AMB.INDEX', medio_ambiente['Agua.Alim']/medio_ambiente['CONTAMINACION AIRE'])
    salida_medio_ambiente = medio_ambiente[['PAIS','NOMBRE PAIS','ANIO','AMB.INDEX','ESPERANZA']].copy()
    #salida_medio_ambiente.to_csv('medio_ambiente.csv', index=False)


    #
    #
    #NIVEL DE VIDA
    nivel_vida = df[['PAIS','NOMBRE PAIS','ANIO','CONSUMO ALCOHOL','CONSUMO TABACO','SERV SANITARIOS','ACCESO ELECTRICIDAD','ESPERANZA']].copy()

    nivel_vida.insert(5, "HAB.MEAN", ((nivel_vida["CONSUMO ALCOHOL"]+nivel_vida["CONSUMO TABACO"])/200))
    nivel_vida.insert(8, "ACC.AE", (nivel_vida["SERV SANITARIOS"]/100)*(nivel_vida["ACCESO ELECTRICIDAD"]/100))
    nivel_vida.insert(9, "IND.N.VIDA", (nivel_vida["ACC.AE"]/nivel_vida["HAB.MEAN"]))

    ind_nivel_vida = nivel_vida[['PAIS','NOMBRE PAIS','ANIO','IND.N.VIDA','ESPERANZA']].copy()
    #ind_nivel_vida.to_csv('nivel_vida.csv', index=False)

    #
    #
    #RECURSOS Y ESTADO
    ind_estado=df[["PAIS","NOMBRE PAIS","ANIO","INVERSION SALUD","INVERSION DESARROLLO","INVERSION EDUCACION","PIB","GINI","ESPERANZA"]].copy()
    ind_estado.insert(6, "INVERS.", (ind_estado["INVERSION SALUD"]/100+ind_estado["INVERSION DESARROLLO"]/100+ind_estado["INVERSION EDUCACION"]/100))
    ind_estado.insert(8, "PIB.INV", (ind_estado["PIB"]*ind_estado["INVERS."]))
    ind_estado.insert(9, "DELTA","")
    for i in paises:
        std1=ind_estado[ind_estado["PAIS"]==i]["PIB.INV"].std()
        std2=ind_estado[ind_estado["PAIS"]==i]["GINI"].std()
        mean1=ind_estado[ind_estado["PAIS"]==i]["PIB.INV"].mean()
        mean2=ind_estado[ind_estado["PAIS"]==i]["GINI"].mean()
        n_mean=std1*mean2/std2
        delta=n_mean-mean1
        ind_estado.loc[ind_estado["PAIS"] == i, "DELTA"] = delta
    ind_estado= ind_estado.astype({"DELTA":"float64"})
    ind_estado.insert(11, "ESTADO.INDEX", (ind_estado["PIB.INV"]+ind_estado["DELTA"])/(ind_estado["GINI"]*100000000))
    ind_estado = ind_estado[['PAIS','NOMBRE PAIS','ANIO','ESTADO.INDEX','ESPERANZA']]
    #ind_estado.to_csv('recursos_y_estado.csv', index=False)

    #
    #
    #Trabajo
    trabajo = df[['PAIS','NOMBRE PAIS','ANIO','FUERZA LABORAL','DESEMPLEO','INGRESO MEDIO PC','POBLACION','ESPERANZA']].copy()
    trabajo.insert(5, "EMPLEADOS", round(trabajo["FUERZA LABORAL"]*(1-(trabajo["DESEMPLEO"]/100)),0))
    trabajo.insert(7, "TRAB.INDEX", (trabajo["EMPLEADOS"]*trabajo["INGRESO MEDIO PC"])/trabajo["POBLACION"])

    salida_trabajo = trabajo[['PAIS','NOMBRE PAIS','ANIO','TRAB.INDEX','ESPERANZA']]
    #salida_trabajo.to_csv('trabajo.csv', index=False)


    indices = pd.merge(salida_educacion, salida_medio_ambiente[['PAIS', 'NOMBRE PAIS','ANIO','AMB.INDEX']], how="left", left_on=['PAIS', 'NOMBRE PAIS','ANIO'], right_on=['PAIS', 'NOMBRE PAIS','ANIO'])
    indices = pd.merge(indices, ind_nivel_vida[['PAIS', 'NOMBRE PAIS','ANIO','IND.N.VIDA']], how="left", left_on=['PAIS', 'NOMBRE PAIS','ANIO'], right_on=['PAIS', 'NOMBRE PAIS','ANIO'])
    indices = pd.merge(indices, ind_estado[['PAIS', 'NOMBRE PAIS','ANIO','ESTADO.INDEX']], how="left", left_on=['PAIS', 'NOMBRE PAIS','ANIO'], right_on=['PAIS', 'NOMBRE PAIS','ANIO'])
    indices = pd.merge(indices, salida_trabajo[['PAIS', 'NOMBRE PAIS','ANIO','TRAB.INDEX']], how="left", left_on=['PAIS', 'NOMBRE PAIS','ANIO'], right_on=['PAIS', 'NOMBRE PAIS','ANIO'])
    indices = indices[['PAIS', 'NOMBRE PAIS', 'ANIO', 'ED.INDEX', 'AMB.INDEX','IND.N.VIDA', 'ESTADO.INDEX', 'TRAB.INDEX', 'ESPERANZA']]


    #obtenemos el df indices solo para argentina para realizar pruebas
    df_train = indices[indices['PAIS']==pais_iso].copy()
    df_train['ANIO'] = pd.to_datetime(df_train['ANIO'], format='%Y')
    df_train.set_index('ANIO',inplace=True)
    df_train = df_train[:-1] # Eliminamos 2020 para probar, ya que por pandemia suponemos baja mucho en este año
    df_train.drop(columns=['PAIS','NOMBRE PAIS'],inplace=True)
    df_train.reset_index(inplace=True)

    df_train = df_train.rename(columns={'ESPERANZA': 'y', 'ANIO':'ds'})
    df_train['y_orig'] = df_train['y']

    model_new = Prophet() 
    model_new.add_regressor('ED.INDEX')
    model_new.add_regressor('AMB.INDEX')
    model_new.add_regressor('IND.N.VIDA')
    model_new.add_regressor('ESTADO.INDEX')
    model_new.add_regressor('TRAB.INDEX')

    model_new.fit(df_train)

    # DATAFRAME NEUTRO
    anios = 5
    future_data = model_new.make_future_dataframe(periods=anios, freq = 'A') # Definimos nuevo set de datos con frecuencia anual
    future_data2 = future_data.copy()
    future_data[['ds', 'ED.INDEX', 'AMB.INDEX', 'IND.N.VIDA', 'ESTADO.INDEX','TRAB.INDEX', 'y', 'y_orig']] = df_train[['ds', 'ED.INDEX', 'AMB.INDEX', 'IND.N.VIDA', 'ESTADO.INDEX','TRAB.INDEX', 'y', 'y_orig']]
    future_data.loc[20:24,:] = future_data2.loc[20:24,:].copy()
    predecir = future_data.copy()
    predecir.loc[20:24,'ED.INDEX':'TRAB.INDEX'] = df_train.loc[19:19,'ED.INDEX':'TRAB.INDEX'].values

    # DATAFRAME KPI2
    porc_adic_educ = p_kpi2
    db_string = "postgresql://postgres:lorussoasoc@proyecto-final-henry.ctv6lgil6x7r.us-east-1.rds.amazonaws.com:5432/lorussoasoc"
    db = create_engine(db_string)

    query = """
    SELECT a.id_pais "PAIS", paises.pais "NOMBRE PAIS", a.year "ANIO", paises.longitude "LONG", paises.latitude "LAT", paises.incomelevel "NIVEL INGRESOS", esperanza.edvan "ESPERANZA",
        a.agua "ACCESO AGUA", 
        b.acceso_electricidad "ACCESO ELECTRICIDAD", 
        c.agotamiento_recursos "AGOTAMIENTO RECURSOS",
        d.alfabetizacion "ALFABETIZACION",
        e.anios_escolares "ANIOS ESCOLARIDAD",
        f.camas_hospitales "CAMAS HOSPITALES",
        g.alcohol "CONSUMO ALCOHOL",
        h.densidad_poblacion "DENSIDAD POBLACION",
        i.desempleo "DESEMPLEO",
        j.emisiones_co2 "EMISIONES CO2",
        k.fuerza_laboral "FUERZA LABORAL",
        l.gini "GINI",
        m.ingreso_medio_pc "INGRESO MEDIO PC",
        n.desarrollo "INVERSION DESARROLLO",
        o.inversion_educacion "INVERSION EDUCACION",
        p.salud "INVERSION SALUD",
        q.obesidad "OBESIDAD",
        r.pib "PIB",
        s.poblacion "POBLACION",
        t.produccion_alimentos "PRODUCCION ALIMENTOS",
        u.renta_recursos "RENTA RECURSOS",
        v.srv_sanit_bas "SERV SANITARIOS",
        w.industria "INDUSTRIA",
        x.tabaco "CONSUMO TABACO",
        y.contaminacion_aire "CONTAMINACION AIRE"
    FROM tbl_acceso_agua_potable a

    LEFT JOIN tbl_esperanza_vida esperanza
    ON a.id_pais = esperanza.id_pais AND a.year = esperanza.year

    LEFT JOIN tbl_paises paises
    ON a.id_pais = paises.id_pais

    LEFT JOIN tbl_acceso_electricidad b
    ON a.id_pais = b.id_pais AND a.year = b.year

    LEFT JOIN tbl_agotamiento_recursos_naturales c
    ON a.id_pais = c.id_pais AND a.year = c.year

    LEFT JOIN tbl_alfabetizacion_porc d
    ON a.id_pais = d.id_pais AND a.year = d.year

    LEFT JOIN tbl_anios_medios_escolaridad e
    ON a.id_pais = e.id_pais AND a.year = e.year

    LEFT JOIN tbl_camas_hospitales f
    ON a.id_pais = f.id_pais AND a.year = f.year

    LEFT JOIN tbl_consumo_alcohol g
    ON a.id_pais = g.id_pais AND a.year = g.year

    LEFT JOIN tbl_densidad_poblacion h
    ON a.id_pais = h.id_pais AND a.year = h.year

    LEFT JOIN tbl_desempleo_fl i
    ON a.id_pais = i.id_pais AND a.year = i.year

    LEFT JOIN tbl_emisiones_co2 j
    ON a.id_pais = j.id_pais AND a.year = j.year

    LEFT JOIN tbl_fuerza_laboral k
    ON a.id_pais = k.id_pais AND a.year = k.year

    LEFT JOIN tbl_gini l
    ON a.id_pais = l.id_pais AND a.year = l.year

    LEFT JOIN tbl_ingreso_medio_pc m
    ON a.id_pais = m.id_pais AND a.year = m.year

    LEFT JOIN tbl_inversion_desarrollo n
    ON a.id_pais = n.id_pais AND a.year = n.year

    LEFT JOIN tbl_inversion_educacion o
    ON a.id_pais = o.id_pais AND a.year = o.year

    LEFT JOIN tbl_inversion_salud p
    ON a.id_pais = p.id_pais AND a.year = p.year

    LEFT JOIN tbl_obesidad q
    ON a.id_pais = q.id_pais AND a.year = q.year

    LEFT JOIN tbl_pib r
    ON a.id_pais = r.id_pais AND a.year = r.year

    LEFT JOIN tbl_poblacion s
    ON a.id_pais = s.id_pais AND a.year = s.year

    LEFT JOIN tbl_produccion_alimentos t
    ON a.id_pais = t.id_pais AND a.year = t.year

    LEFT JOIN tbl_renta_recursos_naturales u
    ON a.id_pais = u.id_pais AND a.year = u.year

    LEFT JOIN tbl_srv_sanit_bas v
    ON a.id_pais = v.id_pais AND a.year = v.year

    LEFT JOIN tbl_valor_industria w
    ON a.id_pais = w.id_pais AND a.year = w.year

    LEFT JOIN tbl_consumo_tabaco x
    ON a.id_pais = x.id_pais AND a.year = x.year

    LEFT JOIN tbl_contaminacion_aire y
    ON a.id_pais = y.id_pais AND a.year = y.year

    """

    df = pd.read_sql_query(query, con = db)
    paises = ['ATG','ARG','BRB','BLZ','BOL','BRA','CAN','CHL','COL','CRI','CUB','DMA','DOM','ECU','SLV','GRD','GTM','GUY','HTI','HND','JAM','MEX','NIC','PAN','PRY','PER','KNA','LCA','VCT','SUR','BHS','TTO','USA','URY','VEN']

    Ind_Estado=df[["PAIS","NOMBRE PAIS","ANIO","INVERSION SALUD","INVERSION DESARROLLO","INVERSION EDUCACION","PIB","GINI","ESPERANZA"]]
    Ind_Estado.insert(6, "INVERS.", (Ind_Estado["INVERSION SALUD"]/100+Ind_Estado["INVERSION DESARROLLO"]/100+Ind_Estado["INVERSION EDUCACION"]*(1 + porc_adic_educ/100)/100))
    Ind_Estado.insert(8, "PIB.INV", (Ind_Estado["PIB"]*Ind_Estado["INVERS."]))
    Ind_Estado.insert(9, "DELTA","")
    for i in paises:
        std1=Ind_Estado[Ind_Estado["PAIS"]==i]["PIB.INV"].std()
        std2=Ind_Estado[Ind_Estado["PAIS"]==i]["GINI"].std()
        mean1=Ind_Estado[Ind_Estado["PAIS"]==i]["PIB.INV"].mean()
        mean2=Ind_Estado[Ind_Estado["PAIS"]==i]["GINI"].mean()
        n_mean=std1*mean2/std2
        delta=n_mean-mean1
        Ind_Estado.loc[Ind_Estado["PAIS"] == i, "DELTA"] = delta
    Ind_Estado= Ind_Estado.astype({"DELTA":"float64"})
    Ind_Estado.insert(11, "ESTADO.INDEX", (Ind_Estado["PIB.INV"]+Ind_Estado["DELTA"])/(Ind_Estado["GINI"]*100000000))

    Ind_Estado = Ind_Estado[Ind_Estado['PAIS']==pais_eval]
    Ind_Estado = Ind_Estado[:-1] # Eliminamos 2020 para probar, ya que la pandemia afecta mucho el valor EDVAN

    predecir_kpi2 = predecir.copy()
    predecir_kpi2.loc[20:24,'ESTADO.INDEX'] = Ind_Estado['ESTADO.INDEX'].iloc[-1] #asignamos el nuevo valor calculado


    # DATAFRAME KPI 3
    porc_adic_salud = p_kpi3
    Ind_Estado=df[["PAIS","NOMBRE PAIS","ANIO","INVERSION SALUD","INVERSION DESARROLLO","INVERSION EDUCACION","PIB","GINI","ESPERANZA"]]
    Ind_Estado.insert(6, "INVERS.", (Ind_Estado["INVERSION SALUD"]*(1 + porc_adic_salud/100)/100+Ind_Estado["INVERSION DESARROLLO"]/100+Ind_Estado["INVERSION EDUCACION"]/100))
    Ind_Estado.insert(8, "PIB.INV", (Ind_Estado["PIB"]*Ind_Estado["INVERS."]))
    Ind_Estado.insert(9, "DELTA","")
    for i in paises:
        std1=Ind_Estado[Ind_Estado["PAIS"]==i]["PIB.INV"].std()
        std2=Ind_Estado[Ind_Estado["PAIS"]==i]["GINI"].std()
        mean1=Ind_Estado[Ind_Estado["PAIS"]==i]["PIB.INV"].mean()
        mean2=Ind_Estado[Ind_Estado["PAIS"]==i]["GINI"].mean()
        n_mean=std1*mean2/std2
        delta=n_mean-mean1
        Ind_Estado.loc[Ind_Estado["PAIS"] == i, "DELTA"] = delta
    Ind_Estado= Ind_Estado.astype({"DELTA":"float64"})
    Ind_Estado.insert(11, "ESTADO.INDEX", (Ind_Estado["PIB.INV"]+Ind_Estado["DELTA"])/(Ind_Estado["GINI"]*100000000))

    Ind_Estado = Ind_Estado[Ind_Estado['PAIS']==pais_eval]
    Ind_Estado = Ind_Estado[:-1] # Eliminamos 2020 para probar, ya que la pandemia afecta mucho el valor EDVAN

    predecir_kpi3 = predecir.copy()
    predecir_kpi3.loc[20:24,'ESTADO.INDEX'] = Ind_Estado['ESTADO.INDEX'].iloc[-1] #asignamos el nuevo valor calculado

    #
    #
    # DATAFRAME KPI 4
    porc_reduc_cont = p_kpi4
    medio_ambiente = df[['PAIS','NOMBRE PAIS','ANIO','EMISIONES CO2','CONTAMINACION AIRE','ACCESO AGUA','PRODUCCION ALIMENTOS','AGOTAMIENTO RECURSOS','ESPERANZA']]

    medio_ambiente.insert(8, "IND.AGUA", (medio_ambiente["ACCESO AGUA"]*df['POBLACION']/1000000000))

    for pais in paises:
        medio_ambiente2 = medio_ambiente[medio_ambiente['PAIS']==pais]
        med1 = medio_ambiente2['IND.AGUA'].mean()
        std1 = medio_ambiente2['IND.AGUA'].std()
        med2 = medio_ambiente2['PRODUCCION ALIMENTOS'].mean()
        std2 = medio_ambiente2['PRODUCCION ALIMENTOS'].std()
        med2_deseada = std2 * med1 / std1
    if med2 < med2_deseada:
        delta = med2_deseada - med2
    else:
        delta = med2 - med2_deseada
    medio_ambiente2['PRODUCCION ALIMENTOS'] = medio_ambiente2['PRODUCCION ALIMENTOS'] + delta
    medio_ambiente.loc[medio_ambiente['PAIS']==pais, 'PRODUCCION ALIMENTOS'] = medio_ambiente2.loc[medio_ambiente2['PAIS']==pais,'PRODUCCION ALIMENTOS'].values

    medio_ambiente.insert(9,'Agua.Alim', medio_ambiente['IND.AGUA']*medio_ambiente['PRODUCCION ALIMENTOS'])

    for pais in paises:
        medio_ambiente2 = medio_ambiente[medio_ambiente['PAIS']==pais]
        med1 = medio_ambiente2['Agua.Alim'].mean()
        std1 = medio_ambiente2['Agua.Alim'].std()
        med2 = medio_ambiente2['CONTAMINACION AIRE'].mean()
        std2 = medio_ambiente2['CONTAMINACION AIRE'].std()
        med2_deseada = std2 * med1 / std1
    if med2 < med2_deseada:
        delta = med2_deseada - med2
    else:
        delta = med2 - med2_deseada
    medio_ambiente2['CONTAMINACION AIRE'] = medio_ambiente2['CONTAMINACION AIRE']*(1 - porc_reduc_cont/100) + delta #Reducimos contaminación aire en 50%
    medio_ambiente.loc[medio_ambiente['PAIS']==pais, 'CONTAMINACION AIRE'] = medio_ambiente2.loc[medio_ambiente2['PAIS']==pais,'CONTAMINACION AIRE'].values

    medio_ambiente.insert(10,'AMB.INDEX', medio_ambiente['Agua.Alim']/medio_ambiente['CONTAMINACION AIRE'])

    salida_medio_ambiente = medio_ambiente[['PAIS','NOMBRE PAIS','ANIO','AMB.INDEX','ESPERANZA']]


    predecir_kpi4 = predecir.copy()
    predecir_kpi4.loc[20:24,'AMB.INDEX'] = salida_medio_ambiente['AMB.INDEX'].iloc[-1] #asignamos el nuevo valor calculado

    #
    #
    #
    #Se realizan predicciones

    #EDVAN si todo permanece igual
    forecast_data = model_new.predict(predecir)
    forecast_data_orig = forecast_data
    final_df = pd.DataFrame(forecast_data_orig)

    #Prediccion KPI2
    forecast_data_kpi2 = model_new.predict(predecir_kpi2)

    #Prediccion KPI3
    forecast_data_kpi3 = model_new.predict(predecir_kpi3)

    #Prediccion KPI4
    forecast_data_kpi4 = model_new.predict(predecir_kpi4)

    #Resultados
    edvan_neutro = forecast_data['yhat'].iloc[-1]
    edvan_kpi2 = forecast_data_kpi2['yhat'].iloc[-1]
    edvan_kpi3 = forecast_data_kpi3['yhat'].iloc[-1]
    edvan_kpi4 = forecast_data_kpi4['yhat'].iloc[-1]

    #Se expresa resultados en meses
    kpi1 = (df_train['y'].iloc[-1] - df_train['y'].iloc[-6])*12
    kpi2 = (edvan_kpi2 - edvan_neutro)*12
    kpi3 = (edvan_kpi3 - edvan_neutro)*12
    kpi4 = (edvan_kpi4 - edvan_neutro)*12

    #dataframes
    df_kpi1 = forecast_data[['ds','yhat']]
    df_kpi2 = forecast_data_kpi2[['ds','yhat']]
    df_kpi3 = forecast_data_kpi3[['ds','yhat']]
    df_kpi4 = forecast_data_kpi4[['ds','yhat']]

    return(kpi1, df_kpi1, kpi2, df_kpi2, kpi3, df_kpi3, kpi4, df_kpi4)


