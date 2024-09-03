import pyodbc

def connect_to_db():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost\\SQLEXPRESS;'  # Asegúrate de tener el doble backslash
                          'Database=DB_BRILLITT;'
                          'Trusted_Connection=yes;')

    return conn

def test_query(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM YouTubeVideos')
    for row in cursor:
        print(f'VideoID: {row.VideoID}, Titulo: {row.Titulo}, Views: {row.Vistas}')
    cursor.close()

def main():
    conn = connect_to_db()
    try:
        test_query(conn)
        print("La conexión y la consulta se realizaron con éxito.")
    except Exception as e:
        print("Hubo un error al realizar la consulta:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()

