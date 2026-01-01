# S3 Bucket Manager Telegram Bot

Simple telegram bot that allows upload, download and delete files on S3-compatible storage like [AWS S3](https://aws.amazon.com/s3/), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), and [Cloudflare R2](https://www.cloudflare.com/products/r2/).

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

### [Cloudflare R2](https://www.cloudflare.com/products/r2/)

Minimal sample `.env` file:

```
TELEGRAM_API_TOKEN=0000000000:AAFBxO9f3HELPkYvaiww0LiNcj6DB-R2d2Q
TELEGRAM_USERNAME=durov
AWS_SERVER_PUBLIC_KEY=a1b2c3d4e5f6g7h8i9j0
AWS_SERVER_SECRET_KEY=1234567890abcdef1234567890abcdef12345678
AWS_REGION=auto
ENDPOINT_URL=https://0123456789abcdef0123456789abcdef.r2.cloudflarestorage.com
BUCKET_NAME=myuploads
# For production, use custom domain:
CUSTOM_ENDPOINT_URL=https://cdn.example.com
# For development, use R2 public dev URL (rate-limited):
# CUSTOM_ENDPOINT_URL=https://pub-0123456789abcdef.r2.dev
```

Get R2 API credentials from [Cloudflare Dashboard](https://dash.cloudflare.com/) → Storage & databases → R2 object storage → Overview → Manage R2 API Tokens.

#### Limitations

R2 is [S3-compatible](https://developers.cloudflare.com/r2/api/s3/api/) but does **not** implement object-level ACL operations:

| Operation | Status | Affected Command |
|-----------|--------|------------------|
| `GetObjectAcl` | Not implemented | - |
| `PutObjectAcl` | Not implemented | `/make_public`, `/make_private` |

Public access in R2 is managed at the bucket level via [R2 Public Buckets](https://developers.cloudflare.com/r2/buckets/public-buckets/), not per-object ACLs. For development, you can enable the Public Development URL (e.g., `https://pub-xxx.r2.dev`) in bucket Settings → Public Development URL. This URL is rate-limited and not recommended for production.

## Deploy/Run

Follow [instructions](https://core.telegram.org/bots#3-how-do-i-create-a-bot) to obtain a token, then paste token to `.env` file in form of `TELEGRAM_API_TOKEN=XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`.

Run `make help` to see all available commands.

```
make build   # Build Docker image
make upd     # Start the bot (detached)
make logs    # Show bot logs
make down    # Stop the bot
```

## Testing

Run integration tests (requires S3 credentials in `.env`):

```
make test
```

Note: ACL-related tests are automatically skipped on storage providers that don't support object-level ACLs (e.g., Cloudflare R2).

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
* [ ] Purge the cache (Cloudflare R2)

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
