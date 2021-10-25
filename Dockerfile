FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1

RUN apt-get update \
    && apt-get install -y \
    gcc \
    libpq-dev \
    libmagic1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN POETRY_VIRTUALENVS_CREATE=false \
    poetry install --no-interaction --no-ansi

COPY . $APP_HOME

CMD [ "python", "fetch_transactions.py" ]
