import requests
import os
import json
import csv 
from dotenv import load_dotenv

def fetch_data():
    load_dotenv()

    url = "https://imdb236.p.rapidapi.com/imdb/top250-movies"

    headers = {
        "x-rapidapi-key": os.getenv("MY_KEY"),
        "x-rapidapi-host": os.getenv("MY_HOST")
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Ensure the directory exists
        os.makedirs("data", exist_ok=True)

        file_path = r"data/top250movies.csv"
        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        return file_path

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error processing data: {e}")
        return None