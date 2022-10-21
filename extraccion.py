import wbgapi as wb
import pandas as pd


def extraccion():
    #Definimos la lista con los países miembros de la OEA
    paises = ['ATG','ARG','BRB','BLZ','BOL','BRA','CAN','CHL','COL','CRI','CUB','DMA','DOM','ECU','SLV','GRD','GTM','GUY','HTI','HND','JAM','MEX','NIC','PAN','PRY','PER','KNA','LCA','VCT','SUR','BHS','TTO','USA','URY','VEN'] 

    #tbl_paises  0
    #Extraemos listado de paises de wb
    print("extrayendo tabla tbl_paises...")
    tbl_paises = wb.economy.DataFrame()
    tbl_paises.drop(columns=['aggregate','region','adminregion','lendingType'], inplace=True)
    tbl_paises.reset_index(inplace=True)
    tbl_paises = tbl_paises[tbl_paises['id'].isin(paises)]
    tbl_paises.reset_index(drop=True)
    tbl_paises.columns = ['id_pais','pais','longitude','latitude','incomeLevel','capitalCity']
    tbl_paises.to_csv('Extraccion/tbl_paises.csv', index = False)


    #tbl_esperanza_vida  1
    print("extrayendo tabla tbl_esperanza_vida...")
    tbl_esperanza_vida = pd.read_csv('Datasets/EsperanzaNacionesUnidas.csv')
    tbl_esperanza_vida = tbl_esperanza_vida[['Time','Iso3','Value']]
    tbl_esperanza_vida.columns = ['Year', 'id_pais', 'edvan']
    tbl_esperanza_vida = tbl_esperanza_vida[tbl_esperanza_vida['id_pais'].isin(paises)]
    tbl_esperanza_vida.reset_index(inplace=True,drop=True)
    tbl_esperanza_vida.columns = ['year','id_pais','edvan']
    tbl_esperanza_vida.to_csv('Extraccion/tbl_esperanza_vida.csv', index = False)

    #tbl_poblacion  2
    print("extrayendo tabla tbl_poblacion...")
    tbl_poblacion = wb.data.DataFrame('SP.POP.TOTL',paises, time =range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_poblacion.drop(["time","Country"], axis=1, inplace=True)
    tbl_poblacion.columns = ['id_pais','year','poblacion']
    tbl_poblacion.to_csv('Extraccion/tbl_poblacion.csv', index = False)
    
    #tbl_alfabetizacion_porc  3
    print("extrayendo tabla tbl_alfabetizacion_porc...")
    tbl_alfabetizacion_porc = wb.data.DataFrame('SE.ADT.LITR.ZS',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_alfabetizacion_porc.drop(["time","Country"], axis=1, inplace=True)
    tbl_alfabetizacion_porc.columns = ['id_pais','year','alfabetizacion']
    tbl_alfabetizacion_porc.to_csv('Extraccion/tbl_alfabetizacion_porc.csv', index = False)

    #tbl_fuerza_laboral  4
    print("extrayendo tabla tbl_fuerza_laboral...")
    tbl_fuerza_laboral = wb.data.DataFrame('SL.TLF.TOTL.IN',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_fuerza_laboral.drop(["time","Country"], axis=1, inplace=True)
    tbl_fuerza_laboral.columns = ["id_pais", "year", " fuerza_laboral"]
    tbl_fuerza_laboral.to_csv('Extraccion/tbl_fuerza_laboral.csv', index = False)

    #tbl_ingreso_medio_pc  5
    print("extrayendo tabla tbl_ingreso_medio_pc...")
    tbl_ingreso_medio_pc = wb.data.DataFrame('NY.GNP.PCAP.CD',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_ingreso_medio_pc.drop(["time","Country"], axis=1, inplace=True)
    tbl_ingreso_medio_pc.columns = ["id_pais", "year", " ingreso_medio_pc"]
    tbl_ingreso_medio_pc.to_csv('Extraccion/tbl_ingreso_medio_pc.csv', index = False)

    
    #tbl_contaminacion_aire  6
    print("extrayendo tabla tbl_contaminacion_aire...")
    tbl_contaminacion_aire = wb.data.DataFrame('EN.ATM.PM25.MC.M3',paises,time =  range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_contaminacion_aire.drop(["time","Country"], axis=1, inplace=True)
    tbl_contaminacion_aire.columns = ["id_pais", "year", " contaminacion_aire"]
    tbl_contaminacion_aire.to_csv('Extraccion/tbl_contaminacion_aire.csv', index = False)

    

    #tbl_inversion_educacion  7
    print("extrayendo tabla tbl_inversion_educacion...")
    tbl_inversion_educacion = wb.data.DataFrame('SE.XPD.TOTL.GD.ZS',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_inversion_educacion.drop(["time","Country"], axis=1, inplace=True)
    tbl_inversion_educacion.columns = ["id_pais", "year", " inversion_educacion"]
    tbl_inversion_educacion.to_csv('Extraccion/tbl_inversion_educacion.csv', index = False)

    #tbl_emisiones_c02  8
    print("extrayendo tabla tbl_emisiones_co2...")
    tbl_emisiones_co2 = wb.data.DataFrame('EN.ATM.CO2E.PC',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_emisiones_co2.drop(["time","Country"], axis=1, inplace=True)
    tbl_emisiones_co2.columns = ["id_pais", "year", "emisiones_co2"]
    tbl_emisiones_co2.to_csv('Extraccion/tbl_emisiones_co2.csv', index = False)


    #tbl_srv_sanit_bas  9
    print("extrayendo tabla tbl_srv_sanit_bas...")
    tbl_srv_sanit_bas = wb.data.DataFrame('SH.STA.BASS.ZS',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_srv_sanit_bas.drop(["time","Country"], axis=1, inplace=True)
    tbl_srv_sanit_bas.columns = ["id_pais", "year", " srv_sanit_bas"]
    tbl_srv_sanit_bas.to_csv('Extraccion/tbl_srv_sanit_bas.csv', index = False)

    #tbl_acceso_electricidad  10
    print("extrayendo tabla tbl_acceso_electricidad...")
    tbl_acceso_electricidad = wb.data.DataFrame('EG.ELC.ACCS.ZS',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_acceso_electricidad.drop(["time","Country"], axis=1, inplace=True)
    tbl_acceso_electricidad.columns = ["id_pais", "year", " acceso_electricidad"]
    tbl_acceso_electricidad.to_csv('Extraccion/tbl_acceso_electricidad.csv', index = False)

    #tbl_camas_hospitales  11
    print("extrayendo tabla tbl_camas_hospitales...")
    tbl_camas_hospitales = wb.data.DataFrame('SH.MED.BEDS.ZS',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_camas_hospitales.drop(["time","Country"], axis=1, inplace=True)
    tbl_camas_hospitales.columns = ["id_pais", "year", "camas_hospitales"]
    tbl_camas_hospitales.to_csv('Extraccion/tbl_camas_hospitales.csv', index = False)

    #tbl_densidad_poblacion  12
    print("extrayendo tabla tbl_densidad_poblacional...")
    tbl_densidad_poblacional = wb.data.DataFrame('EN.POP.DNST',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_densidad_poblacional.drop(["time","Country"], axis=1, inplace=True)
    tbl_densidad_poblacional.columns = ["id_pais", "year", "densidad_poblacion"]
    tbl_densidad_poblacional.to_csv('Extraccion/tbl_densidad_poblacional.csv', index = False)

    #tbl_produccion_alimentos  13
    print("extrayendo tabla tbl_produccion_alimentos...")
    tbl_produccion_alimentos = wb.data.DataFrame('AG.PRD.FOOD.XD',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_produccion_alimentos.drop(["time","Country"], axis=1, inplace=True)
    tbl_produccion_alimentos.columns = ["id_pais", "year", "produccion_alimentos"]
    tbl_produccion_alimentos.to_csv('Extraccion/tbl_produccion_alimentos.csv', index = False)

    #tbl_pib  14
    print("extrayendo tabla tbl_pib...")
    tbl_pib = wb.data.DataFrame('NY.GDP.MKTP.CD',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_pib.drop(["time","Country"], axis=1, inplace=True)
    tbl_pib.columns = ["id_pais", "year", "pib"]
    tbl_pib.to_csv('Extraccion/tbl_pib.csv', index = False)

    #tbl_gini  15
    print("extrayendo tabla tbl_gini...")
    tbl_gini = wb.data.DataFrame('SI.POV.GINI',paises, range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_gini.drop(["time","Country"], axis=1, inplace=True)
    tbl_gini.columns = ["id_pais", "year", "gini"]
    tbl_gini.to_csv('Extraccion/tbl_gini.csv', index = False)

    #tbl_acceso_agua_potable 16
    print("extrayendo tabla tbl_acceso_agua_potable...")
    tbl_acceso_agua_potable = wb.data.DataFrame('ER.H2O.INTR.PC',paises, range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_acceso_agua_potable.drop(["time","Country"], axis=1, inplace=True)
    tbl_acceso_agua_potable.columns = ["id_pais", "year", "agua"]
    tbl_acceso_agua_potable.to_csv('Extraccion/tbl_acceso_agua_potable.csv', index = False)

    #tbl_agotamiento_recursos_naturales 17
    print("extrayendo tabla tbl_agotamiento_recursos_naturales...")
    tbl_agotamiento_recursos_naturales = wb.data.DataFrame('NY.ADJ.DRES.GN.ZS',paises, range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_agotamiento_recursos_naturales.drop(["time","Country"], axis=1, inplace=True)
    tbl_agotamiento_recursos_naturales.columns = ["id_pais", "year", "agotamiento_recursos"]
    tbl_agotamiento_recursos_naturales.to_csv('Extraccion/tbl_agotamiento_recursos_naturales.csv', index = False)

    #tbl_renta_recursos_naturales 18
    print("extrayendo tabla tbl_renta_recursos_naturales...")
    tbl_renta_recursos_naturales = wb.data.DataFrame('NY.GDP.TOTL.RT.ZS',paises, range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_renta_recursos_naturales.drop(["time","Country"], axis=1, inplace=True)
    tbl_renta_recursos_naturales.columns = ["id_pais", "year", "renta_recursos"]
    tbl_renta_recursos_naturales.to_csv('Extraccion/tbl_renta_recursos_naturales.csv', index = False)

    #tbl_valor_industria 19
    print("extrayendo tabla tbl_valor_industria...")
    tbl_valor_industria = wb.data.DataFrame('NV.IND.TOTL.ZS',paises, range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_valor_industria.drop(["time","Country"], axis=1, inplace=True)
    tbl_valor_industria.columns = ["id_pais", "year", "industria"]
    tbl_valor_industria.to_csv('Extraccion/tbl_valor_industria.csv', index = False)

    #tbl_consumo_tabaco 21
    print("extrayendo tabla tbl_consumo_tabaco...")
    tbl_consumo_tabaco = wb.data.DataFrame('SH.PRV.SMOK',paises, time =range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_consumo_tabaco.drop(["time","Country"], axis=1, inplace=True)
    tbl_consumo_tabaco.columns = ["id_pais", "year", "tabaco"]
    tbl_consumo_tabaco.to_csv('Extraccion/tbl_consumo_tabaco.csv', index = False)

    #tbl_desempleo_fl 22 fl=fuerza laboral
    print("extrayendo tabla tbl_desempleo_fl...")
    tbl_desempleo_fl = wb.data.DataFrame('SL.UEM.TOTL.ZS',paises, time =range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_desempleo_fl.drop(["time","Country"], axis=1, inplace=True)
    tbl_desempleo_fl.columns = ["id_pais", "year", "desempleo"]
    tbl_desempleo_fl.to_csv('Extraccion/tbl_desempleo_fl.csv', index = False)

    #tbl_inversion_salud  23
    print("extrayendo tabla tbl_inversion_salud...")
    tbl_inversion_salud = wb.data.DataFrame('SH.XPD.CHEX.GD.ZS',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_inversion_salud.drop(["time","Country"], axis=1, inplace=True)
    tbl_inversion_salud.columns = ["id_pais", "year", "salud"]
    tbl_inversion_salud.to_csv('Extraccion/tbl_inversion_salud.csv', index = False)

    # tbl_inversion_desarrollo 24
    print("extrayendo tabla tbl_inversion_desarrollo...")
    tbl_inversion_desarrollo = wb.data.DataFrame('GB.XPD.RSDV.GD.ZS',paises, time = range(2000, 2021), 
                    columns = "series", numericTimeKeys=True, labels=True).reset_index()
    tbl_inversion_desarrollo.drop(["time","Country"], axis=1, inplace=True)
    tbl_inversion_desarrollo.columns = ["id_pais", "year", "desarrollo"]
    tbl_inversion_desarrollo.to_csv('Extraccion/tbl_inversion_desarrollo.csv', index = False)


    #tbl_anios_medios_escolaridad
    print("extrayendo tabla tbl_anios_medios_escolaridad...")
    df = pd.read_csv('Datasets/Mean-Years-Schooling.csv', sep=';')
    df.drop(columns=['Country'], inplace=True)
    df_unpivot = pd.melt(df, id_vars='ISO_Code', value_vars= df.columns[1:])
    df_unpivot.columns = ['id_pais','year','anios_escolares']
    df_unpivot.sort_values(by='year')
    df_unpivot.to_csv('Extraccion/tbl_anios_medios_escolaridad.csv', index = False)

    #tbl_consumo_alcohol_pc
    print("extrayendo tabla tbl_consumo_alcohol_pc...")
    tbl_consumo_alcohol_pc = pd.read_csv('Datasets/Alcohol2.csv')
    tbl_consumo_alcohol_pc.to_csv('Extraccion/tbl_consumo_alcohol_pc.csv', index = False)

    #tbl_obesidad
    print("extrayendo tabla tbl_obesidad...")
    tbl_obesidad = pd.read_csv('Datasets/Obesidad.csv')
    tbl_obesidad.to_csv('Extraccion/tbl_obesidad.csv', index = False)
