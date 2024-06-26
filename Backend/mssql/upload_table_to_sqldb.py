from sqlalchemy import create_engine, text, Integer, Float, NVARCHAR
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import pyodbc
import os
from urllib.parse import quote_plus
import pandas as pd
import pdb

load_dotenv()
user = quote_plus(os.getenv('DB_USER'))
passwd = quote_plus(os.getenv('DB_PASS'))
server = 'maldb.database.windows.net:1433' 
database = 'MAL SQL'
driver = 'ODBC+Driver+17+for+SQL+Server'

connection_string = f'mssql+pyodbc://{user}:{passwd}@{server}/{database}?driver={driver}&Encrypt=yes&TrustServerCertificate=no'
# connection_string = f"mssql+pymssql://{user}:{passwd}@{server}/{database}"
engine = create_engine(connection_string, connect_args={"timeout":30}, fast_executemany=True)
connection = engine.connect()

# testing: 

result = connection.execute(text("SELECT 1"))
for row in result:
    print(row)

# Prepare table for upload
# Get table
cosine_sim_mat = pd.read_csv('/Users/giulianotissot/Desktop/Cs_folders/MAL/MAL/Temp_data/cosine_sim_mat.csv', index_col=0)
# Reshape to long format
long_format = cosine_sim_mat.melt(ignore_index=False)
long_format.reset_index(inplace=True)
long_format.columns = ['Anime_x', 'Anime_y', 'similarity_score']
print("Filtering out the 0s")
# Filter out unecessary similarities
long_format = long_format[long_format['similarity_score'] > 0.0]
print(long_format.shape)
create_table_query = """
CREATE TABLE CosineSimilarity (
    Anime_x NVARCHAR(255),
    Anime_y NVARCHAR(255),
    similarity_score FLOAT,
    PRIMARY KEY (Anime_x, Anime_y)
);
"""

insert_test = """
INSERT INTO CosineSimilarity VALUES ('anime_1', 'anime_2', 0.7)"""
print("executing query")
connection.execute(text(create_table_query))
print("table succesfully created")

connection.execute(text(insert_test))
connection.commit()
connection.close()

def create_anime_id(df, engine):
    anime_name_list = list(df.columns)
    # Map list to index
    anime_id_list = [(anime_name, index + 1) for index, anime_name in enumerate(anime_name_list)]
    
    # Create Table sql statement
    anime_id_df = pd.DataFrame(anime_id_list, columns=['anime_name', 'anime_id'])

    # Create table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS AnimeIDs (
        anime_id INT PRIMARY KEY,
        anime_name NVARCHAR(255) UNIQUE
    );
    """

    # Execute the CREATE TABLE statement
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            connection.execute(text(create_table_sql))
            trans.commit()
        except Exception as e:
            trans.rollback()
            print(f"Error creating table: {e}")

    # Upload data to the table
    try:
        with engine.connect() as connection:
            anime_id_df.to_sql('AnimeIDs', connection, if_exists='append', index=False, dtype={
                'anime_id': Integer(),
                'anime_name': NVARCHAR(255)
            })
        print("Anime IDs table created and data uploaded successfully.")
    except SQLAlchemyError as e:
        print(f"Error uploading anime IDs: {e}")

create_anime_id(long_format, engine)

def upload_batch(batch, engine):
    try:
        with engine.connect() as connection:
            raw_connection = connection.connection
            if isinstance(raw_connection, pyodbc.Connection):
                raw_connection.fast_executemany = True
            batch.to_sql('SimilarityScores', connection, if_exists='append', index=False, dtype={
                'Anime_x': NVARCHAR(255),
                'Anime_y': NVARCHAR(255),
                'similarity_score': Float()
            })
        return True
    except SQLAlchemyError as e:
        print(f"Error uploading batch: {e}")
        return False


# Function to monitor and upload batches
def upload_with_monitoring(data, batch_size, engine):
    total_batches = len(data) // batch_size + (1 if len(data) % batch_size != 0 else 0)
    start_batch = 0

    # Read progress from log file if exists
    try:
        with open("upload_progress.log", "r") as f:
            start_batch = int(f.readline().strip())
    except FileNotFoundError:
        pass

    for batch_number in range(start_batch, total_batches):
        start_index = batch_number * batch_size
        end_index = start_index + batch_size
        batch = data.iloc[start_index:end_index]

        success = upload_batch(batch, engine)
        if success:
            # Log progress
            with open("upload_progress.log", "w") as f:
                f.write(str(batch_number + 1))
            print(f"Batch {batch_number + 1}/{total_batches} uploaded successfully.")
        else:
            print(f"Batch {batch_number + 1}/{total_batches} failed. Exiting.")
            break