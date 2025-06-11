import unittest
from unittest.mock import patch, MagicMock
import requests # For requests.exceptions
import json # For json.loads and json.JSONDecodeError if not using requests.exceptions.JSONDecodeError
import logging
from src.google_image_client import search_album_art_on_google

# It's better to get the logger for the specific module we are testing
client_logger = logging.getLogger('src.google_image_client')

class TestSearchAlbumArtOnGoogle(unittest.TestCase):

    def setUp(self):
        self.original_logging_level = client_logger.getEffectiveLevel()
        client_logger.setLevel(logging.CRITICAL + 1) # Disable logging from this module

    def tearDown(self):
        client_logger.setLevel(self.original_logging_level) # Restore logging

    @patch('src.google_image_client.requests.get')
    def test_search_successful_returns_items(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        sample_response_data = {
            "items": [
                {"link": "http://example.com/image1.jpg", "title": "Image 1", "snippet": "Desc 1"},
                {"link": "http://example.com/image2.png", "title": "Image 2", "snippet": "Desc 2"}
            ]
        }
        mock_response.json.return_value = sample_response_data
        mock_requests_get.return_value = mock_response

        api_key = "fake_api_key"
        cx_id = "fake_cx_id"
        query = "Test Album"

        expected_items = [
            {'link': 'http://example.com/image1.jpg', 'title': 'Image 1', 'snippet': 'Desc 1'},
            {'link': 'http://example.com/image2.png', 'title': 'Image 2', 'snippet': 'Desc 2'}
        ]

        result = search_album_art_on_google(api_key, cx_id, query)

        mock_requests_get.assert_called_once() # Check it was called
        self.assertEqual(result, expected_items)

    @patch('src.google_image_client.requests.get')
    def test_search_successful_no_items_found(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Test two cases: items key missing, or items list empty
        sample_response_data_no_items_key = {"other_data": "foo"}
        sample_response_data_empty_items = {"items": []}

        # Case 1: 'items' key is not present
        mock_response.json.return_value = sample_response_data_no_items_key
        mock_requests_get.return_value = mock_response
        result1 = search_album_art_on_google("k", "c", "q")
        self.assertEqual(result1, [])

        # Case 2: 'items' key is present but list is empty
        mock_response.json.return_value = sample_response_data_empty_items
        mock_requests_get.return_value = mock_response
        result2 = search_album_art_on_google("k", "c", "q")
        self.assertEqual(result2, [])

    @patch('src.google_image_client.requests.get')
    def test_search_http_error(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 403
        # Configure raise_for_status to simulate the error
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Forbidden")
        mock_requests_get.return_value = mock_response

        result = search_album_art_on_google("key", "cx", "query")
        self.assertIsNone(result) # Function should return None on HTTPError

    @patch('src.google_image_client.requests.get')
    def test_search_request_timeout(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        result = search_album_art_on_google("key", "cx", "query")
        self.assertIsNone(result) # Function should return None on Timeout

    @patch('src.google_image_client.requests.get')
    def test_search_json_decode_error(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "this is not valid json" # For logging, if any
        # requests.exceptions.JSONDecodeError was added in requests 2.27.0
        # Fallback to json.JSONDecodeError for broader compatibility if needed,
        # but requests itself should raise its own version if response.json() is called.
        try:
            from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError
        except ImportError:
            from json import JSONDecodeError as RequestsJSONDecodeError # Fallback for older requests

        mock_response.json.side_effect = RequestsJSONDecodeError("Error decoding JSON", "doc", 0)
        mock_requests_get.return_value = mock_response

        result = search_album_art_on_google("key", "cx", "query")
        self.assertIsNone(result) # Function should return None on JSONDecodeError

    @patch('src.google_image_client.requests.get')
    def test_search_parameters_in_url(self, mock_requests_get):
        # This test checks if the parameters are correctly passed to requests.get
        # The current implementation of search_album_art_on_google doesn't allow changing num or imgSize via args
        # So we will test the default values used in the function.

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []} # Empty items is fine
        mock_requests_get.return_value = mock_response

        api_key = "test_key"
        cx_id = "test_cx"
        query_text = "My Specific Query"

        search_album_art_on_google(api_key, cx_id, query_text)

        mock_requests_get.assert_called_once()
        call_args = mock_requests_get.call_args

        # The first argument to requests.get is the URL, the second is 'params' dict
        self.assertEqual(call_args[0][0], "https://www.googleapis.com/customsearch/v1")

        passed_params = call_args[1]['params']
        self.assertEqual(passed_params['key'], api_key)
        self.assertEqual(passed_params['cx'], cx_id)
        self.assertEqual(passed_params['q'], query_text)
        self.assertEqual(passed_params['searchType'], 'image')
        self.assertEqual(passed_params['num'], 5) # Default from function
        self.assertEqual(passed_params['imgSize'], 'LARGE') # Default from function
        self.assertEqual(passed_params['alt'], 'json')


if __name__ == '__main__':
    unittest.main()
