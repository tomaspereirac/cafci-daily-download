import time
import datetime as dt
from pathlib import Path
import requests

URL = "https://api.pub.cafci.org.ar/pb_get"

def guess_ext(content_type: str) -> str:
    ct = (content_type or "").lower()
    if "excel" in ct or "spreadsheet" in ct:
        return ".xlsx"
    if "csv" in ct or "text/plain" in ct:
        return ".csv"
    return ".bin"

def main():
    params = {"d": int(time.time() * 1000)}
    r = requests.get(URL, params=params, timeout=90)
    r.raise_for_status()

    ext = guess_ext(r.headers.get("Content-Type"))
    today = dt.date.today().isoformat()

    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)

    dated = out_dir / f"cafci_planilla_{today}{ext}"
    alias = out_dir / f"ultimo{ext}"

    dated.write_bytes(r.content)
    alias.write_bytes(r.content)

    print("OK")
    print("Content-Type:", r.headers.get("Content-Type"))
    print("Saved:", dated)
    print("Alias:", alias)

if __name__ == "__main__":
    main()
