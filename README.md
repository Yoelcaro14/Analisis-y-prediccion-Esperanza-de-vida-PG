# <p align="center">**ANALISIS Y PREDICIÓN DE LA ESPERANZA DE VIDA**<p>

# <h1 align="center">![imagen](https://github.com/Yoelcaro14/Analisis-y-prediccion-Esperanza-de-vida-PG/blob/Final/Imagenes/Logo1.png)</h1>

En nuestro proyecto grupal final para SoyHenry, trabajamos con la esperanza de vida en el continente americano, mas especificamente, a los países pertenecientes a la OEA entre los años 2000 y 2020.
**Integrantes**: Carocancha Yoel, Lorusso Nicolas, Caneva Hugo y Cook Camilo

## **¿En que consiste nuestro proyecto?**

Nuestro proyecto consiste en poder determinar cuales son los factores mas incidentes en la esperanza de vida de un país, abordamos el trabajo desde 5 factores:
</br>
**1- Educacion**
</br>
**2- Trabajo**
</br>
**3- Nivel de vida**
</br>
**4- Medio Ambiente**
</br>
**5- Estado**

A partir de estos factores, creamos 5 indices.

# <p align="center">![imagen](https://github.com/Yoelcaro14/Analisis-y-prediccion-Esperanza-de-vida-PG/blob/Final/Imagenes/Individuo.png)<p>


## **Nuestro camino**

Para poder realizar el proyecto, por primera parte creamos un datawarehouse utilizando como prestador de servicio a AWS, creando una base de datos con el motor de base de datos *PostgreSQL*.

Obtuvimos los datasets a utilizar desde la API (utilizando wbgapi) del [World Data Bank](https://databank.worldbank.org/source/world-development-indicators) y con archivos CSV de otras fuentes confiables como la Organizacion Mundial de la Salud (OMS) entre otras.

Se hizo una automatizacion para la carga de los datos extraídos (pipeline) y se organizó, primero, la base de datos en torno a 28 tablas, las cuales derivaron en solo 5 tablas con las variables y los indices antes mencionados.

Proseguimos haciendo, ya con las 5 tablas, una Web APP con la herramienta *Streamlit* dividida por cuatro secciones. *About* *Visual* *Machine Learning* *Data*

Ya finalizando, creamos modelos de Machine Learning para predecir si se cumplian nuestras cuatro KPI's y por ultimo desarrollamos un dashboard en PowerBI para realizar la parte de Analytics del proyecto
</br>
**KPI 1 : Incrementar la esperanza de vida por lo menos 1 año aumentando los años de escolaridad 3 años**
</br>
**KPI 2 : Incrementar la esperanza de vida por lo menos 1 años aumentando los ingresos medios p/c un 15%**
</br>
**KPI 3 : Incrementar la esperanza de vida por lo menos 2 años aumentando las inversiones un 20%**
</br>
**KPI 4 : Incrementar la esperanza de vida por lo menos 2 años disminuyendo la contaminacion un 50%**
</br>

## RESULTADOS:

### [Dashboard PowerBI](https://app.powerbi.com/view?r=eyJrIjoiZTkwNDJlNmMtNDRkOS00MWM4LWEyMjQtY2VkMmE1NjI0NDk4IiwidCI6IjQyM2U0YjljLTBjNTUtNDYyZC04OTA1LWU4NWQxZGNlZGJjZCJ9&pageName=ReportSection2d5b2ba67c8cf353e65e)


### [Streamlit](https://nicolordev97-proyectogrupal-app-final-ucei56.streamlitapp.com/)

## </br><h1 align="center">![Streamlit1](https://github.com/Yoelcaro14/Analisis-y-prediccion-Esperanza-de-vida-PG/blob/Final/Imagenes/About.PNG)</h1></br> <h1 align="center">![Streamlit2](https://github.com/Yoelcaro14/Analisis-y-prediccion-Esperanza-de-vida-PG/blob/Final/Imagenes/Visual.PNG)</h1>




