import sqlite3
import polars as pl

def load_data(parquet_path, db_path):
    """Load data from Parquet file to SQLite database."""
    # Load parquet file
    df = pl.read_parquet(parquet_path)
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table with appropriate data types
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id TEXT PRIMARY KEY,
        url TEXT,
        primaryTitle TEXT,
        originalTitle TEXT,
        type TEXT,
        description TEXT,
        primaryImage TEXT,
        contentRating TEXT,
        startYear INTEGER,
        endYear INTEGER,
        releaseDate DATE,
        interests TEXT,
        countriesOfOrigin TEXT,
        externalLinks TEXT,
        spokenLanguages TEXT,
        filmingLocations TEXT,
        productionCompanies TEXT,
        budget REAL,
        grossWorldwide REAL,
        genres TEXT,
        isAdult INTEGER,
        runtimeMinutes INTEGER,
        averageRating REAL,
        numVotes INTEGER
    )
    ''')
    
    # Create essential indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON movies(primaryTitle)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_year ON movies(startYear)')
    
    # Convert to dictionary format for SQLite insertion
    records = df.to_dicts()
    columns = [col for col in df.columns if col in df.columns]
    placeholders = ', '.join(['?' for _ in columns])
    columns_str = ', '.join(columns)
    
    # Insert data
    batch_values = [[record.get(column) for column in columns] for record in records]
    cursor.executemany(
        f"INSERT OR REPLACE INTO movies ({columns_str}) VALUES ({placeholders})",
        batch_values
    )
    
    conn.commit()
    conn.close()
    
    return len(records)