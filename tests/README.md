# Integration Tests

S3 integration tests for the bucket manager bot.

## Requirements

- Docker
- Valid S3 credentials in `.env` file (AWS_SERVER_PUBLIC_KEY, AWS_SERVER_SECRET_KEY, BUCKET_NAME, etc.)

## Running Tests

```bash
docker-compose --profile test run --rm test
```

## How It Works

- All test files are created under the `tests/` prefix on S3
- File names are generated with UUIDs to avoid conflicts
- Files are automatically cleaned up after each test via `tearDown()`

## Expected Output

You may see `ERROR:root:...404...` or `ERROR:root:...NotImplemented...` messages in the output - these are **expected** and not test failures. The 404 errors come from tests that verify behavior for non-existent files. The NotImplemented errors come from storage providers that don't support ACL operations (e.g., Cloudflare R2).

A successful run on AWS S3 or DigitalOcean Spaces:

```
Ran 15 tests in 18.322s

OK
```

A successful run on Cloudflare R2 (ACL tests skipped):

```
Ran 15 tests in 14.263s

OK (skipped=3)
```

The skipped tests are ACL-related (`test_make_public`, `test_make_private`, `test_copy_file_preserves_acl`) which are not supported by R2.
