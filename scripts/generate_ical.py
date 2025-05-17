import yaml
from pathlib import Path
from datetime import date
from holidays_print import generate_calendar, PUBLIC, UNOFFICIAL, CATHOLIC  # angepasst für Direktnutzung
import locale

try:
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
except locale.Error:
    print("Warning: de_DE.UTF-8 locale not available, falling back.")

CONFIG_FILE = Path("data/ical.yaml")
OUTPUT_DIR = Path("static/ical")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# Clean up output directory (remove all existing .ics files)
for file in OUTPUT_DIR.glob("*.ics"):
    file.unlink()

YEAR_BEFORE = -3
YEAR_AFTER = 5
current_year = date.today().year
start_year = current_year + YEAR_BEFORE
end_year = current_year + YEAR_AFTER

CATEGORY_MAP = {
    "public": PUBLIC,
    "unofficial": UNOFFICIAL,
    "catholic": CATHOLIC
}

with CONFIG_FILE.open("r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

for cal in config.get("calendars", []):
    file_name = cal["file"]
    region = cal.get("region", "DE")
    output_path = OUTPUT_DIR / file_name
    category_keys = cal.get("categories", ["public"])
    categories = [CATEGORY_MAP[c] for c in category_keys if c in CATEGORY_MAP]
    title = cal.get("title", "")

    print(f"Generating {file_name}...")
    generate_calendar(start_year, end_year, region, str(output_path), categories, title)