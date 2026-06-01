import requests
import os
from datetime import date, timedelta
target_date = date.today() - timedelta(days=1)
url = f'https://api.open-meteo.com/v1/forecast?latitude=10.823&longitude=106.6296&hourly=temperature_2m,relative_humidity_2m&start_date={target_date}&end_date={target_date}'
res = requests.get(url)
if res.status_code == 200:
    print(res.json())
else:
    print("API error: ", res.status_code)
