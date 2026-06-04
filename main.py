import requests
import os
from datetime import date, timedelta, datetime
import json
from google.cloud import bigquery
import pandas as pd
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcp_credentials.json"
target_date = date.today() - timedelta(days=1)
url = f'https://api.open-meteo.com/v1/forecast?latitude=10.823&longitude=106.6296&hourly=temperature_2m,relative_humidity_2m&start_date={target_date}&end_date={target_date}'
res = requests.get(url)
if res.status_code == 200:
    # Mở file để ghi (write) với định dạng utf-8 để hỗ trợ tiếng Việt
    with open(f"ThoiTietNgay{target_date}.json", "w") as file:
        json.dump(res.json(), file)
    data = res.json()

# Một cách khác ok hơn
# hourly = data["hourly"]
# df = pd.DataFrame({
#     "timestamp": hourly["time"],
#     "temperature": hourly["temperature_2m"],
#     "humidity": hourly["relative_humidity_2m"]
# })
# df["timestamp"] = pd.to_datetime(df["timestamp"])
# df["ingested_at"] = datetime.utcnow()

    timestamp = data['hourly']['time']
    temperature = data['hourly']['temperature_2m']
    humidity = data['hourly']['relative_humidity_2m']
    data_using = {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity
    }
    df = pd.DataFrame(data_using)
    df['ingested at'] = datetime.now()
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        write_disposition= "WRITE_TRUNCATE"
    )

    job = client.load_table_from_dataframe(
        df,
        'weather-project-498116.weather_info.weather_staging',
        job_config= job_config
    )

else:
    print("API error: ", res.status_code)
