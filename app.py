# Area de trabajo
# pip install --quiet wbgapi
from gettext import install
import matplotlib.pyplot as plt
from requests import options
import wbgapi as wb
import pandas as pd
import os
import numpy as np
os.getcwd()
import plotly.express as px
import streamlit as st
import folium 
from streamlit_folium import st_folium
from PIL import Image
from streamlit_option_menu import option_menu
import seaborn as sns
import re

# WEB

def display_map(df,year,pais):

    if pais != 'All':
        df= df[(df['year'] == year )& (df['pais'] == pais)]
    else: 
        df= df[(df['year'] == year )]

    map= folium.Map ( location=[30,-86],zoom_start=2, 
                    scrollWheelZoom= False, tiles= 'CartoDB positron')
    choropleth = folium.Choropleth( geo_data ='C:/Users/yoe_1/OneDrive/Escritorio/Entorno/world-administrative-boundaries.geojson',
                                    data=df,
                                    columns=( 'pais','edvan'),
                                    key_on='feature.properties.name',
                                    line_opacity=0.8,
                                    highlight=True,
                                    fill_color ='YlOrRd', 
                                    fill_opacity = 0.7
                                    
    )
    choropleth.geojson.add_to(map)

    df = df.set_index('pais')
    # nombre_pais='Argentina'

    for feature in choropleth.geojson.data['features']:
        nombre_pais = feature['properties']['name']
        feature['properties']['Indicador'] = 'Indice:' + str('{:,}'.format(df.loc[nombre_pais,'edvan']) if nombre_pais in list(df.index) else 'N/A')  
    choropleth.geojson.add_child( folium.features.GeoJsonTooltip(['name','Indicador'],labels=False ) )
    st_map = st_folium(map, width=530,height=600)
    return st_map

# Display - FILTROS

def display_time(df):
    year_list= list(df['year'].unique())
    year_list.sort()
    year= st.selectbox('AÑO',year_list, len(year_list)-1)
    return year

def display_countrie(df,country_name):
    pais_list= ['All'] +list(df['NOMBRE PAIS'].unique())
    pais_list.sort(reverse=False)
    pais_index=pais_list.index(country_name) if country_name and country_name in pais_list else 0
    pais= st.selectbox('Seleccionar Pais :',pais_list, pais_index)
    return pais

def display_ingresos(df):#,country_name):
    ingresos_list= ['All'] +list(df['NIVEL INGRESOS'].unique())
    ingresos_list.sort()
    # pais_index=ingresos_list.index(country_name) if country_name and country_name in ingresos_list else 0
    ingresos= st.selectbox('Seleccionar Nivel de Ingresos :',ingresos_list)#, pais_index)
    return ingresos

# Display - TABLAS

def display_tables(df,year,pais):
    if pais != 'All':
        df= df[(df['year'] == year )& (df['pais'] == pais)]
    else: 
        df= df[(df['year'] == year )]
        
    paises_list = df.drop(['id_pais','year'],axis=1)
    paises_list=paises_list.rename({'edvan': 'ESPRNZA.VIDA'}, axis=1)
    paises_list = paises_list.sort_values(by='ESPRNZA.VIDA',ascending=False).reset_index(drop=True)
    # paises_list= paises_list.style.hide_index()
    paises_list=paises_list.set_index('pais')
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
    y1 = df["IND.ESTADO"]
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

# Display - Metricas

def display_corr(df,pais,metric_title):
    val_corr = df[df["NOMBRE PAIS"] == pais].corr().loc['ESPERANZA'][1]
    return st.metric(metric_title,'{:,}'.format(round(val_corr,2)))

def display_medias(df,pais,metric_title,sub_indice):
    val_media = df[df["NOMBRE PAIS"] == pais].mean().loc[f'{sub_indice}']
    return st.metric(metric_title,'{:,}'.format(round(val_media,2)))

# Display - ABOUT

def display_about():
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

# Display - RESULTADOS

def main():

    # ENCABEZADO
    image = Image.open('C:/Users/yoe_1/OneDrive/Escritorio/Entorno/imagenes/Logo1.png')
    st.image( image , caption=None, width=250, use_column_width=None, clamp=True, channels="RGB", output_format="auto")
    # st.set_page_config(page_title='Esperanza de Vida') #, page_icon='',  layout='wide')

    st.title('ESPERANZA DE VIDA')
    st.subheader('Analisis de la Esperanza de Vida del Continente Americano')

    # LOAD DATA 
    df_exp_vida = pd.read_csv('C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/tbl_esperanza_vida_paises.csv')
    dfEducacion = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/Indice_Educacion.csv")#, usecols=['NOMBRE PAIS','ANIO','ED.INDEX','ESPERANZA'])
    dfTrabajo = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/Indice_Trabajo.csv")#, usecols = ['NOMBRE PAIS','ANIO','TRAB.INDEX','ESPERANZA'])
    dfRecursos = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/Indice_Recursos_Estado.csv")#, usecols = ['NOMBRE PAIS','ANIO','IND.ESTADO','ESPERANZA'])
    dfMedio = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/Indice_Medio_Ambiente.csv")#, usecols = ['NOMBRE PAIS','ANIO','AMB.INDEX','ESPERANZA'])
    dfNivel = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/Indice_Nivel_Vida.csv")#, usecols = ['NOMBRE PAIS','ANIO','IND.N.VIDA','ESPERANZA'])
    dfIngresos = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/indice_ev_nivel_ingresos.csv", usecols = ['NOMBRE PAIS','PAIS','ANIO','NIVEL INGRESOS','ESPERANZA DE VIDA'])

    year = 2020
    pais= ''
    country_name = ''
    metric_title= 'Correlación'
   
    # DISPLAY FILTERS AND MAP

    selected = option_menu (
            menu_title = None,
            options=['About','Visual','ML', 'Data'],
            icons=['bookmark-check-fill','house','envelope'],
            orientation='horizontal',
            styles={"container": {"padding": "0!important", "background-color": "orange"},
                    "icon": {"color": "red", "font-size": "25px"}, 
                    "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "black"}}
    )

    if selected == 'About':
        display_about()
        
    if selected == 'Visual':
        
        with st.container():
            st.write("---")
            # Filtros (Año/Pais)
            year = 2020                                         #display_time(df_exp_vida)
            pais = display_countrie(dfEducacion,country_name)
            ingresos = display_ingresos(dfIngresos)

            left_column, right_column = st.columns([2,1],gap="small")
            with left_column:
                # st.header("Mapa")
                country_name = display_map(df_exp_vida,year,pais)
            with right_column:
                # st.header("Tabla")
                # st.write(display_tables(df_exp_vida,year).to_html(index=False), unsafe_allow_html=True)
                st.dataframe(display_tables(df_exp_vida,year,pais),height=600,width=250)

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
                    display_corr(dfEducacion,pais,metric_title)
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
                    str(display_corr(dfTrabajo,pais,metric_title))
                with col2:
                    display_medias(dfTrabajo,pais,'Media del Ind.Trabajo','TRAB.INDEX')              
                with col3:
                    display_medias(dfTrabajo,pais,'Media del Desmpleo','DESEMPLEO')
                with col4:
                    display_medias(dfTrabajo,pais,'Media de la Pobl. Activa','FUERZA LABORAL')
            ##(3)  
            with st.container():
                st.write("---")
                st.subheader(f'Indice Recursos y Estado en {pais}')
                st.pyplot(display_grafico_recursos(dfRecursos,pais))
            with st.container():        
                st.subheader('Estadísticos')
                col1,col2,col3,col4 = st.columns([1.2,1.5,1.5,1.5])
                with col1:
                    display_corr(dfRecursos,pais,metric_title)
                with col2:
                    display_medias(dfRecursos,pais,'Media del Ind.Recursos/Estado','IND.ESTADO')
                with col3:
                    display_medias(dfRecursos,pais,'Media de Inv. en Salud','INVERSION SALUD')
                with col4:
                    display_medias(dfRecursos,pais,'Media de Inv. en Educación','INVERSION EDUCACION')
            #(4)
            with st.container():
                st.write("---")
                st.subheader(f'Indice Medio Ambiente y Estado en {pais}')
                st.pyplot(display_grafico_medio(dfMedio,pais))
            with st.container():
                st.subheader('Estadísticos')
                col1,col2,col3,col4 = st.columns([1,1.5,1.5,1.1])
                with col1:
                    display_corr(dfMedio,pais,metric_title)
                with col2:
                    display_medias(dfMedio,pais,'Media del Ind.Med.Ambiente','AMB.INDEX')
                with col3:
                    display_medias(dfMedio,pais,'Media del Agot. de recursos','AGOTAMIENTO RECURSOS')
                with col4:
                    display_medias(dfMedio,pais,'Media de Emis. de CO2','EMISIONES CO2')
            #(5)
            with st.container():
                st.write("---")
                st.subheader(f'Indice Nivel de Vida en {pais}')
                st.pyplot(display_grafico_nivel(dfNivel,pais))
            with st.container():
                st.subheader('Estadísticos')
                col1,col2,col3,col4 = st.columns([1,1.3,1.3,1.3])
                with col1:
                    display_corr(dfNivel,pais,metric_title)
                with col2:
                    display_medias(dfNivel,pais,'Media del Ind.Nivel de vida','IND.N.VIDA')
                with col3:
                    display_medias(dfNivel,pais,'Media del Cons. Alcohol','CONSUMO ALCOHOL')
                with col4:
                    display_medias(dfNivel,pais,'Media del Cons. Tabaco','CONSUMO TABACO')

    if selected == 'ML':
        st.write('')  

    if selected == 'Data':
        st.write('Datasets')
    
    




if __name__=='__main__':
    main()


















        

# with st.container():
#     st.write("---")
#     st.header("Get In Touch With Me!")
#     st.write("##")

#     # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
#     contact_form = """
#     <form action="https://formsubmit.co/YOUR@MAIL.COM" method="POST">
#         <input type="hidden" name="_captcha" value="false">
#         <input type="text" name="name" placeholder="Your name" required>
#         <input type="email" name="email" placeholder="Your email" required>
#         <textarea name="message" placeholder="Your message here" required></textarea>
#         <button type="submit">Send</button>
#     </form>
#     """
#     left_column, right_column = st.columns(2)
#     with left_column:
#         st.markdown(contact_form, unsafe_allow_html=True)
#     with right_column:
#         st.empty()
