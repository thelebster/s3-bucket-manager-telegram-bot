import unittest
from s3_bucket_bot.s3bucket import upload_file, get_file_name


class TestUpload(unittest.TestCase):
    def test_upload(self):
        upload_status = upload_file(
            "./tests/image.jpeg", "temp/image.jpeg", "image/jpeg", "public"
        )
        self.assertEqual(upload_status, True)


if __name__ == "__main__":
    unittest.main()
