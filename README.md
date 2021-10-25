# Repository Migrated to GitLab
See https://gitlab.com/aybry/collect_whalealerts for the latest (containerised) version of this project.

# Whalealert Transaction Collector
This is a script that fetches transactions from the [Whale Alert](whale-alert.io) API on a regular basis and adds any new transactions to your own database. This could be useful if you're looking to perform data analyses on large transactions, but need to gather the data first.

## Setup
You will need the following to get the script running:

- Whale Alert Account: Get a free account from [Whale Alert](https://whale-alert.io/about). Use your API key as the environment variable `WHALEALERT_API_KEY`.
- Database: Set up a PostgreSQL database (following [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04), for example). If you don't have a DigitalOcean account, feel free to sign up via this referral link: https://m.do.co/c/23d2dec5aec6.
- `.env` file: Create a file named `.env`, and enter your database credentials into it. The file requires the following credentials:

```
PG_WHALEALERT_HOST=**********
PG_WHALEALERT_PORT=**********
PG_WHALEALERT_DBNAME=**********
PG_WHALEALERT_USER=**********
PG_WHALEALERT_PASSWORD=**********
WHALEALERT_API_KEY=**********
```

### Virtual Environment
This project uses Poetry as the dependency/package manager for Python.

To start the script without Docker, run the following shell commands:

```
# Use .env file to access environment variables
set -o allexport
source .env

# Set up poetry
pip install poetry
poetry install

poetry run python fetch_transactions.py
```
