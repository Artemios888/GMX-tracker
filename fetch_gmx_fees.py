import requests
import csv
from datetime import datetime

# Ссылки на API по Arbitrum и Avalanche
URLS = {
    "Arbitrum": "https://stats.gmx.io/api/arbitrum_stats",
    "Avalanche": "https://stats.gmx.io/api/avalanche_stats"
}

# Имя файла, куда будут сохраняться данные
CSV_FILE = "gmx_fees_log.csv"

# Получаем текущую дату и время в UTC
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# Список для новых строк
new_rows = []

for network, url in URLS.items():
    try:
        response = requests.get(url)
        data = response.json()
        fees = float(data["totalFees"])
        new_rows.append([timestamp, network, fees])
    except Exception as e:
        print(f"Ошибка при запросе данных для {network}: {e}")

# Проверяем, существует ли файл, если нет — создаём с заголовками
try:
    with open(CSV_FILE, mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "network", "fees"])
except FileExistsError:
    pass  # файл уже существует

# Добавляем новые строки
with open(CSV_FILE, mode='a', newline='') as file:
    writer = csv.writer(file)
    for row in new_rows:
        writer.writerow(row)

print("Данные успешно обновлены.")
import csv

with open("fees_data.csv", "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([timestamp, chain, fees])
