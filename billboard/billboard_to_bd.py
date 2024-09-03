import billboard
import pyodbc
from datetime import datetime, timedelta

def get_daily_hot_100(year):
    current_date = datetime(year, 1, 1)
    
    daily_charts = []

    while current_date.year == year:
        try:
            date_str = current_date.strftime('%Y-%m-%d')
            
            chart = billboard.ChartData('hot-100', date=date_str)
            
            if chart:
                print("Entro a charts)")
                daily_charts.append((date_str, chart))
                break
            
        except Exception as e:
            print(f"No hay chart para día {date_str}.")
            pass
   
        current_date += timedelta(days=1)
    
    return daily_charts

def save_charts_to_sql_server(charts, server, database):
    # Conéctate a SQL Server usando autenticación de Windows
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Hot100Charts (
        ChartDate DATE,
        Rank INT,
        Title VARCHAR(255),
        Artist VARCHAR(255),
        PeakPosition INT,
        LastPosition INT,
        WeeksOnChart INT,
        IsNew BIT
    )
    """)
    conn.commit()

    # Inserta las filas en la tabla
    for date_str, chart in charts:
        for song in chart:
            cursor.execute("""
            INSERT INTO Hot100Charts (ChartDate, Rank, Title, Artist, PeakPosition, LastPosition, WeeksOnChart, IsNew)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, date_str, song.rank, song.title, song.artist, song.peakPos, song.lastPos, song.weeks, int(song.isNew))
        conn.commit()

    # Cierra la conexión
    cursor.close()
    conn.close()

# Ejemplo de uso
year = 2023
server_name = 'localhost\\SQLEXPRESS'
database_name = 'DB_BRILLITT'

# Obtén los gráficos diarios
daily_charts = get_daily_hot_100(year)

# Guarda la información en la base de datos
save_charts_to_sql_server(daily_charts, server_name, database_name)
