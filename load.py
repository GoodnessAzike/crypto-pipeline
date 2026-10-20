#testing the cache
import os
import psycopg

from extract import extract

coins = extract()

db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:pw@localhost:5433/crypto")
conn = psycopg.connect(db_url)

inserted = 0

for coin in coins:
    cur = conn.execute(
        """
        INSERT INTO coin_prices (coin_id, symbol, name, price_usd, market_cap, source_updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (coin_id, source_updated_at) DO NOTHING
        """,
        (coin["id"], coin["symbol"], coin["name"], coin["current_price"], coin["market_cap"], coin["last_updated"]),
    )
    inserted += cur.rowcount

conn.commit()
conn.close()
print(inserted, "new rows,", len(coins) - inserted, "skipped as duplicates")