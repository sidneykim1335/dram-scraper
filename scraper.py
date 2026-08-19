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
    today_data = {}

    for tr in tbody.find_all("tr")[1:]:
        tds = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(tds) >= 7:
            item = tds[0]
            average = tds[5]
            today_data[item] = average

    # 저장 경로
    save_dir = Path("data")
    save_dir.mkdir(exist_ok=True)
    filename = save_dir / "DRAM_Spot.csv"

    if filename.exists():
        df = pd.read_csv(filename, index_col="Item")
    else:
        df = pd.DataFrame()

    # 오늘 날짜 컬럼 추가/업데이트
    for item, average in today_data.items():
        df.loc[item, today] = average

    # 인덱스 이름 설정
    df.index.name = "Item"

    # 날짜 컬럼 정렬
    date_cols = sorted([col for col in df.columns if col != "Item"])
    df = df[date_cols]

    df.to_csv(filename, encoding="utf-8-sig")

    print(f"저장 완료 → {filename}")
    print(f"오늘 날짜: {today}")
    print(df[[today]].to_string())


if __name__ == "__main__":
    scrape_dram()
