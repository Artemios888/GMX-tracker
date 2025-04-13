import os
import json
from datetime import datetime
from fetch_gmx_fees import fetch_fees

DATA_FILE = "fees_log.json"

def load_last_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_current_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def notify_if_significant_change(last, current):
    threshold_pct = 20  # % изменения для оповещения
    for network in current:
        if network in last:
            prev_fees = last[network]["fees"]
            curr_fees = current[network]["fees"]
            if prev_fees == 0:
                continue
            change_pct = abs((curr_fees - prev_fees) / prev_fees) * 100
            if change_pct >= threshold_pct:
                print(f"⚠️ Внимание! В {network} изменение комиссий: {change_pct:.2f}%")
        else:
            print(f"ℹ️ Новые данные по сети {network} записаны.")

def main():
    print("📥 Получение текущих данных...")
    current_data = fetch_fees()
    current_data["timestamp"] = datetime.utcnow().isoformat()

    print("📂 Загрузка предыдущих данных...")
    last_data = load_last_data()

    print("📊 Сравнение...")
    notify_if_significant_change(last_data, current_data)

    print("💾 Сохраняем новые данные...")
    save_current_data(current_data)

    print("✅ Завершено!")

if __name__ == "__main__":
    main()
