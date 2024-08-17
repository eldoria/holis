import pandas as pd
from sqlalchemy import create_engine

# Load CSV file into a DataFrame
df = pd.read_csv('../part_1/data_pre_processing/BI_2.02__06_CatImpacts_Details.csv')

# Create PostgreSQL engine (replace with your credentials)
engine = create_engine('postgresql+psycopg2://myuser:password@localhost:5432/mydatabase')

# Write DataFrame to SQL table
df.to_sql('table_name', engine, if_exists='replace', index=False)
