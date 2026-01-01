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

You may see `ERROR:root:...404...` messages in the output - these are **expected** and not test failures. They come from tests that verify behavior for non-existent files (`test_file_exist_returns_false`, `test_get_meta_nonexistent`, `test_delete_file`).

A successful run looks like:

```
Ran 15 tests in 18.322s

OK
```
