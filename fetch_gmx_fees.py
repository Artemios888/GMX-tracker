import requests
import csv
from datetime import datetime

# Определяем текущую временную метку
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# URL-адреса для Arbitrum и Avalanche
urls = {
    "arbitrum": "https://api.stats.gmx.io/fees/arbitrum",
    "avalanche": "https://api.stats.gmx.io/fees/avalanche"
}

# Опрос и сбор данных
fees_data = []
for chain, url in urls.items():
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        fees = data.get("totalFees", 0)
        fees_data.append((timestamp, chain, fees))
    except Exception as e:
        print(f"[{timestamp}] Ошибка при получении данных для {chain}: {e}")

# Сохраняем в CSV
with open("gmx_fees_log.csv", "a", newline="") as file:
    writer = csv.writer(file)
    for row in fees_data:
        writer.writerow(row)
