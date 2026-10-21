import os    # os helps talks to my comp, and read the env variable
from datetime import datetime # go and fetch the time
from pathlib import Path #importing tools for files and folders, will be used to build and saves files


RAW_DIR = Path(os.environ.get("RAW_DIR", "raw")) #is there an env variable called RAW DIR, IF YES use it if no use raw and save


def save_raw(source: str, body: str, fetched_at: datetime) -> Path:
    """save one API response exactly as received, under raw/<source>/<yyyy>/<mm>/<dd>/."""
    folder = RAW_DIR / source / fetched_at.strftime("%Y/%m/%d")  #go into the folder & turn the fetch time into text
    folder.mkdir(parents=True, exist_ok=True)  #create a folder & also any missing folder above it & if folder exits, carry on
    path = folder / f"{fetched_at.strftime('%Y%m%dT%H%M%SZ')}.json"  # build the file name with date and time & Z = UTC
    path.write_text(body)  #write the file, saves as written
    return path  # hand the file back to whoever called the function