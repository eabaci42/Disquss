import csv
import requests

# API anahtarlarınız ve forum kısa adınız
api_key = "YOUR_DISQUS_API_KEY"
forum_shortname = "YOUR_FORUM_SHORTNAME"

# CSV dosyası başlıkları ve dosya adı
headers = ['Thread ID', 'Title', 'Status', 'URL']
filename = "threads.csv"

def fetch_threads(cursor=None):
    """Forumdaki konuları Disqus API üzerinden çeker."""
    url = f"https://disqus.com/api/3.0/forums/listThreads.json?forum={forum_shortname}&api_key={api_key}&limit=100"
    if cursor:
        url += f"&cursor={cursor}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def read_existing_ids(filename):
    """CSV dosyasından mevcut konu ID'lerini okur."""
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_ids = {row['Thread ID'] for row in reader}
            return existing_ids
    except FileNotFoundError:
        return set()

def save_to_csv(threads, existing_ids, filename="threads.csv"):
    """Çekilen verileri CSV dosyasına kaydeder."""
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Dosya boşsa başlıkları yaz
            writer.writerow(headers)
        for thread in threads:
            if thread['id'] not in existing_ids:
                writer.writerow([thread['id'], thread['title'], "Open" if thread['isClosed'] == False else "Closed", thread['link']])

def main():
    existing_ids = read_existing_ids(filename)
    cursor = None
    while True:
        data = fetch_threads(cursor)
        if data and 'response' in data:
            threads = data['response']
            save_to_csv(threads, existing_ids, filename)
            # API'dan dönen "cursor" değerini kontrol edin
            if 'cursor' in data and data['cursor']['hasNext']:
                cursor = data['cursor']['next']
            else:
                print("Tüm konular işlendi veya sınır aşıldı.")
                break
        else:
            print("API'den veri çekilemedi.")
            break

if __name__ == "__main__":
    main()
