# 🎬 Jellyfin Movie Statistics Script

This Python script scans your Jellyfin-compatible movie folder structure and generates statistics about your video library. It identifies main movie files, counts them, and provides insights by year and decade.

## 📂 Folder Structure Assumptions

The script expects a root directory containing one folder per movie, like:

```
Z:\Filme\Filme\
├── Inception (2010)\
│   └── Inception (2010).mkv
├── The Lord of the Rings\
│   ├── Fellowship\
│   │   ├── part1.mkv
│   │   └── part2.mkv
│   └── Trailer\
│       └── trailer.mkv
```

- Only the main movie file should be in the main folder (or sub-subfolder).
- Extra content (e.g. trailers, extras) should not contain a year in the filename, or be placed in a separate subfolder.
- Split movies like `"part1"`, `"part2"` will be counted as one movie if the filename includes a year.

## ✅ Features

- Recursively scans directories for `.mkv`, `.mp4`, and `.avi` files
- Identifies **main movie files** using:
  - Presence of a 4-digit year (e.g. `(2001)`)
  - File naming (e.g. ignoring `-part1`, `-trailer`)
- Skips and lists videos without a year
- Generates statistics:
  - Total number of main movies
  - Distribution by year
  - Distribution by decade

## 📦 Requirements

- Python 3.10+
- `python-dotenv`

Install requirements with:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```
python-dotenv>=1.0.0
```

## ⚙️ Usage

1. Clone this repo or copy the script.
2. Create a `.env` file in the same folder:

```env
ROOT_DIR=Z:\Filme\...
```

3. Run the script:

```bash
python main.py
```

## 📊 Example Output

```
✅ Main Movies Found:
Z:\Filme\Filme\Inception (2010)\Inception (2010).mkv
Z:\Filme\Filme\Matrix (1999)\Matrix (1999).mp4

⚠️ MKV files without a year (not counted as main movies):
Z:\Filme\Filme\Matrix (1999)\trailer.mkv

🎬 Total Movies Counted: 2

📆 Movie Distribution by Year:
1999: 1 movies
2010: 1 movies

📊 Movie Distribution by Decade:
1990s: 1 movies
2010s: 1 movies
```

## 📌 Notes

- Only files containing a **year in the filename** are treated as main movies.
- Files like `movie-trailer.mkv` or `sample.avi` without a year are ignored.
- Movies with multiple parts (e.g. `part1`, `part2`) are counted as one movie if they share a name and year.

## 📥 To Do (Ideas for Future Improvements)

- Export statistics to CSV
- Metadata extraction via `ffprobe`
- Web UI dashboard
- Duplicate movie detection
- Watch progress statistics via Jellyfin API

---

MIT License – use freely and modify as needed.
