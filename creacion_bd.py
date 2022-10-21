import psycopg2

def creacion_bd(database):
    

    conn = psycopg2.connect(
        host = "proyecto-final-henry.ctv6lgil6x7r.us-east-1.rds.amazonaws.com",
        port = 5432,
        user = "postgres",
        password = "lorussoasoc"
    ) 

    database = database
    
    conn.autocommit = True
    cursor = conn.cursor()

    query_borrar = f"DROP DATABASE IF EXISTS {database};"
    cursor.execute(query_borrar)

    query_crear = f"CREATE database {database};"
    cursor.execute(query_crear)
    print("La database se creo exitosamente!")
    conn.close()

