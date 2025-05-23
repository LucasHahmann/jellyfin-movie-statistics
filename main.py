import os
import re
from collections import defaultdict
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
ROOT_DIR = os.getenv("ROOT_DIR")

# === Configuration ===
VIDEO_EXTENSIONS = ('.mkv', '.mp4', '.avi')
YEAR_PATTERN = re.compile(r"\(?\b(19|20)\d{2}\b\)?")

# === Data Containers ===
main_movies = set()
skipped_due_to_missing_year = []
year_distribution = defaultdict(int)
decade_distribution = defaultdict(int)

# === Helper Functions ===

def normalize_filename(filename: str) -> str:
    """Strip 'part' info and normalize filename for grouping."""
    name = os.path.splitext(filename)[0]
    name = re.sub(r'[-_. ]?part\d+', '', name, flags=re.IGNORECASE)
    return name.strip().lower()

def extract_year_from_filename(filename: str) -> int | None:
    """Extract and clean the year from the filename."""
    match = YEAR_PATTERN.search(filename)
    if match:
        return int(re.sub(r"[^\d]", "", match.group()))
    return None

def find_main_movie_files(directory: str) -> list[str]:
    """Return a list of main movie files from a directory."""
    mkv_files = [
        f for f in os.listdir(directory)
        if f.lower().endswith(VIDEO_EXTENSIONS) and os.path.isfile(os.path.join(directory, f))
    ]

    if not mkv_files:
        return []

    files_with_year = [f for f in mkv_files if YEAR_PATTERN.search(f)]

    if files_with_year:
        grouped = {}
        for f in files_with_year:
            key = normalize_filename(f)
            grouped.setdefault(key, []).append(f)

        selected_files = [
            os.path.join(directory, sorted(files)[0])
            for files in grouped.values()
        ]
        return selected_files
    else:
        for f in mkv_files:
            skipped_due_to_missing_year.append(os.path.join(directory, f))
        return []

def collect_movies_recursively(path: str) -> list[str]:
    """Recursively search for main movie files."""
    main_files = find_main_movie_files(path)
    if main_files:
        return main_files

    result = []
    subdirs = [
        os.path.join(path, d)
        for d in os.listdir(path)
        if os.path.isdir(os.path.join(path, d))
    ]
    for subdir in subdirs:
        result.extend(collect_movies_recursively(subdir))
    return result

# === Main Logic ===

# Walk through all top-level directories
for entry in os.listdir(ROOT_DIR):
    full_path = os.path.join(ROOT_DIR, entry)
    if os.path.isdir(full_path):
        movies = collect_movies_recursively(full_path)
        for movie_path in movies:
            main_movies.add(movie_path)

# === Output ===

# Main movie list
print("\n✅ Main Movies Found:")
for movie in sorted(main_movies):
    print(movie)

# Skipped files
if skipped_due_to_missing_year:
    print("\n⚠️ MKV files without a year (not counted as main movies):")
    for skipped in sorted(skipped_due_to_missing_year):
        print(skipped)

# Movie count
print(f"\n🎬 Total Movies Counted: {len(main_movies)}")

# Statistics
for movie_path in main_movies:
    filename = os.path.basename(movie_path)
    year = extract_year_from_filename(filename)
    if year:
        year_distribution[year] += 1
        decade = (year // 10) * 10
        decade_distribution[decade] += 1

# Year breakdown
print("\n📆 Movie Distribution by Year:")
for year in sorted(year_distribution):
    print(f"{year}: {year_distribution[year]} movies")

# Decade breakdown
print("\n📊 Movie Distribution by Decade:")
for decade in sorted(decade_distribution):
    print(f"{decade}s: {decade_distribution[decade]} movies")
