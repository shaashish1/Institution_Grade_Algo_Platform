import sqlite3
from tvDatafeed import TvDatafeed
import logging
import getpass

# Setup logging
logging.basicConfig(level=logging.INFO)

# Prompt for TradingView credentials
username = input("ashish.sharma14@gmail.com")
password = getpass.getpass("BlockTrade5$")

# Initialize tvDatafeed with login
tv = TvDatafeed(username=username, password=password)

# List of exchanges to fetch symbols for
exchanges = ['NSE', 'BSE', 'MCX', 'NASDAQ', 'NYSE']

# Connect to SQLite database
conn = sqlite3.connect('tv_symbols.db')
cursor = conn.cursor()

# Create table for each exchange
def create_table(exchange):
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{exchange}" (
            symbol TEXT PRIMARY KEY,
            full_name TEXT,
            description TEXT
        )
    ''')

# Insert symbols into respective exchange table
def insert_symbols(exchange, symbols):
    for symbol in symbols:
        try:
            cursor.execute(f'''
                INSERT OR IGNORE INTO "{exchange}" (symbol, full_name, description)
                VALUES (?, ?, ?)
            ''', (
                symbol.get('symbol', ''),
                symbol.get('full_name', ''),
                symbol.get('description', '')
            ))
        except Exception as e:
            logging.error(f"Error inserting symbol into {exchange}: {e}")

# Fetch and store symbols
for exchange in exchanges:
    try:
        logging.info(f"Fetching symbols for {exchange}...")
        symbols = tv.search_symbol('', exchange)
        create_table(exchange)
        insert_symbols(exchange, symbols)
        logging.info(f"Stored {len(symbols)} symbols in {exchange} table.")
    except Exception as e:
        logging.error(f"Failed to fetch symbols for {exchange}: {e}")

# Finalize
conn.commit()
conn.close()
print("✅ Symbol data stored in tv_symbols.db.")
