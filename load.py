import pandas as pd
import psycopg2
import os

def carga():

    conn = psycopg2.connect(
        host = "proyecto-final-henry.ctv6lgil6x7r.us-east-1.rds.amazonaws.com",
        port = 5432,
        user = "postgres",
        password = "lorussoasoc",
        database = "lorussoasoc"
    )
    
    conn.autocommit = True
    print("Seleccione la carpeta donde se encuentran los archivos limpios")
    
    directorio = input()
    carpeta = directorio 
    lista = []
    for file in os.listdir(carpeta):
        if file.endswith('.csv'):
            lista.append(file)
    lista = sorted(lista)
    
    csv_paises = carpeta + "\\tbl_paises.csv"
    csv_esperanza_vida = carpeta + "\\tbl_esperanza_vida.csv"
    csv_poblacion = carpeta + "\\tbl_poblacion.csv"
    csv_alfabetizacion =carpeta + "\\tbl_alfabetizacion_porc.csv"
    csv_escolaridad = carpeta + "\\tbl_anios_medios_escolaridad.csv"
    csv_fuerza_laboral = carpeta + "\\tbl_fuerza_laboral.csv"
    csv_desempleo = carpeta + "\\tbl_desempleo_fl.csv"
    csv_ingreso_medio = carpeta + "\\tbl_ingreso_medio_pc.csv"
    csv_alcohol = carpeta + "\\tbl_consumo_alcohol_pc.csv"
    csv_tabaco = carpeta + "\\tbl_consumo_tabaco.csv"
    csv_obesidad = carpeta + "\\tbl_obesidad.csv"
    csv_srv_sanit_bas =carpeta + "\\tbl_srv_sanit_bas.csv"
    csv_acceso_electricidad = carpeta + "\\tbl_acceso_electricidad.csv"
    csv_camas = carpeta + "\\tbl_camas_hospitales.csv"
    csv_densidad_poblacional = carpeta + "\\tbl_densidad_poblacional.csv"
    csv_contaminacion = carpeta + "\\tbl_contaminacion_aire.csv"
    csv_co2 =carpeta + "\\tbl_emisiones_co2.csv"
    csv_acceso_agua = carpeta + "\\tbl_acceso_agua_potable.csv"
    csv_produccion_alimentos = carpeta + "\\tbl_produccion_alimentos.csv"
    csv_agotamiento_recursos = carpeta + "\\tbl_agotamiento_recursos_naturales.csv"
    csv_renta_recursos = carpeta + "\\tbl_renta_recursos_naturales.csv"
    csv_industria = carpeta + "\\tbl_valor_industria.csv"
    csv_pib = carpeta + "\\tbl_pib.csv"
    csv_inversion_desarrollo = carpeta + "\\tbl_inversion_desarrollo.csv"
    csv_inversion_salud = carpeta + "\\tbl_inversion_salud.csv"
    csv_inversion_educacion = carpeta + "\\tbl_inversion_educacion.csv"
    csv_gini = carpeta + "\\tbl_gini.csv"

    print("-------------------")
    print("Iniciando carga de datos...")
    print("-------------------")

    query_paises = """DROP TABLE IF EXISTS tbl_paises;
        CREATE TABLE IF NOT EXISTS tbl_paises ( 
            id_pais VARCHAR(3), 
            pais VARCHAR(255),
            longitude FLOAT,
            latitude FLOAT,
            incomeLevel VARCHAR(5),
            capitalCity VARCHAR(255),
            PRIMARY KEY (id_pais)
        );
        COPY tbl_paises(id_pais, pais,longitude,latitude,incomeLevel,capitalCity)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;

    """
    cursor = conn.cursor()
    print("cargando tbl_paises...")
    cursor.copy_expert(query_paises, open(csv_paises, "r"))
    print("tbl_paises cargada")

    query_esperanza_vida = """
        DROP TABLE IF EXISTS tbl_esperanza_vida;
        CREATE TABLE IF NOT EXISTS tbl_esperanza_vida(
            year INTEGER,
            id_pais VARCHAR(3),
            edvan FLOAT
        );
        COPY tbl_esperanza_vida( year, id_pais, edvan)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_esperanza_vida...")
    cursor.copy_expert(query_esperanza_vida, open(csv_esperanza_vida, "r"))
    print("tbl_esperanza_vida cargada")


    query_poblacion = """
        DROP TABLE IF EXISTS tbl_poblacion;
        CREATE TABLE IF NOT EXISTS tbl_poblacion(
            id_pais VARCHAR(3),
            year INTEGER,
            poblacion FLOAT
        );
        COPY tbl_poblacion(id_pais, year, poblacion)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_poblacion...")
    cursor.copy_expert(query_poblacion, open(csv_poblacion, "r"))
    print("tbl_poblacion cargada")

    query_alfabetizacion_porc = """
        DROP TABLE IF EXISTS tbl_alfabetizacion_porc;
        CREATE TABLE IF NOT EXISTS tbl_alfabetizacion_porc(
            id_pais VARCHAR(3),
            year INTEGER,
            alfabetizacion FLOAT
        );
        COPY tbl_alfabetizacion_porc(id_pais, year, alfabetizacion)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_alfabetizacion_porc...")
    cursor.copy_expert(query_alfabetizacion_porc, open(csv_alfabetizacion, "r"))
    print("tbl_alfabetizacion_porc cargada")



    query_anios_escolaridad = """
        DROP TABLE IF EXISTS tbl_anios_medios_escolaridad;
        CREATE TABLE IF NOT EXISTS tbl_anios_medios_escolaridad(
            id_pais VARCHAR(3),
            year INTEGER,
            anios_escolares FLOAT
        );
        COPY tbl_anios_medios_escolaridad(id_pais, year, anios_escolares)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_anios_medios_escolaridad...")
    cursor.copy_expert(query_anios_escolaridad, open(csv_escolaridad, "r"))
    print("tbl_anios_medios_escolaridad cargada")

    query_fuerza_laboral = """
        DROP TABLE IF EXISTS tbl_fuerza_laboral;
        CREATE TABLE IF NOT EXISTS tbl_fuerza_laboral(
            id_pais VARCHAR(3),
            year INTEGER,
            fuerza_laboral FLOAT
        );
        COPY tbl_fuerza_laboral(id_pais, year, fuerza_laboral)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_fuerza_laboral...")
    cursor.copy_expert(query_fuerza_laboral, open(csv_fuerza_laboral, "r"))
    print("tbl_fuerza_laboral cargada")

    query_desempleo = """
        DROP TABLE IF EXISTS tbl_desempleo_fl;
        CREATE TABLE IF NOT EXISTS tbl_desempleo_fl(
            id_pais VARCHAR(3),
            year INTEGER,
            desempleo FLOAT
        );
        COPY tbl_desempleo_fl(id_pais, year, desempleo)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_desempleo_fl...")
    cursor.copy_expert(query_desempleo, open(csv_desempleo, "r"))
    print("tbl_desempleo_fl cargada")

    query_ingreso_medio_pc = """
        DROP TABLE IF EXISTS tbl_ingreso_medio_pc;
        CREATE TABLE IF NOT EXISTS tbl_ingreso_medio_pc(
            id_pais VARCHAR(3),
            year INTEGER,
            ingreso_medio_pc FLOAT
        );
        COPY tbl_ingreso_medio_pc(id_pais, year, ingreso_medio_pc)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_ingreso_medio_pc...")
    cursor.copy_expert(query_ingreso_medio_pc, open(csv_ingreso_medio, "r"))
    print("tbl_ingreso_medio_pc cargada")

    query_alcohol = """
        DROP TABLE IF EXISTS tbl_consumo_alcohol;
        CREATE TABLE IF NOT EXISTS tbl_consumo_alcohol(
            year INTEGER,
            id_pais VARCHAR(3),
            alcohol FLOAT
        );
        COPY  tbl_consumo_alcohol(year, id_pais, alcohol)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_consumo_alcohol...")
    cursor.copy_expert(query_alcohol, open(csv_alcohol, "r"))
    print("tbl_consumo_alcohol cargada")

    
    query_tabaco = """
        DROP TABLE IF EXISTS tbl_consumo_tabaco;
        CREATE TABLE IF NOT EXISTS tbl_consumo_tabaco(
            id_pais VARCHAR(3),
            year INTEGER,
            tabaco FLOAT
        );
        COPY  tbl_consumo_tabaco(id_pais, year, tabaco)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_consumo_tabaco...")
    cursor.copy_expert(query_tabaco, open(csv_tabaco, "r"))
    print("tbl_consumo_tabaco cargada")
    
    

    query_obesidad = """
        DROP TABLE IF EXISTS tbl_obesidad;
        CREATE TABLE IF NOT EXISTS tbl_obesidad(
            year INTEGER,
            id_pais VARCHAR(3),
            obesidad FLOAT
        );
        COPY tbl_obesidad(year, id_pais, obesidad)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_obesidad...")
    cursor.copy_expert(query_obesidad, open(csv_obesidad, "r"))
    print("tbl_obesidad cargada")

    query_srv_sanit_bas = """
        DROP TABLE IF EXISTS tbl_srv_sanit_bas;
        CREATE TABLE IF NOT EXISTS tbl_srv_sanit_bas(
            id_pais VARCHAR(3),
            year INTEGER,
            srv_sanit_bas FLOAT
        );
        COPY tbl_srv_sanit_bas(id_pais, year, srv_sanit_bas)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_srv_sanit_bas...")
    cursor.copy_expert(query_srv_sanit_bas, open(csv_srv_sanit_bas, "r"))
    print("tbl_srv_sanit_bas cargada")

    query_acceso_electricidad = """
        DROP TABLE IF EXISTS tbl_acceso_electricidad;
        CREATE TABLE IF NOT EXISTS tbl_acceso_electricidad(
            id_pais VARCHAR(3),
            year INTEGER,
            acceso_electricidad FLOAT
        );
        COPY tbl_acceso_electricidad(id_pais, year, acceso_electricidad)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_acceso_electricidad...")
    cursor.copy_expert(query_acceso_electricidad, open(csv_acceso_electricidad, "r"))
    print("tbl_acceso_electricidad cargada")

    query_camas_hospitales = """
        DROP TABLE IF EXISTS tbl_camas_hospitales;
        CREATE TABLE IF NOT EXISTS tbl_camas_hospitales(
            id_pais VARCHAR(3),
            year INTEGER,
            camas_hospitales FLOAT
        );
        COPY tbl_camas_hospitales(id_pais, year, camas_hospitales)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """
    cursor = conn.cursor()
    print("cargando tbl_camas_hospitales...")
    cursor.copy_expert(query_camas_hospitales, open(csv_camas, "r"))
    print("tbl_camas_hospitales cargada")

    query_densidad_poblacion = """
        DROP TABLE IF EXISTS tbl_densidad_poblacion;
        CREATE TABLE IF NOT EXISTS tbl_densidad_poblacion(
            id_pais VARCHAR(3),
            year INTEGER,
            densidad_poblacion FLOAT
        );
        COPY tbl_densidad_poblacion(id_pais, year, densidad_poblacion)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_densidad_poblacion...")
    cursor.copy_expert(query_densidad_poblacion, open(csv_densidad_poblacional, "r"))
    print("tbl_densidad_poblacion cargada")

    
    query_contaminacion_aire= """
        DROP TABLE IF EXISTS tbl_contaminacion_aire;
        CREATE TABLE IF NOT EXISTS tbl_contaminacion_aire(
            id_pais VARCHAR(3),
            year INTEGER,
            contaminacion_aire FLOAT
        );
        COPY tbl_contaminacion_aire(id_pais, year, contaminacion_aire)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_contaminacion_aire...")
    cursor.copy_expert(query_contaminacion_aire, open(csv_contaminacion, "r"))
    print("tbl_contaminacion_aire cargada")
    

    query_emisiones_c02 = """
        DROP TABLE IF EXISTS tbl_emisiones_co2;
        CREATE TABLE IF NOT EXISTS tbl_emisiones_co2(
            id_pais VARCHAR(3),
            year INTEGER,
            emisiones_co2 FLOAT
        );
        COPY tbl_emisiones_co2(id_pais, year, emisiones_co2)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_emisiones_co2...")
    cursor.copy_expert(query_emisiones_c02, open(csv_co2, "r"))
    print("tbl_emisiones_co2 cargada")

    query_agua = """
        DROP TABLE IF EXISTS tbl_acceso_agua_potable;
        CREATE TABLE IF NOT EXISTS tbl_acceso_agua_potable(
            id_pais VARCHAR(3),
            year INTEGER,
            agua FLOAT
        );
        COPY  tbl_acceso_agua_potable(id_pais, year, agua)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_acceso_agua_potable...")
    cursor.copy_expert(query_agua, open(csv_acceso_agua, "r"))
    print("tbl_acceso_agua_potable cargada")

    query_produccion_alimentos = """
        DROP TABLE IF EXISTS tbl_produccion_alimentos;
        CREATE TABLE IF NOT EXISTS tbl_produccion_alimentos(
            id_pais VARCHAR(3),
            year INTEGER,
            produccion_alimentos FLOAT
        );
        COPY tbl_produccion_alimentos(id_pais, year, produccion_alimentos)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_produccion_alimentos...")
    cursor.copy_expert(query_produccion_alimentos, open(csv_produccion_alimentos, "r"))
    print("tbl_produccion_alimentos cargada")

    query_agotamiento_recursos = """
        DROP TABLE IF EXISTS tbl_agotamiento_recursos_naturales;
        CREATE TABLE IF NOT EXISTS tbl_agotamiento_recursos_naturales(
            id_pais VARCHAR(3),
            year INTEGER,
            agotamiento_recursos FLOAT
        );
        COPY  tbl_agotamiento_recursos_naturales(id_pais, year, agotamiento_recursos)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_agotamiento_recursos_naturales...")
    cursor.copy_expert(query_agotamiento_recursos, open(csv_agotamiento_recursos, "r"))
    print("tbl_agotamiento_recursos_naturales cargada")

    query_renta_recursos = """
        DROP TABLE IF EXISTS tbl_renta_recursos_naturales;
        CREATE TABLE IF NOT EXISTS tbl_renta_recursos_naturales(
            id_pais VARCHAR(3),
            year INTEGER,
            renta_recursos FLOAT
        );
        COPY  tbl_renta_recursos_naturales(id_pais, year, renta_recursos)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_renta_recursos_naturales...")
    cursor.copy_expert(query_renta_recursos, open(csv_renta_recursos, "r"))
    print("tbl_renta_recursos_naturales cargada")

    query_industria = """
        DROP TABLE IF EXISTS tbl_valor_industria;
        CREATE TABLE IF NOT EXISTS tbl_valor_industria(
            id_pais VARCHAR(3),
            year INTEGER,
            industria FLOAT
        );
        COPY  tbl_valor_industria(id_pais, year, industria)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_valor_industria...")
    cursor.copy_expert(query_industria, open(csv_industria, "r"))
    print("tbl_valor_industria cargada")

    query_pib = """
        DROP TABLE IF EXISTS tbl_pib;
        CREATE TABLE IF NOT EXISTS tbl_pib(
            id_pais VARCHAR(3),
            year INTEGER,
            pib FLOAT
        );
        COPY tbl_pib(id_pais, year, pib)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_pib...")
    cursor.copy_expert(query_pib, open(csv_pib, "r"))
    print("tbl_pib cargada")

    query_desarrollo = """
        DROP TABLE IF EXISTS tbl_inversion_desarrollo;
        CREATE TABLE IF NOT EXISTS tbl_inversion_desarrollo(
            id_pais VARCHAR(3),
            year INTEGER,
            desarrollo FLOAT
        );
        COPY tbl_inversion_desarrollo(id_pais, Year, desarrollo)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_inversion_desarrollo...")
    cursor.copy_expert(query_desarrollo, open(csv_inversion_desarrollo, "r"))
    print("tbl_inversion_desarrollo cargada")

    query_salud = """
        DROP TABLE IF EXISTS tbl_inversion_salud;
        CREATE TABLE IF NOT EXISTS tbl_inversion_salud(
            id_pais VARCHAR(3),
            year INTEGER,
            salud FLOAT
        );
        COPY tbl_inversion_salud(id_pais, year, salud)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_inversion_salud...")
    cursor.copy_expert(query_salud, open(csv_inversion_salud, "r"))
    print("tbl_inversion_salud cargada")


    query_inversion_educacion = """
        DROP TABLE IF EXISTS tbl_inversion_educacion;
        CREATE TABLE IF NOT EXISTS tbl_inversion_educacion(
            id_pais VARCHAR(3),
            year INTEGER,
            inversion_educacion FLOAT
        );
        COPY tbl_inversion_educacion(id_pais, year, inversion_educacion)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER; 
    """ 
    cursor = conn.cursor()
    print("cargando tbl_inversion_educacion...")
    cursor.copy_expert(query_inversion_educacion, open(csv_inversion_educacion, "r"))
    print("tbl_inversion_educacion cargada")

    query_gini = """
        DROP TABLE IF EXISTS tbl_gini;
        CREATE TABLE IF NOT EXISTS tbl_gini(
            id_pais VARCHAR(3),
            year INTEGER,
            gini FLOAT
        );
        COPY  tbl_gini(id_pais, year, gini)
        FROM STDIN 
        DELIMITER ',' 
        CSV HEADER;
    """ 
    cursor = conn.cursor()
    print("cargando tbl_gini...")
    cursor.copy_expert(query_gini, open(csv_gini, "r"))
    print("tbl_gini cargada")
    print("-------------------")
    print("-------------------")
    print("tablas cargadas a BD")
    conn.close()
carga()