import requests
import datetime
import time
import csv

START_DATE = datetime.date(2022, 2, 24)
END_DATE = datetime.date.today()
BELLIGERENT = "russia"
BASE_URL = "https://ukr.warspotting.net/api"
HEADERS = {"User-Agent": "WarSpotClient/1.0 (contact@example.com)"}
SLEEP_BETWEEN_DATES = 2
OUTFILE = "warspotting_losses.csv"

def fetch_day_all_pages(date_str: str, belligerent: str):
    all_losses = []
    page = 1

    while True:
        if page == 1:
            url = f"{BASE_URL}/losses/{belligerent}/{date_str}/"
        else:
            url = f"{BASE_URL}/losses/{belligerent}/{date_str}/{page}/"
        print(f"    ↳ Fetching: {url}")
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 404:
                print(f"    No data for {date_str}, page {page} (404).")
                break
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"    Request error: {e}")
            break

        data = r.json().get("losses", [])
        if not data:
            break

        all_losses.extend(data)

        if len(data) < 100:
            break
        page += 1

    return all_losses

def flatten(e: dict) -> dict:
    geo_str = e.get("geo")
    lat, lon = (None, None)
    if geo_str and "," in geo_str:
        parts = geo_str.split(",")
        if len(parts) == 2:
            try:
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
            except ValueError:
                pass

    return {
        "id": e.get("id"),
        "date": e.get("date"),
        "type": e.get("type"),
        "model": e.get("model"),
        "status": e.get("status"),
        "lost_by": e.get("lost_by"),
        "nearest_location": e.get("nearest_location"),
        "geo": geo_str,
        "latitude": lat,
        "longitude": lon,
        "unit": e.get("unit"),
        "tags": e.get("tags"),
        "comment": e.get("comment"),
        "sources": ", ".join(e.get("sources", [])) if isinstance(e.get("sources"), list) else e.get("sources"),
        "photos": ", ".join(e.get("photos", [])) if isinstance(e.get("photos"), list) else e.get("photos"),
    }

def main():
    all_rows = []
    header_written = False

    with open(OUTFILE, mode="w", newline="", encoding="utf-8") as f:
        writer = None
        current = START_DATE
        total_rows = 0

        while current <= END_DATE:
            ds = current.isoformat()
            print(f"\n📅 Fetching records for {ds} …")
            day_records = fetch_day_all_pages(ds, BELLIGERENT)

            if day_records:
                flattened = [flatten(r) for r in day_records]
                if not header_written:
                    writer = csv.DictWriter(f, fieldnames=flattened[0].keys())
                    writer.writeheader()
                    header_written = True
                for row in flattened:
                    writer.writerow(row)
                total_rows += len(flattened)
                print(f"    ✅ {len(flattened)} records written.")
            else:
                print(f"    ⚠️  No records found for {ds}.")
            current += datetime.timedelta(days=1)
            time.sleep(SLEEP_BETWEEN_DATES)

    print(f"\n✅ DONE – {total_rows} total records saved to {OUTFILE}")

if __name__ == "__main__":
    main()
