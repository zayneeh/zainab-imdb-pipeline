import polars as pl

def clean_data(file_path: str) -> pl.DataFrame:
    # Load data
    df = pl.read_csv(file_path)
    
    # Clean text columns
    text_columns = ["id", "primaryTitle", "originalTitle", "description", 
                   "productionCompanies", "filmingLocations"]
    text_cols = [col for col in text_columns if col in df.columns]
    if text_cols:
        df = df.with_columns([
            pl.col(col).cast(pl.Utf8).str.replace_all(r'^\s+|\s+$', '') for col in text_cols
        ])
    
    # Convert numeric columns
    num_cols = ["startYear", "endYear", "budget", "grossWorldwide", 
               "runtimeMinutes", "averageRating", "numVotes"]
    num_cols = [col for col in num_cols if col in df.columns]
    if num_cols:
        df = df.with_columns([pl.col(col).cast(pl.Float64, strict=False) for col in num_cols])
    
    # Parse date column 
    if "releaseDate" in df.columns:
        try:
            df = df.with_column(pl.col("releaseDate").str.to_date("%Y-%m-%d", strict=False))
        except:
            pass  
    # Remove duplicates with id
    if "id" in df.columns:
        df = df.unique(subset=["id"], keep="first")

    # Save cleaned DataFrame to a Parquet file inside the function
    df.write_parquet(r'data\processed_data.parquet')
    
    return df