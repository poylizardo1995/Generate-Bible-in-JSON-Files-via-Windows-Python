import os
import json
import urllib.request
import urllib.error
import time

OUTPUT_DIR = "./tagalog_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Complete Bible Books & Chapter Counts (Standard 66 Books)
bible_books = {
    # Old Testament
    "Genesis": 50, "Exodus": 40, "Leviticus": 27, "Numbers": 36, "Deuteronomy": 34,
    "Joshua": 24, "Judges": 21, "Ruth": 4, "1 Samuel": 31, "2 Samuel": 24,
    "1 Kings": 22, "2 Kings": 25, "1 Chronicles": 29, "2 Chronicles": 36,
    "Ezra": 10, "Nehemiah": 13, "Esther": 10, "Job": 42, "Psalms": 150,
    "Proverbs": 31, "Ecclesiastes": 12, "Song of Solomon": 8, "Isaiah": 66,
    "Jeremiah": 52, "Lamentations": 5, "Ezekiel": 48, "Daniel": 12, "Hosea": 14,
    "Joel": 3, "Amos": 9, "Obadiah": 1, "Jonah": 4, "Micah": 7, "Nahum": 3,
    "Habakkuk": 3, "Zephaniah": 3, "Haggai": 2, "Zechariah": 14, "Malachi": 4,
    
    # New Testament
    "Matthew": 28, "Mark": 16, "Luke": 24, "John": 21, "Acts": 28,
    "Romans": 16, "1 Corinthians": 16, "2 Corinthians": 13, "Galatians": 6,
    "Ephesians": 6, "Philippians": 4, "Colossians": 4, "1 Thessalonians": 5,
    "2 Thessalonians": 3, "1 Timothy": 6, "2 Timothy": 4, "Titus": 3,
    "Philemon": 1, "Hebrews": 13, "James": 5, "1 Peter": 5, "2 Peter": 3,
    "1 John": 5, "2 John": 1, "3 John": 1, "Jude": 1, "Revelation": 22
}

def fetch_chapter_with_retry(book, chapter, max_retries=10):
    api_book_name = book.replace(" ", "+")
    # Using 'tl' (Tagalog Ang Biblia) translation parameter
    url = f"https://bible-api.com/{api_book_name}+{chapter}?translation=tl"
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = (attempt + 1) * 6
                print(f"    [!] Rate limited (429) on Tagalog {book} Ch {chapter}. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"    [x] HTTP Error {e.code} on Tagalog {book} Ch {chapter}. Retrying in 5s...")
                time.sleep(5)
        except Exception as e:
            print(f"    [!] Connection glitch: {e}. Retrying in 5s...")
            time.sleep(5)
    return None

def download_tagalog_to_pc():
    print(f"Starting Tagalog (Ang Biblia) download into '{OUTPUT_DIR}'...\n")
    
    for book, total_chapters in bible_books.items():
        print(f"Processing Tagalog: {book}...")
        
        for chapter in range(1, total_chapters + 1):
            file_slug = book.lower().replace(" ", "_")
            filename = os.path.join(OUTPUT_DIR, f"{file_slug}_ch{chapter}_tl.json")
            
            # Skip if already downloaded
            if os.path.exists(filename):
                continue

            data = fetch_chapter_with_retry(book, chapter)
            if not data:
                print(f"  [x] Permanently failed to download Tagalog {book} Ch {chapter}")
                continue
            
            verses = data.get("verses", [])
            formatted_json = []

            for i, v in enumerate(verses):
                text = v["text"].strip().replace("\n", " ")
                ref = f"{book} {v['chapter']}:{v['verse']} (TL)"
                
                item = {
                    "text": text,
                    "reference": ref
                }
                
                # Apply the same multi-verse connection rules
                if text.endswith(":") or text.endswith(","):
                    if i < len(verses) - 1:
                        item["connected_to"] = f"{book} {v['chapter']}:{v['verse'] + 1}"
                
                if i > 0 and (verses[i-1]["text"].strip().endswith(":") or verses[i-1]["text"].strip().endswith(",")):
                    item["connected_from"] = f"{book} {v['chapter']}:{v['verse'] - 1}"

                formatted_json.append(item)

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(formatted_json, f, indent=2, ensure_ascii=False)
            
            print(f"  [+] Saved Tagalog {file_slug}_ch{chapter}.json")
            
            # Safe pause interval to prevent 429 blocks
            time.sleep(1.2)

if __name__ == "__main__":
    download_tagalog_to_pc()
    print("\nDownload complete! All Tagalog files secured in 'tagalog_assets'.")
