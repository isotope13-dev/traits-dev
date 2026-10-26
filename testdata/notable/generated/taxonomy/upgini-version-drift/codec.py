def save(df, path):
    df.to_parquet(path, compression="gzip")
