
import os
import requests
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

# === CONFIG ===
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
EPIC_API_URL = "https://api.nasa.gov/EPIC/api/natural"
IMAGE_BASE_URL = "https://epic.gsfc.nasa.gov/archive/natural"
HISTORY_DIR = "history"
README_FILE = "README.md"

# === CREATE MAIN HISTORY FOLDER ===
Path(HISTORY_DIR).mkdir(exist_ok=True)

def fetch_metadata_for_date(date):
    url = f"{EPIC_API_URL}/date/{date}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data
    return None

# === Try yesterday's metadata first ===
target_date = (datetime.now(timezone.utc) - timedelta(days=1)).date()
print(f"📅 Trying to fetch EPIC image metadata for {target_date}")
data = fetch_metadata_for_date(target_date)

if not data:
    print(f"❌ No EPIC metadata for {target_date}. Using most recent image from history...")
    subfolders = sorted(Path(HISTORY_DIR).iterdir(), reverse=True)
    for folder in subfolders:
        if folder.is_dir():
            image_files = list(folder.glob("*.jpg"))
            if image_files:
                image_path = image_files[0]
                date_obj = datetime.strptime(folder.name, "%Y-%m-%d")
                filename = image_path.name
                image_name = filename.replace(".jpg", "")
                target_date = date_obj
                day_folder = folder
                print(f"📁 Using fallback image from {folder.name}")
                break
    else:
        raise Exception("❌ No fallback image found in history folder.")

    # Populate fake metadata fields
# Try loading metadata from fallback folder
    metadata_file = image_path.with_suffix('.json')
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            closest_entry = json.load(f)
        print(f"📝 Loaded metadata for fallback image.")
    else:
        print(f"⚠️ No metadata file found for fallback image. Using placeholder values.")
        closest_entry = {
            "image": image_name,
            "date": date_obj.strftime("%Y-%m-%d %H:%M:%S"),
            "caption": "Fallback image from previous successful day.",
            "centroid_coordinates": {"lat": 0.0, "lon": 0.0}
        }

else:
    print(f"✅ Found metadata for {target_date}")
    closest_entry = random.choice(data)
    print(f"🎲 Random image selected: {closest_entry['image']} at {closest_entry['centroid_coordinates']}")

    image_name = closest_entry['image']
    date_str = closest_entry['date']
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    date_path = date_obj.strftime("%Y/%m/%d")
    day_folder = os.path.join(HISTORY_DIR, date_obj.strftime("%Y-%m-%d"))
    Path(day_folder).mkdir(parents=True, exist_ok=True)
    filename = f"{date_obj.strftime('%H%M%S')}.jpg"
    image_url = f"{IMAGE_BASE_URL}/{date_path}/jpg/{image_name}.jpg"
    image_path = os.path.join(day_folder, filename)

    # Download image
    try:
        img_response = requests.get(image_url, timeout=15)
        img_response.raise_for_status()
        with open(image_path, 'wb') as f:
            f.write(img_response.content)
        print(f"✅ Downloaded {filename} (random Earth image)")
    # Save metadata
        metadata_path = os.path.join(day_folder, f"{date_obj.strftime('%H%M%S')}.json")
        with open(metadata_path, 'w', encoding='utf-8') as meta_file:
            json.dump(closest_entry, meta_file, indent=2)
    except requests.exceptions.RequestException as e:
        raise Exception(f"❌ Failed to download image: {e}")

# === PREPARE README IMAGE BLOCK ===
image_rel_path = f"./{day_folder}/{filename}"
time_str = date_obj.strftime('%H:%M:%S')
caption = closest_entry.get("caption", "")
coords = closest_entry.get("centroid_coordinates", {})

readme_content = f"""# Daily 🌎 Image

![Earth Image]({image_rel_path})

**Coordinates:** {coords.get("lat")}, {coords.get("lon")}  
**Caption:** {caption}

---

## Credits

- Updated using NASA's EPIC API 
- Imagery © NASA EPIC / NOAA DSCOVR spacecraft  
- This repo is powered by a GitHub Actions workflow that automates the entire process.

## What it does

- Runs daily at 13:00 UTC  
- Downloads a random EPIC image of Earth  
- Updates this README with the latest image and its metadata  
- If NASA's EPIC API does not publish a new image, the script will display the most recent available image.

## Why I built this

- GitHub Actions and workflows  
- Automation scripts 
- Python scripts
- Git operations from within workflows  
- Working with external APIs  
- Show a daily random image of Earth

## How it works

- Fetches all available EPIC images  
- Picks one at random  
- Saves the image  
- Updates this README  

## Things to improve

- NASA updates some day's photos more than a day after, so need to account for latency. 
- Solved by saving and pulling from API photos history.

## Satellite damage

- The satellite that takes these pictures is damaged as of July 15th.
- NASA is working on fixing it.

_Last updated: {datetime.now(timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y')}_
"""

# === WRITE TO README ===
with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(readme_content)

print("✅ README.md updated.")
