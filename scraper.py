import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from pathlib import Path

def scrape_dram():
    url = "https://www.dramexchange.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    res = requests.get(url, headers=headers, timeout=20)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    tbody = soup.find("tbody", id="tb_NationalDramSpotPrice")
    if not tbody:
        raise ValueError("DRAM Spot Price 테이블을 찾을 수 없습니다.")

    today = datetime.now().strftime("%Y-%m-%d")
    data = []

    for tr in tbody.find_all("tr")[1:]:
        tds = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(tds) >= 7:
            data.append({
                "Date": today,
                "Item": tds[0],
                "Session Average": tds[5],
                "Change": tds[6]
            })

    df = pd.DataFrame(data)

    save_dir = Path("data")
    save_dir.mkdir(exist_ok=True)

    filename = save_dir / f"DRAM_Spot_{today}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    print(f"저장 완료 → {filename}")
    print(df.to_string(index=False))


if __name__ == "__main__":
    scrape_dram()
