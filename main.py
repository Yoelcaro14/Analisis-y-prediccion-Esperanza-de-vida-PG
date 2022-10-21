import extraccion as ex
import transformacion as tr
import load as ld
import creacion_bd as bd

# Hilo conductor
print("Iniciando el proceso de ETL, arrancaremos por la extracción...")
ex.extraccion()
print("Extracción finalizada")

print("----------")
print("----------")
print("Seguiremos con la transformación...")
tr.transformacion()
print("Transformación finalizada")

print("----------")
print("----------")
print("Creando la base de datos...")
print("Especifique la database a crear y cargar: ")
database = input()
bd.creacion_bd(database)
print(f'Base de datos --{database}-- creada')

print("----------")
print("----------")
print("Finalizaremos con la carga de datos")
ld.carga()
print("----------")
print("----------")
print(f'Datos cargados en BD: {database}')
print("----------")
