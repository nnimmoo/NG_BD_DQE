import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Hardcoded file paths is not my usual get go but in this case I wanted to make sure that only one file is created correctly

input_csv = 'Here Hardcoded CSV file path' 
output_parquet = 'Hardcoded parquet file path'

# took chunk size of 250k as a good compromise between memory use and speed
chunk_size = 250000
writer = None

# Converting CSV to a single Parquet file using chunks so we wont brake memory

try:
    csv_stream = pd.read_csv(input_csv, chunksize=chunk_size, iterator=True)    
    first_chunk = next(csv_stream)    
    table = pa.Table.from_pandas(first_chunk)
    writer = pq.ParquetWriter(output_parquet, schema=table.schema)
    writer.write_table(table)
    for i, chunk in enumerate(csv_stream, start=2):
        table = pa.Table.from_pandas(chunk)
        writer.write_table(table)
        print(f"Wrote chunk {i} to file.")
finally:
    if writer:
        writer.close()
    print("Done")