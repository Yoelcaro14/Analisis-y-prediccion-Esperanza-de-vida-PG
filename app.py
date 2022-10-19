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

    map= folium.Map ( location=[30,-76],zoom_start=2, 
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
    st_map = st_folium(map, width=600,height=600)
    return st_map

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

def display_tables(df,year):
    df = df[df['year']==year]
    paises_list = df.drop(['id_pais','year'],axis=1)
    paises_list = paises_list.sort_values(by='edvan',ascending=False).reset_index(drop=True)
    # paises_list= paises_list.style.hide_index()
    paises_list=paises_list.set_index('pais')
    return paises_list

# def pruebas():
#     if st.button('Say hello'):
#         st.write('Why hello there')
#     else:
#         st.write('Goodbye')


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

def display_metrics(df,pais,metric_title):
    val_corr = df[df["NOMBRE PAIS"] == pais].corr().loc['ESPERANZA'][1]
    return st.metric(metric_title,'{:,}'.format(round(val_corr,2)))


def main():

    # Encabezado
    image = Image.open('C:/Users/yoe_1/OneDrive/Escritorio/Entorno/imagenes/Logo1.png')
    st.image( image , caption=None, width=250, use_column_width=None, clamp=True, channels="RGB", output_format="auto")
    # st.set_page_config(page_title='Esperanza de Vida') #, page_icon='',  layout='wide')

    st.title('ESPERANZA DE VIDA')
    st.subheader('Analisis de la Esperanza de Vida del Continente Americano')

    # LOAD DATA 
    df_exp_vida = pd.read_csv('C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/tbl_esperanza_vida_paises.csv')
    dfEducacion = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/Indice_Educacion.csv", usecols=['NOMBRE PAIS','ANIO','ED.INDEX','ESPERANZA'])
    dfTrabajo = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/Indice_Trabajo.csv", usecols = ['NOMBRE PAIS','ANIO','TRAB.INDEX','ESPERANZA'])
    dfRecursos = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/Indice_Recursos_Estado.csv", usecols = ['NOMBRE PAIS','ANIO','IND.ESTADO','ESPERANZA'])
    dfMedio = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/Indice_Medio_Ambiente.csv", usecols = ['NOMBRE PAIS','ANIO','AMB.INDEX','ESPERANZA'])
    dfNivel = pd.read_csv("C:/Users/yoe_1/OneDrive/Escritorio/Entorno/datasets/Indice_Nivel_Vida.csv", usecols = ['NOMBRE PAIS','ANIO','IND.N.VIDA','ESPERANZA'])


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

            left_column, right_column = st.columns([2,1],gap="small")
            with left_column:
                # st.header("Mapa")
                country_name = display_map(df_exp_vida,year,pais)
            with right_column:
                # st.header("Tabla")
                # st.write(display_tables(df_exp_vida,year).to_html(index=False), unsafe_allow_html=True)
                st.dataframe(display_tables(df_exp_vida,year),height=600,width=250)

        st.write("---")     

        # Graficos
        if pais != 'All':
            st.header("Esperanza de vida e Indices")
            #(1)
            with st.container():
                st.subheader(f'Indice de Educacion en {pais}')
                st.pyplot(display_grafico_educacion(dfEducacion,pais))
            with st.container():
                st.subheader('Correlacion')
                col1,col2,col3 = st.columns(3)
                with col1:
                    display_metrics(dfEducacion,pais,metric_title)
            #(2)
            with st.container():
                st.write("---")
                st.subheader(f'Indice de Trabajo en {pais}')
                st.pyplot(display_grafico_trabajo(dfTrabajo,pais))            
            with st.container():
                st.subheader('Correlacion')
                col1,col2,col3 = st.columns(3)
                with col1:
                    display_metrics(dfTrabajo,pais,metric_title)
            ##(3)  
            with st.container():
                st.write("---")
                st.subheader(f'Indice Recursos y Estado en {pais}')
                st.pyplot(display_grafico_recursos(dfRecursos,pais))
            with st.container():        
                st.subheader('Correlacion')
                col1,col2,col3 = st.columns(3)
                with col1:
                    display_metrics(dfRecursos,pais,metric_title)
            #(4)
            with st.container():
                st.write("---")
                st.subheader(f'Indice Medio Ambiente y Estado en {pais}')
                st.pyplot(display_grafico_medio(dfMedio,pais))
            with st.container():
                st.subheader('Correlacion')
                col1,col2,col3 = st.columns(3)
                with col1:
                    display_metrics(dfMedio,pais,metric_title)
            #(5)
            with st.container():
                st.write("---")
                st.subheader(f'Indice Nivel de Vida en {pais}')
                st.pyplot(display_grafico_nivel(dfNivel,pais))
            with st.container():
                st.subheader('Correlacion')
                col1,col2,col3 = st.columns(3)
                with col1:
                    display_metrics(dfNivel,pais,metric_title)

    if selected == 'ML':
        st.write('')  

    if selected == 'Data':
        st.write('Datasets')
    
    
            
    # Display metrics
    


    # st.write(pruebas())

    # Filtros
    ## Año


    # ## Pais
    # country_list= list(df['pais'].unique())
    # country_list.sort()
    # country= st.sidebar.selectbox('pais',country_list)

    # st.write(df.shape)
    # st.write(df.head())



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
