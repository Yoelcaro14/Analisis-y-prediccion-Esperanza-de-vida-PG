# Area de trabajo
# pip install --quiet wbgapi
from gettext import install
import matplotlib.pyplot as plt
from requests import options
import wbgapi as wb
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import folium 
from streamlit_folium import st_folium
from PIL import Image
from streamlit_option_menu import option_menu
import seaborn as sns
import re
from indices import *
# from predicciones_kpi import *

# WEB

def display_map(df,year,pais):

    if pais != 'All':
        df= df[(df['ANIO'] == year )& (df['NOMBRE PAIS'] == pais)]
    else: 
        df= df[(df['ANIO'] == year )]

    map= folium.Map ( location=[30,-86],zoom_start=2, 
                    scrollWheelZoom= False, tiles= 'CartoDB positron')
    choropleth = folium.Choropleth( geo_data ='world-administrative-boundaries.geojson',
                                    data=df,
                                    columns=( 'NOMBRE PAIS','ESPERANZA'),
                                    key_on='feature.properties.name',
                                    line_opacity=0.8,
                                    highlight=True,
                                    fill_color ='YlOrRd', 
                                    fill_opacity = 0.7,
                                    legend_name="ESPERANZA"
                                    
    )
   
    choropleth.geojson.add_to(map)

    df = df.set_index('NOMBRE PAIS')
    # nombre_pais='Argentina'

    for feature in choropleth.geojson.data['features']:
        nombre_pais = feature['properties']['name']
        feature['properties']['Indicador'] = 'Indice:' + str('{:,}'.format(df.loc[nombre_pais,'ESPERANZA']) if nombre_pais in list(df.index) else 'N/A')  
    choropleth.geojson.add_child( folium.features.GeoJsonTooltip(['name','Indicador'],labels=False ) )
    st_map = st_folium(map, width=530,height=600)
    return st_map

# Display - FILTROS

def display_time(df):
    year_list= list(df['ANIO'].unique())
    year_list.sort()
    year= st.selectbox('AÑO',year_list, len(year_list)-1)
    return year

def display_ingresos(df):#,country_name):
    # if pais!='All':
        # ingresos_list= ['All']
    # else: 
        ingresos_list= ['All','LIC', 'LMC','UMC','HIC']
        # ingresos_list= ['All','LIC : País de ingresos bajos', 'LMC : País de ingresos medios bajos','UMC : País de ingresos medios altos','HIC : País de ingresos altos']

        ingresos_list.sort()
        # pais_index=ingresos_list.index(country_name) if country_name and country_name in ingresos_list else 0
        ingresos= st.radio('Seleccionar Nivel de Ingresos :',ingresos_list,horizontal=False)#, pais_index)
        return ingresos

def display_countrie(df,country_name,ingresos):
    if ingresos=='All':
        pais_list= ['All'] +list(df['NOMBRE PAIS'].unique())
    if ingresos!='All':
        pais_list= ['All'] +list(df[df['NIVEL INGRESOS']==f'{ingresos}']['NOMBRE PAIS'].unique())

    pais_list.sort(reverse=False)
    pais_index=pais_list.index(country_name) if country_name and country_name in pais_list else 0
    pais= st.selectbox('Seleccionar Pais :',pais_list, pais_index)

    return pais

def display_iso():

    paises.sort(reverse=False)
    iso_list= ['Ninguno'] + paises

    # iso_list.sort(reverse=False)
    # pais_index=iso_list.index(country_name) if country_name and country_name in iso_list else 0
    iso= st.selectbox('Seleccionar Iso Pais :',iso_list)

    return iso
# Display - TABLAS

def display_tables(df,year,pais,ingresos):
    if (pais == 'All') and (ingresos=='All'):
        df = df[(df['ANIO'] == year )]
    if ingresos != 'All':
        df = df[df['NIVEL INGRESOS']==f'{ingresos}']
    if pais != 'All': 
        df= df[(df['ANIO'] == year )& (df['NOMBRE PAIS'] == pais)]
    
        
    paises_list = df.drop(['PAIS','ANIO','NIVEL INGRESOS'],axis=1)
    paises_list=paises_list.rename({'ESPERANZA': 'ESPRNZA.VIDA'}, axis=1)
    paises_list = paises_list.sort_values(by='ESPRNZA.VIDA',ascending=False).reset_index(drop=True)
    # paises_list= paises_list.style.hide_index()
    paises_list=paises_list.set_index('NOMBRE PAIS',)
    paises_list.columns.name ='Pais'
    
    return paises_list


# Display - GRAFICOS

def display_grafico_educacion(df,pais):
    df = df[df["NOMBRE PAIS"] == pais]
    x = df["ANIO"]
    y1 = df["ED.INDEX"]
    y2 = df["ESPERANZA"]

    fig = plt.figure(figsize=(12,6))
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    ax1 = fig.add_subplot(111)
    ax1.plot(x, y1, color = "green", linewidth = 2, label = "Indice de Educacion")
    ax1.set_ylabel("Indice de Educacion")
    ax1.set_title("Indice de educación y Esperanza de vida")
    
    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(x, y2, color = "red", linewidth = 2, label = "Esperanza de vida")
    ax2.set_ylabel( "Indice de Esperanza de vida")

    plt.xticks(range(df["ANIO"].min(),df["ANIO"].max()+1,1))
    fig.legend(loc='upper left', facecolor='w', bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)
    plt.show()
    return fig 

def display_grafico_trabajo(df,pais):

    df = df[df["NOMBRE PAIS"] == pais]
    x = df["ANIO"]
    y1 = df["TRAB.INDEX"]
    y2 = df["ESPERANZA"]

    fig = plt.figure(figsize=(12,6))
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    ax1 = fig.add_subplot(111)
    ax1.plot(x, y1, color = "green", linewidth = 2, label = "Indice de Trabajo")
    ax1.set_ylabel("Indice de Trabajo")
    ax1.set_title("Indice de Trabajo y Esperanza de vida")
    
    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(x, y2, color = "red", linewidth = 2, label = "Esperanza de vida")
    ax2.set_ylabel( "Indice de Esperanza de vida")

    plt.xticks(range(df["ANIO"].min(),df["ANIO"].max()+1,1))
    fig.legend(loc='upper left', facecolor='w', bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)
    plt.show()

    return fig 

def display_grafico_recursos(df,pais):

    df = df[df["NOMBRE PAIS"] == pais]
    x = df["ANIO"]
    y1 = df["ESTADO.INDEX"]
    y2 = df["ESPERANZA"]

    fig = plt.figure(figsize=(12,6))
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    ax1 = fig.add_subplot(111)
    ax1.plot(x, y1, color = "green", linewidth = 2, label = "Indice de Recursos y Estado")
    ax1.set_ylabel("Indice de Recursos y Estado")
    ax1.set_title("Indice de Recursos y Estado y Esperanza de vida")
    
    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(x, y2, color = "red", linewidth = 2, label = "Esperanza de vida")
    ax2.set_ylabel( "Indice de Esperanza de vida")

    plt.xticks(range(df["ANIO"].min(),df["ANIO"].max()+1,1))
    fig.legend(loc='upper left', facecolor='w', bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)
    plt.show()

    return fig 

def display_grafico_medio(df,pais):

    df = df[df["NOMBRE PAIS"] == pais]
    x = df["ANIO"]
    y1 = df["AMB.INDEX"]
    y2 = df["ESPERANZA"]

    fig = plt.figure(figsize=(12,6))
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    ax1 = fig.add_subplot(111)
    ax1.plot(x, y1, color = "green", linewidth = 2, label = "Indice de Medio Ambiente")
    ax1.set_ylabel("Indice de Medio Ambiente")
    ax1.set_title("Indice de Medio Ambiente y Esperanza de vida")
    
    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(x, y2, color = "red", linewidth = 2, label = "Esperanza de vida")
    ax2.set_ylabel( "Indice de Esperanza de vida")

    plt.xticks(range(df["ANIO"].min(),df["ANIO"].max()+1,1))
    fig.legend(loc='upper left', facecolor='w', bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)
    plt.show()

    return fig 

def display_grafico_nivel(df,pais):

    df = df[df["NOMBRE PAIS"] == pais]
    x = df["ANIO"]
    y1 = df["IND.N.VIDA"]
    y2 = df["ESPERANZA"]

    fig = plt.figure(figsize=(12,6))
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    ax1 = fig.add_subplot(111)
    ax1.plot(x, y1, color = "green", linewidth = 2, label = "Indice de Medio Ambiente")
    ax1.set_ylabel("Indice de Nivel de Vida")
    ax1.set_title("Indice de Nivel de Vida y Esperanza de vida")
    
    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(x, y2, color = "red", linewidth = 2, label = "Esperanza de vida")
    ax2.set_ylabel( "Indice de Esperanza de vida")

    plt.xticks(range(df["ANIO"].min(),df["ANIO"].max()+1,1))
    fig.legend(loc='upper left', facecolor='w', bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)
    plt.show()

    return fig 

def display_grafico_ML(df,pais_iso):
    #KPI 4: Valores buenos COL USA CRI SLV HND JAM PAN PER VCT SUR
    
    df = df[df["id_pais"] == pais_iso]
    x = df["ds"]
    y1 = df["pred_neutro"]
    y2 = df["ESPERANZA"]

    fig = plt.figure(figsize=(12,6))
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    ax1 = fig.add_subplot(111)
    ax1.plot(x, y1, color = "red", linewidth = 2, label = "Esperanza de vida Proyectada")
    ax1.set_ylabel("Esperanza de vida")
    ax1.set_title("Indice de Esperanza de vida real y proyectada")

    # ax2 = ax1.twinx()  # this is the important function
    ax1.plot(x, y2, color = "green", linewidth = 2, label = "Esperanza de vida real")
    ax1.set_ylabel( "Esperanza de vida proyectada")

    plt.xticks(range(df["ds"].min(),df["ds"].max()+1,1))
    fig.legend(loc='upper left', facecolor='w', bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)
    plt.show()
    return fig 

# Display - Metricas

def display_corr(df,pais,metric_title,sub_indice):

    # Formato texto 
    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
    background-color: rgba(28, 131, 225, 0.1); 
    border: 1px solid rgba(28, 131, 225, 0.1);
    padding: 5% 5% 5% 10%;
    border-radius: 10px;
    color: rgb(16, 248, 9);
    # overflow-wrap: break-word;
    }

    /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
    # overflow-wrap: break-word;
    # white-space: break-spaces;
    color: rgb(28, 255, 9);   
    }
    </style>""", unsafe_allow_html=True)
    
    val_corr = df[df["NOMBRE PAIS"] == pais].corr().loc['ESPERANZA'][f'{sub_indice}']
    
    return st.metric(label= metric_title,value='{:,}'.format(round(val_corr,2)))

def display_medias(df,pais,metric_title,sub_indice):
    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
    # background-color: rgba(28, 131, 225, 0.1); 
    # border: 1px solid rgba(28, 131, 225, 0.1);
    # padding: 5% 5% 5% 10%;
    # border-radius: 10px;
    color: rgb(16, 248, 9);
    # overflow-wrap: break-word;
    }

    /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
    # overflow-wrap: break-word;
    # white-space: break-spaces;
    color: rgb(28, 255, 9);   
    }
    </style>""", unsafe_allow_html=True)
    
    val_media = df[df["NOMBRE PAIS"] == pais].mean().loc[f'{sub_indice}']
    return st.metric(metric_title,'{:,}'.format(round(val_media,2)))

def display_kpi(df,kpi_title,pais_iso):
    df= df[df['id_pais']==pais_iso]
    kpi_valor = df.iloc[0,1]

    return st.metric(kpi_title,round(kpi_valor,2))

# Display - DATA

def display_data():
    st.write("---")
    st.header("Sobre la data")
    st.markdown("""
                En cuanto a la data, trabajamos con AWS como prestador de servicio. Se utilizo un motor de base de datos **Postgresql** el cual alojá
                las tablas en una base de datos estrella. Las tablas fueron extraídas de, por ejemplo, el **World Data Bank**, la **OMS** entre otras 
                fuentes.
                """)
    st.markdown("Creamos un Script, mediante el cual extraemos, transformamos y cargamos los datos de manera automatica.")
    st.write("Para mas informacion, ingresar al informe [Aqui](https://docs.google.com/document/d/1jvehToFX1oxlBIWwyT8AS-2mqDl_QnCO/edit)")
    st.write("---")
    st.header("Ranking")
    st.markdown("Veremos a continuacion un ranking de los países en cuanto a los indices elaborados")
    ranking = st.radio("Ranking a mostrar", ("Indice Gini", "Inversiones", "Ingreso Per Capita", "Años Escolaridad", "Desempleo","Contaminacion"), horizontal = True)
    
    if ranking == "Indice Gini":
        df = pd.read_csv("Limpiados/data_completa.csv")
        gini = df[['PAIS','NOMBRE PAIS','ANIO','GINI','ESPERANZA']]
        gini = gini.groupby(["NOMBRE PAIS"]).mean()
        gini= gini.sort_values(by=["GINI"],ascending=False)
        gini = gini.drop(columns = ["ANIO", "ESPERANZA"])
        st.dataframe(gini.head(10), width = 500)
    if ranking == "Inversiones":
        df = pd.read_csv("Limpiados/data_completa.csv")
        recursos_estado = df[['PAIS','NOMBRE PAIS','ANIO','RENTA RECURSOS','INDUSTRIA','PIB','INVERSION SALUD','INVERSION EDUCACION','INVERSION DESARROLLO','GINI','ESPERANZA']]
        recursos_estado.insert(10, "Inversion % PIB", (recursos_estado["INVERSION SALUD"]+recursos_estado["INVERSION DESARROLLO"]+recursos_estado["INVERSION EDUCACION"]))
        recursos_estado = recursos_estado.groupby(["NOMBRE PAIS"]).mean()
        recursos_estado = recursos_estado.sort_values(by=["Inversion % PIB"],ascending = False)
        recursos_estado = recursos_estado.drop(columns = ['ANIO','RENTA RECURSOS','INDUSTRIA','PIB','INVERSION SALUD','INVERSION EDUCACION','INVERSION DESARROLLO','GINI','ESPERANZA'])
        st.dataframe(recursos_estado.head(10), width = 500)
    if ranking == "Ingreso Per Capita":
        df = pd.read_csv("Limpiados/data_completa.csv")
        ingreso_pc = df[['NOMBRE PAIS','INGRESO MEDIO PC']]
        ingreso_pc = ingreso_pc.groupby(["NOMBRE PAIS"]).mean()
        ingreso_pc = ingreso_pc.sort_values(by=["INGRESO MEDIO PC"], ascending=False)
        ingreso_pc = ingreso_pc.rename(columns ={"INGRESO MEDIO PC" : "Ingreso Per Capita"})
        st.dataframe(ingreso_pc.head(10), width = 500)
    if ranking == "Años Escolaridad":
        df = pd.read_csv("Limpiados/data_completa.csv")
        años_escolaridad = df[['NOMBRE PAIS','ANIOS ESCOLARIDAD']]
        años_escolaridad = round(años_escolaridad.groupby(["NOMBRE PAIS"]).mean(),2)
        años_escolaridad = años_escolaridad.sort_values(by=["ANIOS ESCOLARIDAD"], ascending=False)
        años_escolaridad = años_escolaridad.rename(columns ={"ANIOS ESCOLARIDAD" : "Años Escolaridad"})
        st.dataframe(años_escolaridad.head(10), width = 500)
    if ranking == "Desempleo":
        df = pd.read_csv("Limpiados/data_completa.csv")
        desempleo = df[['NOMBRE PAIS','DESEMPLEO']]
        desempleo = round(desempleo.groupby(["NOMBRE PAIS"]).mean(),2)
        desempleo = desempleo.sort_values(by=["DESEMPLEO"], ascending=False)
        desempleo = desempleo.rename(columns ={"DESEMPLEO" : "Desempleo %"})
        st.dataframe(desempleo.head(10), width = 500)
    if ranking == "Contaminacion":
        df = pd.read_csv("Limpiados/data_completa.csv")
        contaminacion = df[['NOMBRE PAIS','CONTAMINACION AIRE']]
        contaminacion = contaminacion.groupby(["NOMBRE PAIS"]).mean()
        contaminacion = contaminacion.sort_values(by=["CONTAMINACION AIRE"], ascending=False)
        contaminacion = contaminacion.rename(columns ={"CONTAMINACION AIRE" : "Contaminacion"})
        st.dataframe(contaminacion.head(10), width = 500)
    st.write("---")
    st.header("Demostración de los datasets")
    st.markdown("A continuación procederemos a mostrarles como es el resultado de la limpieza en una breve demostración.")
    col1,col2 = st.columns(2)
    extraido = False
    transformado = False
    with col1:
        if st.button("Recien Extraido"):
            extraido = True
    with col2:
        if st.button("Transformado"):
            transformado = True
    if extraido:
        df = pd.read_csv("Extraccion/tbl_gini.csv")
        df = df.sample(frac = 1,random_state = 5).reset_index()
        st.dataframe(df.head(), width = 600)
    if transformado:
        df = pd.read_csv("Limpiados/tbl_gini.csv")
        df = df.sample(frac = 1,random_state = 5).reset_index()
        st.dataframe(df.head(), width = 600)
    st.write("---")
    st.markdown("Veremos ahora, algunos de los datasets trabajados.")
    mostrar = st.radio("Dataset :" ,("Mostrar", "Ocultar"), horizontal = True)
    if mostrar == "Mostrar":
        df = pd.read_csv("Limpiados/data_completa.csv")
        df = df.sample(frac = 1,random_state = 5).reset_index()
        df.drop(columns = ["Unnamed: 0"]
        st.dataframe(df.head(20), width = 800)

# Display - ABOUT

def display_about():
    st.write("---")
    st.markdown("# Sobre Nosotros")
    st.markdown("""
                ###### Somos integrantes de la compania Lorusso Asocs. y del grupo 7 de *SoyHenry* de la carrera *Data Science*.
                """)
    st.markdown("###### Los participantes somos Caneva Hugo, Cook Camilo, Carocancha Yoel y Lorusso Nicolas.")
    st.markdown("---")
    st.header("Entendimiento de la situación actual")
    st.markdown(
    '''
        El Departamento de Desarrollo Humano, Educación y Empleo (DHDEE) de la OEA, nos ha contratado 
        con el fin de realizar un estudio y análisis sobre la evolución y progreso de la esperanza de 
        vida en el Continente Americano. Teniendo como objetivo determinar y cuantificar cuáles son los
        factores que inciden sobre la misma, haciendo énfasis en que la educación y el trabajo son los 
        pilares fundamentales para el desarrollo humano y la calidad de vida de los mismos. Por otro lado, 
        se pretende desarrollar un modelo que prediga la esperanza de vida teniendo en cuenta ciertas 
        circunstancias aportadas por un usuario.
    '''     )
    st.write("---")
    st.header("Objetivos")
    st.markdown("""
            Tenemos como objetivo determinar cuales son los factores mas influyentes dentro de la esperanza de vida.
            Extraímos y elaboramos indicadores adecuados, según datos obtenidos de fuentes confiables y seguras.
            Predecimos mediante un modelo de Machine Learning la esperanza de vida de los estados Involucrados
    """
    )
    st.write("---")
    st.header("Nuestra Solución")
    st.markdown(""" 
                Consideramos a la salud del individuo como eje principal y factor fundamental a la hora de estudiar la esperanza de vida del mismo. 
                La salud del individuo no sólo depende de sí mismo, sino también del entorno que lo rodea, el medio ambiente donde éste se desarrolla, 
                y las circunstancias socio-económicas del país o región donde reside. En resumen, podemos decir que la salud depende, en un principio, 
                de dos grandes factores: el Interno o Individual y el Externo o del Entorno como podremos verlo representado a continuacion:
                """)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col2:
        image = Image.open('Imagenes/Individuo.png')
        st.image( image , caption=None, width=350, use_column_width=None, clamp=True, channels="RGB", output_format="auto")
    st.write("Para mas informacion, ingresar al informe [Aqui](https://docs.google.com/document/d/1ziX75piXZ6Z_yS0-zLRovJk0PI4debMV/edit)")
    st.write("---")
    st.subheader("Indices")
    st.markdown(""" Los indices con los cuales trabajamos esta problematica que fueron elaborados por nuestro equipo fueron 5.
                """)
    st.markdown("#### _Indice Trabajo:_") 
    st.markdown("Compuesto por la Fuerza laboral, desempleo, ingreso medio per capita y poblacion de cada estado.")
    st.markdown("#### _Indice Estado:_")
    st.markdown("Compuesto por la inversion en salud, inversion en desarrollo, inversion en educacion, PIB e indice GINI de cada estado.")
    st.markdown("#### _Indice Nivel de Vida:_")
    st.markdown("Compuesto por el consumo de alcohol, consumo de tabajo, servicios sanitarios, acceso a electricidad y disponibilidad de agua de cada estado.")
    st.markdown("#### _Indice medio ambiente:_")
    st.markdown("Compuesto por las emisiones de CO2, contaminacion del aire, disponibilidad al agua, produccion de alimentos y agotamiento de recursos naturales de cada estado.")
    st.markdown("#### _Indice Educación:_")
    st.markdown("Compuesto por alfabetización y años de escolaridad de cada estado.")

# Display - RESULTADOS

def main():

    # ENCABEZADO
    image = Image.open('Imagenes/Logo1.png')
    st.image( image , caption=None, width=250, use_column_width=None, clamp=True, channels="RGB", output_format="auto")
    # st.set_page_config(page_title='Esperanza de Vida') #, page_icon='',  layout='wide')

    st.title('ESPERANZA DE VIDA')
    st.subheader('Analisis de la Esperanza de Vida del Continente Americano')

    # LOAD DATA 
    df_exp_vida = tbl_esperanza_vida_paises
    dfEducacion = educacion 
    dfTrabajo = trabajo
    dfRecursos = ind_estado
    dfMedio = medio_ambiente
    dfNivel = nivel_vida
    dfIngresos = Nivel_Ingresos


    year = 2020
    pais= ''
    country_name = ''
    metric_title= 'Correlación'
   
    # DISPLAY FILTERS AND MAP

    selected = option_menu (
            menu_title = None,
            options=['About','Visual','ML', 'Data'],
            icons=['bookmark-check-fill','bar-chart-fill','bezier','cloud-download-fill'],
            orientation='horizontal',
            styles={"container": {"padding": "0!important", "background-color": "red"},
                    "icon": {"color": "yellow", "font-size": "25px"}, 
                    "nav-link": {"font-size": "25px", "text-align": "center", "margin":"7px", "--hover-color": "orange"},
                    "nav-link-selected": { "margin":"7px","background-color": "black", "color" : "yellow"}}
    )

    if selected == 'About':
        display_about()
        
    if selected == 'Visual':
        
        with st.container():
            st.write("---")
            # Filtros (Año/Pais)
            year = 2020                                        
            left_column, right_column = st.columns([2,1.3],gap="small")
            with left_column:
                ingresos = display_ingresos(dfIngresos)
            with right_column:
                pais = display_countrie(dfIngresos,country_name,ingresos)
            # Mapa / Tabla
            left_column, right_column = st.columns([2,1.3],gap="small")
            with left_column:
                # st.header("Mapa")
                country_name = display_map(df_exp_vida,year,pais)
            with right_column:
                # st.header("Tabla")
                # st.write(display_tables(dfIngresos,year,pais,ingresos).to_html(index=False), unsafe_allow_html=True)
                st.dataframe(display_tables(dfIngresos,year,pais,ingresos),height=600,width=300)

        st.write("---")     

        # Graficos
        if pais != 'All':
            st.header("Esperanza de vida e Indices")
            #(1)
            with st.container():
                st.subheader(f'Indice de Educacion en {pais}')
                st.pyplot(display_grafico_educacion(dfEducacion,pais))
            with st.container():
                st.subheader('Estadísticos')
                col1,col2,col3,col4 = st.columns([1,2,2,2])
                with col1:
                    display_corr(dfEducacion,pais,metric_title,'ED.INDEX')
                with col2:
                    display_medias(dfEducacion,pais,'Media del Ind.Educación','ED.INDEX')
                with col3:
                    display_medias(dfEducacion,pais,'Media de Alfabetización','ALFABETIZACION')
                with col4:
                    display_medias(dfEducacion,pais,'Media de Años Escolaridad','ANIOS ESCOLARIDAD')
                
            #(2)
            with st.container():
                st.write("---")
                st.subheader(f'Indice de Trabajo en {pais}')
                st.pyplot(display_grafico_trabajo(dfTrabajo,pais))            
            with st.container():
                st.subheader('Estadísticos')
                col1,col2,col3,col4 = st.columns([1,1.5,1.5,1.9])
                with col1:
                    display_corr(dfTrabajo,pais,metric_title,'TRAB.INDEX')
                with col2:
                    display_medias(dfTrabajo,pais,'Media del Ind.Trabajo','TRAB.INDEX')              
                with col3:
                    display_medias(dfTrabajo,pais,'Media del Desmpleo','DESEMPLEO')
                # with col4:
                    # display_medias(dfTrabajo,pais,'Media de la Pobl. Activa','FUERZA LABORAL')
            ##(3)  
            with st.container():
                st.write("---")
                st.subheader(f'Indice Estado en {pais}')
                st.pyplot(display_grafico_recursos(dfRecursos,pais))
            with st.container():        
                st.subheader('Estadísticos')
                col1,col2,col3,col4 = st.columns([1.2,1.5,1.5,1.5])
                with col1:
                    display_corr(dfRecursos,pais,metric_title,'ESTADO.INDEX')
                with col2:
                    display_medias(dfRecursos,pais,'Media del Ind.Estado','ESTADO.INDEX')
                with col3:
                    display_medias(dfRecursos,pais,'Media de Inv.Salud','INVERSION SALUD')
                with col4:
                    display_medias(dfRecursos,pais,'Media de Inv.Educación','INVERSION EDUCACION')
            #(4)
            with st.container():
                st.write("---")
                st.subheader(f'Indice Medio Ambiente en {pais}')
                st.pyplot(display_grafico_medio(dfMedio,pais))
            with st.container():
                st.subheader('Estadísticos')
                col1,col2,col3,col4 = st.columns([1,1.5,1.5,1.1])
                with col1:
                    display_corr(dfMedio,pais,metric_title,'AMB.INDEX')
                with col2:
                    display_medias(dfMedio,pais,'Media del Ind.Med.Ambiente','AMB.INDEX')
                with col3:
                    display_medias(dfMedio,pais,'Media del Agot. recursos','AGOTAMIENTO RECURSOS')
                with col4:
                    display_medias(dfMedio,pais,'Media de Emis. CO2','EMISIONES CO2')
            #(5)
            with st.container():
                st.write("---")
                st.subheader(f'Indice Nivel de Vida en {pais}')
                st.pyplot(display_grafico_nivel(dfNivel,pais))
            with st.container():
                st.subheader('Estadísticos')
                col1,col2,col3,col4 = st.columns([1,1.3,1.3,1.3])
                with col1:
                    display_corr(dfNivel,pais,metric_title,'IND.N.VIDA')
                with col2:
                    display_medias(dfNivel,pais,'Media del Ind.Nivel vida','IND.N.VIDA')
                with col3:
                    display_medias(dfNivel,pais,'Media del Cons.Alcohol','CONSUMO ALCOHOL')
                with col4:
                    display_medias(dfNivel,pais,'Media del Cons.Tabaco','CONSUMO TABACO')

    if selected == 'ML':
        st.write("---")                                      
        left_column, right_column = st.columns([1,1],gap="small")
        with left_column:
            # ingresos = display_ingresos(dfIngresos)
            pais_iso = display_iso()
        # with right_column:
            # pais = display_countrie(dfIngresos,country_name,ingresos)
        if  pais_iso != 'Ninguno':
            #(1)
            st.header('Esperanza de vida proyectada al 2025')         
            # st.subheader('Esperanza de vida proyectada al 2025')
            st.pyplot(display_grafico_ML(df_final1,pais_iso))
            
            st.write("---")
    
    if selected == 'Data':
        display_data()   


if __name__=='__main__':
    main()
