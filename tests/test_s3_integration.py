"""
Integration tests for S3 bucket operations.

These tests require valid S3 credentials in environment variables.
All test files are created under the 'tests/' prefix on S3 and cleaned up after each test.

Run with: python -m unittest tests.test_s3_integration -v
"""

import unittest
import uuid
import os
from s3_bucket_bot.s3bucket import (
    upload_file,
    delete_file,
    file_exist,
    copy_file,
    make_public,
    make_private,
    get_file_acl,
    list_files,
    get_meta,
    get_obj_url,
    BUCKET_NAME,
    AWS_SERVER_PUBLIC_KEY,
    ACLNotSupportedError,
)


def generate_test_path(extension='txt'):
    """Generate a unique test file path under tests/ prefix."""
    return f'tests/{uuid.uuid4()}.{extension}'


def check_acl_support():
    """Check if the storage provider supports ACL operations."""
    local_file = f'/tmp/{uuid.uuid4()}.txt'
    s3_path = generate_test_path('txt')

    try:
        # Create a test file
        with open(local_file, 'w') as f:
            f.write('acl test')
        upload_file(local_file, s3_path, 'text/plain', 'private')

        # Try to get ACL - returns None if not supported
        acl = get_file_acl(s3_path)
        return acl is not None
    except ACLNotSupportedError:
        return False
    finally:
        # Cleanup
        try:
            os.unlink(local_file)
        except OSError:
            pass
        try:
            delete_file(s3_path)
        except Exception:
            pass


class TestS3Integration(unittest.TestCase):
    """Integration tests for S3 operations."""

    # Track files created during tests for cleanup
    created_files = []

    @classmethod
    def setUpClass(cls):
        """Check that S3 credentials are configured."""
        if not AWS_SERVER_PUBLIC_KEY:
            raise unittest.SkipTest('S3 credentials not configured. Set AWS_SERVER_PUBLIC_KEY.')
        if not BUCKET_NAME:
            raise unittest.SkipTest('BUCKET_NAME not configured.')
        # Check if the storage provider supports ACL operations
        cls.acl_supported = check_acl_support()

    def setUp(self):
        """Reset created files list before each test."""
        self.created_files = []

    def tearDown(self):
        """Clean up any files created during the test."""
        for file_path in self.created_files:
            try:
                if file_exist(file_path):
                    delete_file(file_path)
            except Exception as e:
                print(f'Warning: Failed to clean up {file_path}: {e}')

    def create_test_file(self, content='test content'):
        """Create a local temporary file for upload testing."""
        tmp_path = f'/tmp/{uuid.uuid4()}.txt'
        with open(tmp_path, 'w') as f:
            f.write(content)
        return tmp_path

    def track_s3_file(self, s3_path):
        """Track an S3 file for cleanup after test."""
        self.created_files.append(s3_path)

    # --- Upload Tests ---

    def test_upload_file(self):
        """Test basic file upload."""
        local_file = self.create_test_file('Hello, S3!')
        s3_path = generate_test_path('txt')
        self.track_s3_file(s3_path)

        result = upload_file(local_file, s3_path, 'text/plain', 'public-read')

        self.assertTrue(result)
        self.assertTrue(file_exist(s3_path))

        # Cleanup local file
        os.unlink(local_file)

    def test_upload_file_private(self):
        """Test file upload with private ACL."""
        local_file = self.create_test_file('Private content')
        s3_path = generate_test_path('txt')
        self.track_s3_file(s3_path)

        result = upload_file(local_file, s3_path, 'text/plain', 'private')

        self.assertTrue(result)
        self.assertTrue(file_exist(s3_path))
        if self.acl_supported:
            self.assertEqual(get_file_acl(s3_path), 'private')

        os.unlink(local_file)

    # --- File Exist Tests ---

    def test_file_exist_returns_true(self):
        """Test file_exist returns True for existing file."""
        local_file = self.create_test_file()
        s3_path = generate_test_path('txt')
        self.track_s3_file(s3_path)

        upload_file(local_file, s3_path, 'text/plain', 'private')

        self.assertTrue(file_exist(s3_path))

        os.unlink(local_file)

    def test_file_exist_returns_false(self):
        """Test file_exist returns False for non-existing file."""
        s3_path = f'tests/nonexistent-{uuid.uuid4()}.txt'

        self.assertFalse(file_exist(s3_path))

    # --- Delete Tests ---

    def test_delete_file(self):
        """Test file deletion."""
        local_file = self.create_test_file()
        s3_path = generate_test_path('txt')
        # Don't track - we're testing deletion

        upload_file(local_file, s3_path, 'text/plain', 'private')
        self.assertTrue(file_exist(s3_path))

        delete_file(s3_path)

        self.assertFalse(file_exist(s3_path))

        os.unlink(local_file)

    # --- ACL Tests ---

    def test_make_public(self):
        """Test making a file public."""
        if not self.acl_supported:
            self.skipTest('ACL operations not supported by storage provider')

        local_file = self.create_test_file()
        s3_path = generate_test_path('txt')
        self.track_s3_file(s3_path)

        upload_file(local_file, s3_path, 'text/plain', 'private')
        self.assertEqual(get_file_acl(s3_path), 'private')

        make_public(s3_path)

        self.assertEqual(get_file_acl(s3_path), 'public-read')

        os.unlink(local_file)

    def test_make_private(self):
        """Test making a file private."""
        if not self.acl_supported:
            self.skipTest('ACL operations not supported by storage provider')

        local_file = self.create_test_file()
        s3_path = generate_test_path('txt')
        self.track_s3_file(s3_path)

        upload_file(local_file, s3_path, 'text/plain', 'public-read')
        self.assertEqual(get_file_acl(s3_path), 'public-read')

        make_private(s3_path)

        self.assertEqual(get_file_acl(s3_path), 'private')

        os.unlink(local_file)

    # --- Copy Tests ---

    def test_copy_file(self):
        """Test copying a file."""
        local_file = self.create_test_file('Copy me!')
        src_path = generate_test_path('txt')
        dest_path = generate_test_path('txt')
        self.track_s3_file(src_path)
        self.track_s3_file(dest_path)

        upload_file(local_file, src_path, 'text/plain', 'public-read')

        result = copy_file(src_path, dest_path)

        self.assertTrue(result)
        self.assertTrue(file_exist(dest_path))
        # Both files should exist
        self.assertTrue(file_exist(src_path))

        os.unlink(local_file)

    def test_copy_file_preserves_acl(self):
        """Test that copy preserves ACL."""
        if not self.acl_supported:
            self.skipTest('ACL operations not supported by storage provider')

        local_file = self.create_test_file()
        src_path = generate_test_path('txt')
        dest_path = generate_test_path('txt')
        self.track_s3_file(src_path)
        self.track_s3_file(dest_path)

        upload_file(local_file, src_path, 'text/plain', 'public-read')

        copy_file(src_path, dest_path)

        self.assertEqual(get_file_acl(dest_path), 'public-read')

        os.unlink(local_file)

    # --- List Tests ---

    def test_list_files(self):
        """Test listing files by prefix."""
        local_file = self.create_test_file()
        # Use a unique prefix for this test
        test_prefix = f'tests/list-test-{uuid.uuid4()}'
        s3_path1 = f'{test_prefix}/file1.txt'
        s3_path2 = f'{test_prefix}/file2.txt'
        self.track_s3_file(s3_path1)
        self.track_s3_file(s3_path2)

        upload_file(local_file, s3_path1, 'text/plain', 'private')
        upload_file(local_file, s3_path2, 'text/plain', 'private')

        entries = list_files(test_prefix, limit=10)

        self.assertEqual(len(entries), 2)
        keys = [e['key'] for e in entries]
        self.assertIn(s3_path1, keys)
        self.assertIn(s3_path2, keys)

        os.unlink(local_file)

    def test_list_files_with_limit(self):
        """Test list respects limit parameter."""
        local_file = self.create_test_file()
        test_prefix = f'tests/limit-test-{uuid.uuid4()}'
        paths = [f'{test_prefix}/file{i}.txt' for i in range(5)]
        for path in paths:
            self.track_s3_file(path)
            upload_file(local_file, path, 'text/plain', 'private')

        entries = list_files(test_prefix, limit=2)

        self.assertEqual(len(entries), 2)

        os.unlink(local_file)

    def test_list_files_empty_result(self):
        """Test list returns empty for non-matching prefix."""
        entries = list_files(f'tests/nonexistent-prefix-{uuid.uuid4()}', limit=10)

        self.assertEqual(entries, [])

    # --- Metadata Tests ---

    def test_get_meta(self):
        """Test getting file metadata."""
        local_file = self.create_test_file('Metadata test content')
        s3_path = generate_test_path('txt')
        self.track_s3_file(s3_path)

        upload_file(local_file, s3_path, 'text/plain', 'private')

        meta = get_meta(s3_path)

        self.assertIsNotNone(meta)
        self.assertIn('ContentLength', meta)
        self.assertIn('ContentType', meta)
        self.assertEqual(meta['ContentType'], 'text/plain')

        os.unlink(local_file)

    def test_get_meta_nonexistent(self):
        """Test get_meta returns None for non-existing file."""
        s3_path = f'tests/nonexistent-{uuid.uuid4()}.txt'

        meta = get_meta(s3_path)

        self.assertIsNone(meta)

    # --- URL Tests ---

    def test_get_obj_url(self):
        """Test URL generation."""
        s3_path = 'tests/example.txt'

        url = get_obj_url(s3_path)

        self.assertIsInstance(url, str)
        self.assertIn(s3_path, url)


if __name__ == '__main__':
    unittest.main()
