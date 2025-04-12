# fetch_gmx_data.py
# Получает доходность по GLP в сети Arbitrum с сайта GMX.io

import requests

def fetch_glp_apr():
    url = "https://stats.gmx.io/api/glp/stats"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        apr = data["glpAprArbitrum"] * 100
        print(f"Текущая доходность GLP (Arbitrum): {apr:.2f}% годовых")
    else:
        print(f"Ошибка при получении данных: {response.status_code}")

if __name__ == "__main__":
    fetch_glp_apr()
