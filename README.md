# Crypto price pipeline

A small batch pipeline that pulls live crypto prices from the CoinGecko API and loads them into Postgres, safe to run as often as you like. Built step by step as a learning project, heading for a production-style setup on AWS.

## What it does today

```
CoinGecko API  ──►  extract.py  ──►  load.py  ──►  Postgres (coin_prices)
                    (Python, run in Docker; Postgres in a second container)
```

- **Extract:** calls CoinGecko's `/coins/markets` for the top 10 coins by markets cap, priced in USD.
- **Load:** inserts each coin's price into `coin_prices`, with CoinGecko's own `last_updated` time as `source_updated_at`.
- **Latest price:** `coin_prices_current` (a view) shows the most recent price for each coin.
- **Safe to rerun:** `coin_prices` has a unique key on `(coin_id, source_updated_at)`, and inserts use `ON CONFLICT DO NOTHING`. Running twice in a row adds nothing new, and a later run adds only prices CoinGecko has updated since.

## Run it

Needs Docker.

```bash
docker compose up --build --abort-on-container-exit
```

Compose starts Postgres, waits until it's ready (a health check runs `pg_isready`), then runs the pipeline once. Run it again with:

```bash
docker compose run --rm pipeline
```

Each run prints how many rows were new and how many were skipped as duplicates.

## Design choices

| Choice | Why |
|---|---|
| Store the source's timestamp, not just the fetch time | It's what tells a new price apart from the same price fetched twice, and it shows how fresh the data is. |
| Unique key + `ON CONFLICT DO NOTHING` | Schedules fire twice and failed runs get retried. The data should never double. |
| `depends_on` with `service_healthy` | A started container isn't a ready database. The pipeline waits for Postgres to accept connections. |
| Database URL from an environment variable | The same image runs anywhere. Only the setting changes. |

## Roadmap

The goal is to answer a question: **can you trust one free source for a crypto price?**

- [ ] Add Coinbase and Kraken prices, and convert everything to GBP (Frankfurter)
- [ ] Keep the raw API responses, and use numbered migrations instead of one setup file
- [ ] dbt models and data tests: disagreement between sources, freshness, reliability
- [ ] Run on AWS: Terraform, ECR, ECS Fargate on a schedule, RDS Postgres, Secrets Manager, S3
- [ ] CloudWatch logs and alerts, and GitHub Actions deploys with OIDC
- [ ] Run for 30 days and publish the answer, with what it cost

## Notes

The Postgres password in `compose.yaml` is for a database on your laptop only. Real secrets (API keys, cloud database passwords) never go in this repo.

Check before committing:
- Does your extract call /coins/markets?
- Are coin_id and source_updated_at your real column names?
- Does it print "new rows" and "skipped"? Your output says it does.