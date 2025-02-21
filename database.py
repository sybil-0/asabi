
import sqlite3
import os
import time

def create_database(db_path="file_data.db"):
    """Creates a SQLite database with a table for storing file metadata."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filepath TEXT,
            creation_date TEXT,
            size INTEGER,
            filetype TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_file_data(db_path, file_data):
    """Inserts file metadata into the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO files (filename, filepath, creation_date, size, filetype)
        VALUES (?, ?, ?, ?, ?)
    ''', file_data)
    conn.commit()
    conn.close()

def scan_directory(directory, db_path="file_data.db"):
    """Scans a given directory and stores file metadata in the database."""
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for root, _, files in os.walk(directory):
        try:
            for file in files:
                filepath = os.path.join(root, file)
                creation_date = time.ctime(os.path.getctime(filepath))
                size = os.path.getsize(filepath)
                filetype = os.path.splitext(file)[-1].lower()
                
                cursor.execute('''
                    INSERT INTO files (filename, filepath, creation_date, size, filetype)
                    VALUES (?, ?, ?, ?, ?)
                ''', (file, filepath, creation_date, size, filetype))
        except Exception as e:
            print(e)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    directory_to_scan = "/home/kevinh"  # Change this to your target directory
    scan_directory(directory_to_scan)
