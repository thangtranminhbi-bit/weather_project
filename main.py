import requests
import os
from datetime import date, timedelta
import json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcp_credentials.json"
target_date = date.today() - timedelta(days=1)
url = f'https://api.open-meteo.com/v1/forecast?latitude=10.823&longitude=106.6296&hourly=temperature_2m,relative_humidity_2m&start_date={target_date}&end_date={target_date}'
res = requests.get(url)
if res.status_code == 200:
    # Mở file để ghi (write) với định dạng utf-8 để hỗ trợ tiếng Việt
    with open(f"ThoiTietNgay{target_date}.json", "w") as file:
        json.dump(res.json(), file)
else:
    print("API error: ", res.status_code)
