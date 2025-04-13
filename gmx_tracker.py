import requests
import csv
import os
from datetime import datetime

# URLs для сетей
URLS = {
    "Arbitrum": "https://stats.gmx.io/api/arbitrum/fees",
    "Avalanche": "https://stats.gmx.io/api/avalanche/fees"
}

# Файл для сохранения данных
CSV_FILE = "gmx_fees_log.csv"

def fetch_fees(network, url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        total_fees = data.get("totalFees", 0)
        return total_fees
    except Exception as e:
        print(f"[{network}] Ошибка при получении данных: {e}")
        return None

def read_last_row():
    if not os.path.exists(CSV_FILE):
        return {}
    
    with open(CSV_FILE, "r", newline='', encoding='utf-8') as file:
        reader = list(csv.DictReader(file))
        if not reader:
            return {}
        return reader[-1]

def write_new_row(timestamp, arbitrum_fees, avalanche_fees):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "arbitrum_fees", "avalanche_fees"])
        writer.writerow([timestamp, arbitrum_fees, avalanche_fees])

def main():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    arb_fees = fetch_fees("Arbitrum", URLS["Arbitrum"])
    ava_fees = fetch_fees("Avalanche", URLS["Avalanche"])

    if arb_fees is None or ava_fees is None:
        print("Ошибка получения данных. Завершение.")
        return

    last_row = read_last_row()
    last_arb = float(last_row.get("arbitrum_fees", 0))
    last_ava = float(last_row.get("avalanche_fees", 0))

    # Вывод разницы для отладки
    print(f"[Arbitrum] Старое: {last_arb}, Новое: {arb_fees}, Разница: {arb_fees - last_arb}")
    print(f"[Avalanche] Старое: {last_ava}, Новое: {ava_fees}, Разница: {ava_fees - last_ava}")

    write_new_row(now, arb_fees, ava_fees)

if __name__ == "__main__":
    main()
