CREATE TABLE coin_prices (
    coin_id            TEXT NOT NULL,
    symbol             TEXT,
    name               TEXT,
    price_usd          NUMERIC,
    market_cap         BIGINT,
    source_updated_at  TIMESTAMPTZ NOT NULL,
    loaded_at          TIMESTAMPTZ DEFAULT now(),
    UNIQUE (coin_id, source_updated_at)
);

CREATE VIEW coin_prices_current AS
SELECT DISTINCT ON (coin_id)
    coin_id, symbol, name, price_usd, market_cap, source_updated_at
FROM coin_prices
ORDER BY coin_id, source_updated_at DESC;
