import requests
import os
from datetime import date, timedelta, datetime, timezone
import json
from google.cloud import bigquery
import pandas as pd
from google.cloud import storage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="dbtWeather/Weather_dbt/gcp_credential.json"
target_date = date.today() - timedelta(days=1)
url = f'https://api.open-meteo.com/v1/forecast?latitude=10.823&longitude=106.6296&hourly=temperature_2m,relative_humidity_2m&start_date={target_date}&end_date={target_date}'
res = requests.get(url)
if res.status_code == 200:
    #Ghi file json tu API
    with open(f"ThoiTietNgay{target_date}.json", "w") as file:
        json.dump(res.json(), file, ensure_ascii=False, indent=4)
    data = res.json()
    data_using_string = json.dumps(data)

    CSclient = storage.Client()
    bucket = CSclient.bucket("weather-data-lake-123")
    blob = bucket.blob( f"raw/year={target_date.year}/" 
                    f"month={target_date.month:02d}/" 
                    f"day={target_date.day:02d}/" 
                    f"weather_{target_date}.json" 
    )
    blob.upload_from_string(
        data_using_string,
        content_type="application/json"
    )


# Mot cach tao DF
# hourly = data["hourly"]
# df = pd.DataFrame({
#     "timestamp": hourly["time"],
#     "temperature": hourly["temperature_2m"],
#     "humidity": hourly["relative_humidity_2m"]
# })
# df["timestamp"] = pd.to_datetime(df["timestamp"])
# df["ingested_at"] = datetime.utcnow()

    # Mot cach tao  DF khac
    timestamp = data['hourly']['time']
    temperature = data['hourly']['temperature_2m']
    humidity = data['hourly']['relative_humidity_2m']
    data_using = {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity

    }
    df = pd.DataFrame(data_using)
    df['ingested_at'] = datetime.now(timezone.utc)
    df['timestamp'] = pd.to_datetime(df['timestamp'],utc=True)

    BQclient = bigquery.Client()
    load_job_config = bigquery.LoadJobConfig(
        write_disposition= "WRITE_TRUNCATE",
        schema=[
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("temperature", "FLOAT"),
        bigquery.SchemaField("humidity", "INTEGER"),
        bigquery.SchemaField("ingested_at", "TIMESTAMP"),
    ]   
    )

    load_job = BQclient.load_table_from_dataframe(
        df,
        'weather-project-498116.weather_info.weather_staging',
        job_config= load_job_config
    )
    load_job.result()
    merge_query = """
        MERGE `weather-project-498116.weather_info.weather_final` T
        USING `weather-project-498116.weather_info.weather_staging` S
        ON T.timestamp = S.timestamp
        WHEN MATCHED THEN
        UPDATE SET T.temperature = S.temperature, T.humidity = S.humidity, T.ingested_at = S.ingested_at
        WHEN NOT MATCHED THEN
        INSERT (timestamp, temperature, humidity, ingested_at)
        VALUES (S.timestamp, S.temperature, S.humidity, S.ingested_at)
        """
    query_running = BQclient.query(merge_query)
    query_running.result()
    print(f"Hoan thanh ngay {target_date}")
else:
    print("API error: ", res.status_code)
