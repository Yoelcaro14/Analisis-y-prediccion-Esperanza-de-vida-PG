![LorussoLogo](https://scontent.fmdq3-1.fna.fbcdn.net/v/t39.30808-6/313263786_110911411815519_5789214515215323117_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=730e14&_nc_ohc=Uro4rsrXKA8AX_QfctZ&_nc_ht=scontent.fmdq3-1.fna&oh=00_AfAzh9i3mpLsiiAp1wuNUflN2prWxLmA6RYCGeY3ecaaog&oe=635DF96D)

# **PROYECTO FINAL , DATA SCIENCE SOY HENRY**

# <h1 align="center">**`Lorusso y Asocs.`**</h1>

Este es nuestro proyecto final para SoyHenry, trabajamos con la esperanza de vida en el continente americano, mas especificamente, a los países pertenecientes a la OEA entre los años 2000 y 2020.

 **Integrantes**: Lorusso Nicolas, Caneva Hugo, Carocancha Yoel y Cook Camilo

</br>

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

## **Nuestro camino**

Para poder realizar el proyecto, por primera parte creamos un datawarehouse utilizando como prestador de servicio a AWS, creando una base de datos con el motor de base de datos *PostgreSQL*.

Obtuvimos los datasets a utilizar desde la API (utilizando wbgapi) del [World Data Bank](https://databank.worldbank.org/source/world-development-indicators) y con archivos CSV de otras fuentes confiables como la Organizacion Mundial de la Salud (OMS) entre otras.

![DataWarehouse](https://scontent.fmdq3-1.fna.fbcdn.net/v/t39.30808-6/306332137_110927635147230_2178348703837984022_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=730e14&_nc_ohc=bo7XYUecuacAX8MEVus&_nc_ht=scontent.fmdq3-1.fna&oh=00_AfA3FyDDZ5wHRNjwS18PtUjEVw7AFanM27laCM5Fh45KvQ&oe=635E181C)

Se hizo una automatizacion para la carga de los datos extraídos (pipeline) y se organizó, primero, la base de datos en torno a 28 tablas, las cuales derivaron en solo 5 tablas con las variables y los indices antes mencionados.

Proseguimos haciendo, ya con las 5 tablas, una Web APP con la herramienta *Streamlit* dividida por cuatro secciones. *About* *Visual* *Machine Learning* *Data*

Ya finalizando, creamos modelos de Machine Learning para predecir si se cumplian nuestras cuatro KPI's y por ultimo desarrollamos un dashboard en PowerBI para realizar la parte de Analytics del proyecto
</br>
**KPI 1 : % de aumento en la esperanza de vida en referencia hace 5 años**
</br>
**KPI 2 : Aumento en la esperanza de vida en 5 años (2025) si se invierte 5% adicional en educacion**
</br>
**KPI 3 : Aumento en la esperanza de vida en 5 años (2025) si se invierte 5% adicional en salud**
</br>
**KPI 4 : Aumentar la esperanza de vida 2.5 años en un periodo de 5 años (2025) si se disminuye la contaminacion PM 2.5 en 50%**
</br>


[PowerBI](https://app.powerbi.com/view?r=eyJrIjoiZTkwNDJlNmMtNDRkOS00MWM4LWEyMjQtY2VkMmE1NjI0NDk4IiwidCI6IjQyM2U0YjljLTBjNTUtNDYyZC04OTA1LWU4NWQxZGNlZGJjZCJ9&pageName=ReportSection2d5b2ba67c8cf353e65e)





