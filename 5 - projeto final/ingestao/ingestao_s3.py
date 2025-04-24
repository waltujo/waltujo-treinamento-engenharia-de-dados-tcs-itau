import awswrangler as wr
import pandas as pd
from datetime import datetime

S3_FILE_PATH = "s3://recepcao-taxa-de-juros/interest_rate.csv"

S3_PARQUET_PATH = "s3://walter-araujo-bucket-exemplo/interest_rate/"

DATABASE_NAME = "walter_araujo_database_sor"
TABLE_NAME = "interest_rate"

def main():
    df = wr.s3.read_csv(path=S3_FILE_PATH, dtype=str)

    df["data_ingestao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    wr.s3.to_parquet(
        df=df,
        path=S3_PARQUET_PATH,
        dataset=True,
        mode="overwrite",
        database=DATABASE_NAME,
        table=TABLE_NAME,
        dtype={col: "string" for col in df.columns}
    )

if __name__ == "__main__":
    from traceback import format_exc
    try:
        main()
    except Exception:
        print(format_exc())
        exit(1)
