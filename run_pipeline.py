from src.data_transform import clean_data
from src.db_loader import  load_data
from src.web_scraper import fetch_data

def run_etl_pipeline():
    try:
        # Step 1: Extract
        raw_data = fetch_data()
        print (raw_data)
        
        # Step 2: Transform
        transformed_data = clean_data(raw_data)
        print(transformed_data)

        # Step 3: Load
        load_data(r'data\processed_data.parquet', r'data\movies.db')
        print("ETL pipeline executed successfully.")

    except Exception as e:
        print(f"Error occurred: {e}")

# Run the ETL pipeline
run_etl_pipeline()



