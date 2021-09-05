# S3 Bucket Manager Telegram Bot

Simple telegram bot that allows upload, ~~download and delete~~ files on S3-compatible storage like [AWS S3](https://aws.amazon.com/s3/) and [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/).

Built on top of [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

## Configuration

### [AWS S3](https://aws.amazon.com/s3/)

Minimal sample `.env` file:

```
TELEGRAM_API_TOKEN=0000000000:AAFBxO9f3HELPkYvaiww0LiNcj6DB-R2d2Q
TELEGRAM_USERNAME=durov
AWS_SERVER_PUBLIC_KEY=AKIAQWERTY4BLSCYBT36
AWS_SERVER_SECRET_KEY=7b79ipOp8sDqycbY4dVSd28TQyaNzyT99PpLJrGO
AWS_REGION=us-east-1
BUCKET_NAME=myuploads
```

### [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/)

Minimal sample `.env` file:

```
TELEGRAM_API_TOKEN=0000000000:AAFBxO9f3HELPkYvaiww0LiNcj6DB-R2d2Q
TELEGRAM_USERNAME=durov
AWS_SERVER_PUBLIC_KEY=DTDINKIYJMAKAUTOEIWV
AWS_SERVER_SECRET_KEY=LBa9U+XUtg7fngBBQuOWXpSgOLULJTk0iaXERS+mlYA
AWS_REGION=ams3
ENDPOINT_URL=https://ams3.digitaloceanspaces.com
CUSTOM_ENDPOINT_URL=https://cdn.example.com
BUCKET_NAME=myuploads
```

## Usage

Follow [instructions](https://core.telegram.org/bots#3-how-do-i-create-a-bot) to obtain a token, then paste token to `.env` file in form of `TELEGRAM_API_TOKEN=XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`.

```
docker-compose up -d --build
```

## TODO

* [x] Upload single file [up tp 20MB](https://core.telegram.org/bots/api#getfile)
* [ ] Delete single file
* [ ] Change access level (make file private or public)
* [ ] List files by pattern

## Development notes

### Update python-telegram-bot (pipenv)

```
cd s3_bucket_bot
pipenv update python-telegram-bot
```

or

```
cd s3_bucket_bot
/usr/local/opt/pipenv/bin/pipenv update python-telegram-bot
```

### Update virtual env (pip)

```
cd s3_bucket_bot
pip install python-telegram-bot --upgrade
```

#### Lock requirements

```

/usr/local/opt/pipenv/bin/pipenv lock --requirements > requirements.txt
```
