# Daily 🌎 Image

![Earth Image](./history/2025-07-15/080956.jpg)

**Coordinates:** 13.64502, 61.567383  
**Caption:** This image was taken by NASA's EPIC camera onboard the NOAA DSCOVR spacecraft

---

## Credits

- Updated using NASA's EPIC API 
- Imagery © NASA EPIC / NOAA DSCOVR spacecraft  
- This repo is powered by a GitHub Actions workflow that automates the entire process.

- Fetches NASA's EPIC metadata daily using GitHub Actions
- Downloads the latest image from 2 days ago (due to NASA's data delay)
- Updates this README and logs the change
- Auto-commits changes every morning at 5:00 AM EST (10:00 UTC)

- Runs daily at 13:00 UTC  
- Downloads a random EPIC image of Earth  
- Updates this README with the latest image and its metadata  
- If NASA's EPIC API does not publish a new image, the script will display the most recent available image.

## 📡 Data Source

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
- Satellite damage and being able to cache and pull from recent backups.

_Last updated: Mon Sep 01 13:31:05 UTC 2025_
