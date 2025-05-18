from importlib.metadata import metadata

import yaml
import json
from pathlib import Path
from datetime import date
from holidays_print import generate_calendar, PUBLIC, UNOFFICIAL, CATHOLIC  # angepasst für Direktnutzung
from holidays_print import AUGSBURG

CONFIG_FILE = Path("data/ical.yaml")
OUTPUT_DIR = Path("public/ical")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RESOURCES_DIR = Path("resources/_gen")
RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
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
    "catholic": CATHOLIC,
    "augsburg": AUGSBURG,
}

with CONFIG_FILE.open("r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

metadata_all = []

for cal in config.get("calendars", []):
    file_name = cal["file"]
    region = cal.get("region", "DE")
    output_path = OUTPUT_DIR / file_name
    metadata_file = str(output_path) + ".json"
    category_keys = cal.get("categories", ["public"])
    categories = [CATEGORY_MAP[c] for c in category_keys if c in CATEGORY_MAP]
    title = cal.get("title", "")

    print(f"Generating {file_name}...")
    generate_calendar(start_year, end_year, region, str(output_path), categories, title, str(metadata_file))


    with open(metadata_file, "r", encoding="utf-8") as mf:
        metadata = json.load(mf)
    Path(metadata_file).unlink()
    metadata.update({
        "file": file_name,
        "region": region,
        "categories": category_keys,
        "title": title
    })
    metadata_all.append(metadata)

with open("resources/_gen/metadata_all.json", "w", encoding="utf-8") as out:
    json.dump(metadata_all, out, indent=2, ensure_ascii=False)