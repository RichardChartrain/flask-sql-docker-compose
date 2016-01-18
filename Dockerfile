FROM python:2.7-slim

MAINTAINER Ivan Gorbachev <ip0000h@gmail.com>

RUN apt-get update && apt-get install -qq -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libpq-dev \
    libsqlite3-dev \
    supervisor \
    sqlite3 \
&& apt-get purge -y --auto-remove \
    -o APT::AutoRemove::RecommendsImportant=false \
    -o APT::AutoRemove::SuggestsImportant=false $buildDeps \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/* \
&& easy_install pip

COPY ./app/requirements.txt ./requirements.txt
RUN pip install -U -r requirements.txt
