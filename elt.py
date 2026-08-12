import requests
import psycopg2
from datetime import datetime

DB_HOST = "localhost"
DB_NAME = "weather_db"
DB_USER = "admin"
DB_PASS = "adminpassword"

def create_table_if_not_exists(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS crypto_prices (
        id SERIAL PRIMARY KEY,
        coin_name VARCHAR(50),
        symbol VARCHAR(50),
        price_usd DECIMAL,
        inserted_at TIMESTAMP
    );
    """
    cursor.execute(create_table_query)

def extract_data():
    # using binance api (NO DNS blocks )
    print("Extracting data from Binance API...")
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()[:10] # Top 10 coins
    else:
        print("API failed!")
        return []

def load_data(data):
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = conn.cursor()
        create_table_if_not_exists(cursor)
        
        insert_query = """
        INSERT INTO crypto_prices (coin_name, symbol, price_usd, inserted_at)
        VALUES (%s, %s, %s, %s)
        """
        
        print("Loading data into PostgreSQL...")
        for coin in data:
            # Binance fetch  'price' and 'symbol' 
            price = round(float(coin['price']), 2) 
            current_time = datetime.now()
            
            # Name and Symbol two of  coin['symbol'] (e.g., BTCUSDT)
            cursor.execute(insert_query, (coin['symbol'], coin['symbol'], price, current_time))
            
        conn.commit()
        print("Successfully loaded 10 records into the database!")
        
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == "__main__":
    raw_data = extract_data()
    if raw_data:
        load_data(raw_data)
