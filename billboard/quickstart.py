import billboard
from datetime import datetime, timedelta

def get_weekly_hot_100(year):
    current_date = datetime(year, 1, 1)

    weekly_charts = []

    while current_date.year == year:
        try:
            date_str = current_date.strftime('%Y-%m-%d')
            chart = billboard.ChartData('hot-100', date=date_str)
            if chart:
                weekly_charts.append((date_str, chart))
            
        except Exception as e:
            pass
         
        # Avanza una semana
        current_date += timedelta(weeks=1)
    
    return weekly_charts

# Ejemplo: Obtén el Hot 100 semanal para cada semana del 2023
weekly_charts_2023 = get_weekly_hot_100(2023)

# Imprime las primeras 5 canciones de cada semana del 2023
for date_str, chart in weekly_charts_2023:
    print(f"Top 5 del Hot 100 para la semana del {date_str}:")
    for song in chart[:5]:
        print(f"  {song.rank}. {song.title} by {song.artist}")
    print("-" * 40)
