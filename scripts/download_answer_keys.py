#!/usr/bin/env python3
"""
Download official GATE CSE answer keys (2011 - 2025) and save them to answer_keys/
"""

import os
import sys
import json
import csv
import re
import urllib.request
import urllib.error
from pathlib import Path
from bs4 import BeautifulSoup

OUTPUT_DIR = Path("answer_keys")

GOOGLE_DRIVE_KEYS = {
    # 2025
    "2025_CS1_key.pdf": "1788WOR8AAdb5oR9SFNOg6ZOqLje-xHwU",
    "2025_CS2_key.pdf": "1owBOF96x3Fatj-sLp9z7GxLt3AwWSPDf",
    # 2024
    "2024_CS1_key.pdf": "106ptm21IAnDJ1Y3F7wnSLRcT7mLDavyX",
    "2024_CS2_key.pdf": "1V_k3tKwPF8twrQI2nqZEz03dTQbCylG5",
    # 2023
    "2023_CS_key.pdf": "14tU1APAz4ddbeqeJeGuszPuPRF3-Xq_O",
    # 2022
    "2022_CS_key.pdf": "1U2ro3Oya21A8SIHf8cLAkf_wQN15mp9a",
    # 2021
    "2021_CS1_key.pdf": "15DOjJGIT5nNQ4o0hmHxa3iy8EY3m1ShN",
    "2021_CS2_key.pdf": "1viqL1BURfNmPgiURPueBO3anck6-IYmo",
    # 2020
    "2020_CS_key.pdf": "16013cuRi_2fNS4JSQmF_6EIwtQjYXyx8",
    # 2019
    "2019_CS_key.pdf": "1QQSP-BNOXH_hDAdcFLOXlHpH4XFDR8ib",
    # 2018
    "2018_CS_key.pdf": "1HEcIz6mZoGfGGW3RMY0W2Mee6_65GW5R",
    # 2017
    "2017_CS1_key.pdf": "1XNwOUEbRa-IdQOTfnBJOrqN7XmtCGVrh",
    "2017_CS2_key.pdf": "1LWmOwxMnFkNqNI5SWsrJzReXfAEbyZAQ",
    # 2016
    "2016_CS1_key.pdf": "1hr7a-IvT22EpYyw8qgbdpr6y_cX8jOIz",
    "2016_CS2_key.pdf": "16DeLUMJH1noQrIlAvtv4dIjcDmR43oul",
    # 2014
    "2014_CS1_key.pdf": "1y-j8-5j69c4p8S200D-j7loCmvl97gI6",
    "2014_CS2_key.pdf": "1oRBWf5W8lPxQGcQvDkPYR1Igs6wSnoLI",
    "2014_CS3_key.pdf": "1HRj0sh_oeYi4lpAY7FEkHTUFFFy5tb3q",
    # 2013
    "2013_CS_key.pdf": "11760s1L3JNpXWzE6Fzxqzsj18c7k-01i",
    # 2012
    "2012_CS_key.pdf": "1fTPVtMRos3J3O_PgAs03O6w-2AyxEzov",
    # 2011
    "2011_CS_key.pdf": "1LPlDbEgtZIYg_HNTbX1V3kyLZEUkbEn-",
}

WIKI_2015_URLS = {
    "2015_CS1_key": "http://gatecse.in/wiki/GATE2015-1_Keys",
    "2015_CS2_key": "http://gatecse.in/wiki/GATE2015-2_Keys",
    "2015_CS3_key": "http://gatecse.in/wiki/GATE2015-3_Keys",
}


def download_gdrive_file(file_id: str, dest_path: Path) -> bool:
    urls = [
        f"https://drive.usercontent.google.com/download?id={file_id}&export=download&authuser=0",
        f"https://docs.google.com/uc?export=download&id={file_id}",
    ]
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                # Check for PDF signature or confirm token
                if data.startswith(b"%PDF-"):
                    with open(dest_path, "wb") as f:
                        f.write(data)
                    return True
                # If HTML returned, check for confirm code
                text = data.decode("utf-8", errors="ignore")
                confirm_match = re.search(r"confirm=([0-9A-Za-z_]+)", text)
                if confirm_match:
                    confirm_code = confirm_match.group(1)
                    confirm_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm={confirm_code}"
                    req2 = urllib.request.Request(confirm_url, headers=headers)
                    with urllib.request.urlopen(req2, timeout=30) as resp2:
                        data2 = resp2.read()
                        if data2.startswith(b"%PDF-"):
                            with open(dest_path, "wb") as f:
                                f.write(data2)
                            return True
        except Exception as e:
            print(f"Error downloading {file_id} from {url}: {e}")

    return False


def fetch_2015_keys():
    for name, url in WIKI_2015_URLS.items():
        json_path = OUTPUT_DIR / f"{name}.json"
        csv_path = OUTPUT_DIR / f"{name}.csv"
        print(f"Fetching 2015 key from {url}...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table")
            if not table:
                print(f"No table found for {url}")
                continue

            rows = table.find_all("tr")
            header = [td.get_text(strip=True) for td in rows[0].find_all(["td", "th"])]
            records = []
            for tr in rows[1:]:
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if len(cells) == len(header):
                    record = dict(zip(header, cells))
                    records.append(record)

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2)

            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                writer.writerows(records)

            print(f"Saved {len(records)} entries to {json_path} and {csv_path}")
        except Exception as e:
            print(f"Error fetching 2015 keys from {url}: {e}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR.resolve()}")

    success_count = 0
    fail_count = 0

    print("\n--- Downloading Official Answer Key PDFs (2011 - 2025) ---")
    for filename, file_id in GOOGLE_DRIVE_KEYS.items():
        dest = OUTPUT_DIR / filename
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"[SKIP] {filename} already exists ({dest.stat().st_size} bytes)")
            success_count += 1
            continue

        print(f"Downloading {filename} (ID: {file_id})...")
        ok = download_gdrive_file(file_id, dest)
        if ok:
            print(f"[SUCCESS] {filename} ({dest.stat().st_size} bytes)")
            success_count += 1
        else:
            print(f"[FAILED] {filename}")
            fail_count += 1

    print("\n--- Fetching 2015 Official Keys (Structured Wiki Tables) ---")
    fetch_2015_keys()

    print("\n--- Summary ---")
    print(f"Successfully downloaded/verified: {success_count} PDFs")
    if fail_count > 0:
        print(f"Failed downloads: {fail_count} files")
    else:
        print("All downloads completed successfully.")


if __name__ == "__main__":
    main()

