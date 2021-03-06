# S3 Bucket Manager Telegram Bot

Simple telegram bot that allows upload, download and delete files on S3-compatible storage like [AWS S3](https://aws.amazon.com/s3/) and [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/).

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

#### Purge cache

> The Spaces API itself does not have support for purging the CDN’s cache, but the DigitalOcean platform API does. The Spaces API was designed to emulate the AWS S3 API so that developers could use it as a drop-in replacement for S3 existing projects. Spaces-specific functionality like the builtin CDN are not part of the S3 API but are support in the DigitalOcean API.

To be able to purge object from the edge caches, you need to obtain a DigitalOcean API token and add to `.env` file.

```
DIGITALOCEAN_TOKEN=77e027c7447f468068a7d4fea41e7149a75a94088082c66fcf555de3977f69d3
```

## Deploy/Run

Follow [instructions](https://core.telegram.org/bots#3-how-do-i-create-a-bot) to obtain a token, then paste token to `.env` file in form of `TELEGRAM_API_TOKEN=XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`.

```
docker-compose up -d --build
```

## Usage

```
/exist image.jpg
```

```
/delete image.jpg
```

```
/make_public image.jpg
```

```
/make_private image.jpg
```

```
/copy_file image.jpg assets/image.jpg
```

```
/list PREFIX LIMIT
```

```
/get_meta image.jpg
```

```
/purge_cache image.jpg
```

## TODO

* [x] Upload single file [up tp 20MB](https://core.telegram.org/bots/api#getfile)
* [x] Delete single file
* [x] Copy single file to another path on the same bucket
* [x] Change access level (make file private or public)
* [x] Check if file exist
* [x] List files by prefix
* [x] Get object metadata
* [x] Purge the cache (DigitalOcean Spaces)
* [ ] Purge the cache (AWS S3)

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
