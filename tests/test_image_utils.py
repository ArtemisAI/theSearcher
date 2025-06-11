import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import shutil
import tempfile
import io
import logging
from src.image_utils import check_for_existing_image, download_image, _determine_image_extension, DEFAULT_EXTENSION, CONTENT_TYPE_TO_EXTENSION

# Disable most logging for tests unless specifically testing logging
# logging.disable(logging.CRITICAL)

class TestCheckForExistingImage(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _create_file(self, filename):
        open(os.path.join(self.test_dir, filename), 'a').close()

    def test_image_exists_common_name_jpg(self):
        self._create_file("cover.jpg")
        self.assertTrue(check_for_existing_image(self.test_dir))

    def test_image_exists_common_name_png_case_insensitive(self):
        self._create_file("Folder.PNG")
        self.assertTrue(check_for_existing_image(self.test_dir))

    def test_image_exists_albumart_jpeg(self):
        self._create_file("albumart.jpeg")
        self.assertTrue(check_for_existing_image(self.test_dir))

    def test_image_exists_front_gif(self):
        self._create_file("front.gif")
        self.assertTrue(check_for_existing_image(self.test_dir))

    def test_no_image_exists_empty_dir(self):
        self.assertFalse(check_for_existing_image(self.test_dir))

    def test_no_image_exists_other_files(self):
        self._create_file("song.mp3")
        self._create_file("notes.txt")
        self.assertFalse(check_for_existing_image(self.test_dir))

    def test_image_exists_but_uncommon_name(self):
        self._create_file("myphoto.jpg")
        self.assertFalse(check_for_existing_image(self.test_dir))

    def test_common_name_but_wrong_extension(self):
        self._create_file("cover.txt")
        self.assertFalse(check_for_existing_image(self.test_dir))

    def test_non_existent_folder(self):
        self.assertFalse(check_for_existing_image(os.path.join(self.test_dir, "non_existent")))


class TestDetermineImageExtension(unittest.TestCase):

    def test_from_url_simple_png(self):
        self.assertEqual(_determine_image_extension("http://example.com/image.png"), ".png")

    def test_from_url_simple_jpg(self):
        self.assertEqual(_determine_image_extension("http://example.com/image.jpg"), ".jpg")

    def test_from_url_with_query_params_jpeg(self):
        self.assertEqual(_determine_image_extension("http://example.com/image.jpeg?a=1&b=2"), ".jpeg")

    def test_from_url_uppercase_ext(self):
        self.assertEqual(_determine_image_extension("http://example.com/image.JPG"), ".jpg")

    def test_from_url_no_extension(self):
        self.assertEqual(_determine_image_extension("http://example.com/image_without_extension"), DEFAULT_EXTENSION)

    def test_from_content_type_jpg(self):
        self.assertEqual(_determine_image_extension("http://example.com/dynamic", "image/jpeg"), ".jpg")

    def test_from_content_type_png_with_charset(self):
        self.assertEqual(_determine_image_extension("http://example.com/dynamic", "image/png; charset=UTF-8"), ".png")

    def test_from_content_type_gif(self):
        self.assertEqual(_determine_image_extension("http://example.com/dynamic", "image/gif"), ".gif")

    def test_from_content_type_webp(self):
        self.assertEqual(_determine_image_extension("http://example.com/dynamic", "image/webp"), ".webp")

    def test_url_ext_takes_precedence_over_content_type(self):
        # If URL has a known extension, it might be preferred or used as fallback.
        # Current implementation: URL ext is checked first. If valid, it's used.
        self.assertEqual(_determine_image_extension("http://example.com/image.png", "image/jpeg"), ".png")

    def test_unknown_content_type_uses_url_ext_if_available(self):
        # image/bmp is not in our default CONTENT_TYPE_TO_EXTENSION, but .bmp is a valid image ext
        # The function _determine_image_extension will try to use .bmp from URL if image/bmp is not in map
        # However, for this to pass, .bmp must be a value in CONTENT_TYPE_TO_EXTENSION for the first check.
        # Let's assume .bmp is not in the map to test fallback to default.
        # If .bmp *is* in the map, this test would be self.assertEqual(_determine_image_extension("http://example.com/image.bmp", "image/bmp-custom"), ".bmp")
        original_map_value = CONTENT_TYPE_TO_EXTENSION.get('image/bmp')
        if 'image/bmp' in CONTENT_TYPE_TO_EXTENSION: # Temporarily remove if exists
            del CONTENT_TYPE_TO_EXTENSION['image/bmp']

        # If .bmp is a recognized extension from URL, it should be used.
        # To make this test more robust, we need to ensure .bmp is not in CONTENT_TYPE_TO_EXTENSION values
        # or that the logic correctly prefers URL if content type is unmapped.
        # Current logic: tries URL, then content-type, then default.
        # So if URL has .bmp and .bmp is a known extension type, it will be returned.
        # For this test, let's assume .bmp is a "known" extension by virtue of being common.
        # The test is more about content-type being unmapped.
        self.assertEqual(_determine_image_extension("http://example.com/image.bmp", "image/bmp-custom"), ".bmp")

        if original_map_value: # Restore if it was there
             CONTENT_TYPE_TO_EXTENSION['image/bmp'] = original_map_value


    def test_unknown_content_type_and_no_url_ext_uses_default(self):
        self.assertEqual(_determine_image_extension("http://example.com/dynamic", "image/foo-bar"), DEFAULT_EXTENSION)

    def test_no_url_ext_and_no_content_type_uses_default(self):
        self.assertEqual(_determine_image_extension("http://example.com/dynamic_image_no_params"), DEFAULT_EXTENSION)

    def test_url_with_unrelated_dots(self):
        self.assertEqual(_determine_image_extension("http://example.com/some.folder/image.png"), ".png")
        self.assertEqual(_determine_image_extension("http://example.com/some.folder/image_no_ext", "image/jpeg"), ".jpg")


class TestDownloadImage(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_logging_level = logging.getLogger('src.image_utils').getEffectiveLevel()
        logging.getLogger('src.image_utils').setLevel(logging.CRITICAL + 1) # Disable logging from this module

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        logging.getLogger('src.image_utils').setLevel(self.original_logging_level) # Restore logging

    @patch('src.image_utils.shutil.copyfileobj')
    @patch('src.image_utils.requests.get')
    @patch('src.image_utils.requests.head')
    def test_download_successful_jpg_from_url_ext(self, mock_head, mock_get, mock_copyfileobj):
        # Mock HEAD response (not strictly needed if URL has extension, but good practice)
        mock_head_response = MagicMock()
        mock_head_response.status_code = 200
        mock_head_response.headers = {'Content-Type': 'image/jpeg'} # Irrelevant if URL has ext
        mock_head.return_value = mock_head_response

        # Mock GET response
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.raw = io.BytesIO(b"dummy jpg data")
        mock_get.return_value = mock_get_response

        save_name = "myalbum"
        image_url = "http://example.com/image.jpg"
        expected_path = os.path.join(self.test_dir, f"{save_name}.jpg")

        result_path = download_image(image_url, os.path.join(self.test_dir, save_name))

        self.assertEqual(result_path, expected_path)
        mock_head.assert_called_once_with(image_url, timeout=10, allow_redirects=True)
        mock_get.assert_called_once_with(image_url, stream=True, timeout=15)
        mock_copyfileobj.assert_called_once()
        # Check if file was "written" (mock_open can be used for more specific checks on write content)
        # For now, asserting copyfileobj was called is primary. If it were real, check os.path.exists(expected_path)

    @patch('src.image_utils.shutil.copyfileobj')
    @patch('src.image_utils.requests.get')
    @patch('src.image_utils.requests.head')
    def test_download_successful_png_from_content_type(self, mock_head, mock_get, mock_copyfileobj):
        mock_head_response = MagicMock()
        mock_head_response.status_code = 200
        mock_head_response.headers = {'Content-Type': 'image/png'}
        mock_head.return_value = mock_head_response

        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.raw = io.BytesIO(b"dummy png data")
        mock_get.return_value = mock_get_response

        save_name = "myalbum2"
        image_url = "http://example.com/dynamicimage" # No extension in URL
        expected_path = os.path.join(self.test_dir, f"{save_name}.png")

        result_path = download_image(image_url, os.path.join(self.test_dir, save_name))

        self.assertEqual(result_path, expected_path)
        mock_head.assert_called_once_with(image_url, timeout=10, allow_redirects=True)
        mock_get.assert_called_once_with(image_url, stream=True, timeout=15)
        mock_copyfileobj.assert_called_once()

    @patch('src.image_utils.requests.get')
    @patch('src.image_utils.requests.head')
    def test_download_http_error_on_get(self, mock_head, mock_get):
        mock_head_response = MagicMock()
        mock_head_response.status_code = 200
        mock_head_response.headers = {'Content-Type': 'image/jpeg'}
        mock_head.return_value = mock_head_response

        mock_get_response = MagicMock()
        mock_get_response.status_code = 404
        mock_get_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_get_response

        image_url = "http://example.com/notfound.jpg"
        result = download_image(image_url, os.path.join(self.test_dir, "test"))
        self.assertIsNone(result)
        mock_get.assert_called_once()

    @patch('src.image_utils.requests.get')
    @patch('src.image_utils.requests.head')
    def test_download_request_exception_on_get(self, mock_head, mock_get):
        mock_head_response = MagicMock()
        mock_head_response.status_code = 200
        mock_head_response.headers = {'Content-Type': 'image/jpeg'}
        mock_head.return_value = mock_head_response

        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        image_url = "http://example.com/timeout.jpg"
        result = download_image(image_url, os.path.join(self.test_dir, "test"))
        self.assertIsNone(result)
        mock_get.assert_called_once()

    @patch('src.image_utils.shutil.copyfileobj')
    @patch('src.image_utils.requests.get')
    @patch('src.image_utils.requests.head')
    @patch('src.image_utils.os.makedirs') # Mock os.makedirs
    def test_download_creates_directory(self, mock_makedirs, mock_head, mock_get, mock_copyfileobj):
        mock_head_response = MagicMock()
        mock_head_response.status_code = 200
        mock_head_response.headers = {'Content-Type': 'image/jpeg'}
        mock_head.return_value = mock_head_response

        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.raw = io.BytesIO(b"dummy data")
        mock_get.return_value = mock_get_response

        save_base_name = "cover"
        # Path for saving includes a new subdirectory
        new_subdir_path = os.path.join(self.test_dir, "new_subdir")
        save_path_without_ext = os.path.join(new_subdir_path, save_base_name)
        expected_full_path = f"{save_path_without_ext}.jpg"

        image_url = "http://example.com/image.jpg"

        # Actual os.makedirs will be called unless we mock it.
        # We want to assert it's called correctly.
        # The function itself uses os.makedirs(..., exist_ok=True)

        result_path = download_image(image_url, save_path_without_ext)

        self.assertEqual(result_path, expected_full_path)
        mock_makedirs.assert_called_once_with(new_subdir_path, exist_ok=True)
        mock_copyfileobj.assert_called_once()
        # In a real scenario, we'd also check if the file exists at expected_full_path
        # self.assertTrue(os.path.exists(expected_full_path)) # This would require actual file creation

if __name__ == '__main__':
    unittest.main()
