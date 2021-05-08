# Whalealert Transaction Collector
This is a script that fetches transactions from the [Whale Alert](whale-alert.io) API on a regular basis and adds any new transactions to your own database. This could be useful if you're looking to perform data analyses on large transactions, but need to gather the data first.

## Setup
The following steps should cover (almost) everything you need to get it running. Get in touch if you are stuck.

### Whale Alert Account
Head over to [Whale Alert](https://whale-alert.io/about) and create a free account. The free plan is sufficient for this script. Create an API key from your account and use this as `WHALEALERT_API_KEY` in the step **Environment Variables** below.

### Database
Set up a PostgreSQL database (following [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04), for example). Use the credentials for this in the next step.

Create a database named `whalealert` and a user named `whalealert`.

### Environment Variables
Add the following lines (replace the `xxx`s) to your `~/.bashrc`:

```
export PG_WHALEALERT_HOST=xxxxxxxx
export PG_WHALEALERT_PORT=xxxxxxxx
export PG_WHALEALERT_PASSWORD=xxxxxxxx
export WHALEALERT_API_KEY=xxxxxxxx
```

### Python Environment
Create a virtual environment for this repo. I used Anaconda.

```
conda create -y -n whalealert --file requirements.txt
```

Activate the environment and start the script.

```
conda activate whalealert
python fetch_transactions.py
```

## Recommendations
If you are running this on a server, use [Screen](https://linuxize.com/post/how-to-use-linux-screen/). This allows you to leave terminal screens running in the background, and return to them when necessary (e.g. if you want to kill the process with `Ctrl+C`).

Create a Screen for this process before starting the script:

```
screen -S whalealert
conda activate whalealert
python fetch_transactions.py
```

Then press `Ctrl+A Ctrl+D` to detach from this screen and leave it running in the background.

Should you want to return to this screen, type:

```
screen -r whalealert
```
