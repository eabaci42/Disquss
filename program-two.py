"""
import csv
import requests
import tempfile
import shutil

# API anahtarlarınız, erişim jetonunuz ve forum kısa adınız
api_key = "9gRlESJ9oW45wgQXf9tq7b3scy544yYTpoCwAHKVWv7MgWohbaYF7nzBM3dt5qxH"
access_token = "5e2d90bdb65b42e89d0e54499a6cfe57"
forum_shortname = "atikrost"

# CSV dosyası adı
filename = "ccclosed.csv"

def open_thread(thread_id):
    #Kapalı bir konuyu Disqus API kullanarak açar.
    url = f"https://disqus.com/api/3.0/threads/open.json"
    data = {
        'api_key': api_key,
        'access_token': access_token,
        'thread': thread_id
    }
    response = requests.post(url, data=data)
    return response.status_code == 200

def update_csv(filename):
    #CSV dosyasını okur, kapalı konuları açar ve CSV'de günceller.
    # Geçici bir dosya oluştur
    tempfile_name = tempfile.mktemp()
    with open(filename, mode='r', newline='', encoding='utf-8') as infile, open(tempfile_name, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row['Status'] == 'Closed':
                if open_thread(row['Thread ID']):
                    row['Status'] = 'Open'
                    print(f"Thread {row['Thread ID']} opened successfully.")
                else:
                    print(f"Failed to open thread {row['Thread ID']}.")
            writer.writerow(row)

    # Orijinal CSV dosyasını güncellenmiş verilerle değiştir
    shutil.move(tempfile_name, filename)

def main():
    update_csv(filename)

if __name__ == "__main__":
    main()
 """







import csv
import requests
import tempfile
import shutil
import sys

# Replace these with your actual Disqus API credentials and forum shortname
API_KEY = "YOUR_DISQUS_API_KEY"
ACCESS_TOKEN = "YOUR_DISQUS_ACCESS_TOKEN"
FORUM_SHORTNAME = "YOUR_FORUM_SHORTNAME"

def open_thread(thread_id):
    """Opens a closed thread using the Disqus API."""
    url = "https://disqus.com/api/3.0/threads/open.json"
    data = {
        'api_key': API_KEY,
        'access_token': ACCESS_TOKEN,
        'thread': thread_id
    }
    response = requests.post(url, data=data)
    return response.status_code == 200

def update_csv(filename):
    """Reads a CSV file, opens closed threads using the Disqus API, and updates the CSV."""
    # Create a temporary file
    tempfile_name = tempfile.mktemp()
    with open(filename, mode='r', newline='', encoding='utf-8') as infile, open(tempfile_name, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row['Status'] == 'Closed':
                if open_thread(row['Thread ID']):
                    row['Status'] = 'Open'
                    print(f"Thread {row['Thread ID']} opened successfully.")
                else:
                    print(f"Failed to open thread {row['Thread ID']}.")
            writer.writerow(row)

    # Replace the original CSV file with the updated data
    shutil.move(tempfile_name, filename)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_csv_path>")
        sys.exit(1)
    
    input_csv_path = sys.argv[1]
    print(f"Processing '{input_csv_path}' to open closed threads...")
    update_csv(input_csv_path)
    print("Done.")

if __name__ == "__main__":
    main()
