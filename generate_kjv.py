import os
import json
import urllib.request
import time

# Output directory on your PC
OUTPUT_DIR = "./kjv_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Complete KJV Bible Books & Chapter Counts
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

def download_kjv_to_pc():
    print(f"Starting KJV download into '{OUTPUT_DIR}' folder on your PC...\n")
    
    for book, total_chapters in bible_books.items():
        print(f"Downloading {book} ({total_chapters} chapters)...")
        
        for chapter in range(1, total_chapters + 1):
            api_book_name = book.replace(" ", "+")
            url = f"https://bible-api.com/{api_book_name}+{chapter}?translation=kjv"
            
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode())
                
                verses = data.get("verses", [])
                formatted_json = []

                for i, v in enumerate(verses):
                    text = v["text"].strip().replace("\n", " ")
                    ref = f"{book} {v['chapter']}:{v['verse']} (KJV)"
                    
                    item = {
                        "text": text,
                        "reference": ref
                    }
                    
                    # Apply your multi-verse connection rules
                    if text.endswith(":") or text.endswith(","):
                        if i < len(verses) - 1:
                            item["connected_to"] = f"{book} {v['chapter']}:{v['verse'] + 1}"
                    
                    if i > 0 and (verses[i-1]["text"].strip().endswith(":") or verses[i-1]["text"].strip().endswith(",")):
                        item["connected_from"] = f"{book} {v['chapter']}:{v['verse'] - 1}"

                    formatted_json.append(item)

                file_slug = book.lower().replace(" ", "_")
                filename = os.path.join(OUTPUT_DIR, f"{file_slug}_ch{chapter}_kjv.json")
                
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(formatted_json, f, indent=2, ensure_ascii=False)
                
                time.sleep(0.05) # Gentle pause for smooth downloading
                
            except Exception as e:
                print(f"  [x] Error downloading {book} Ch {chapter}: {e}")

if __name__ == "__main__":
    download_kjv_to_pc()
    print("\nDownload complete! Check the 'kjv_assets' folder on your computer.")
