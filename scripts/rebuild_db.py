"""
Rebuild library.db from books_metadata.csv.
Run from the repo root:  python scripts/rebuild_db.py
"""
import csv
import os
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "books_metadata.csv"
DB_PATH = REPO_ROOT / "data" / "database" / "library.db"


def main():
    if not CSV_PATH.exists():
        print(f"[ERROR] CSV not found: {CSV_PATH}")
        return

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute("""
        CREATE TABLE books (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            title         TEXT    NOT NULL,
            author        TEXT    NOT NULL,
            subject_tags  TEXT,
            category      TEXT    DEFAULT 'General',
            language      TEXT    DEFAULT 'English',
            file_path     TEXT    NOT NULL,
            word_count    INTEGER DEFAULT 0,
            file_size_bytes INTEGER DEFAULT 0
        )
    """)

    added = 0
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            file_path = row.get("file_path", "").strip()
            resolved = REPO_ROOT / file_path
            if not resolved.exists():
                alt = REPO_ROOT / "data" / "cleaned" / Path(file_path).name
                if alt.exists():
                    file_path = str(alt.relative_to(REPO_ROOT))

            cursor.execute("""
                INSERT INTO books (title, author, subject_tags, category, language, file_path, word_count, file_size_bytes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row.get("title", "Unknown").strip(),
                row.get("author", "Unknown").strip(),
                row.get("subject_tags", "").strip(),
                row.get("category", "General").strip() or "General",
                row.get("language", "English").strip() or "English",
                file_path,
                int(row.get("wordcount", 0) or 0),
                int(row.get("filesize_bytes", 0) or 0),
            ))
            added += 1
            print(f"  + {row.get('title', '?')} by {row.get('author', '?')}")

    conn.commit()
    conn.close()
    print(f"\nDone. {added} books written to {DB_PATH}")


if __name__ == "__main__":
    main()
