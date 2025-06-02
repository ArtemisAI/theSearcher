import unittest
from src.theSearcher import search_images

class TestTheSearcher(unittest.TestCase):

    def test_search_images_dry_run(self):
        query = "test_query_dry_run"
        expected_result = f"Dry run: Searched for '{query}'"
        actual_result = search_images(query, dry_run=True)
        self.assertEqual(actual_result, expected_result)

    def test_search_images_live_run(self):
        query = "test_query_live"
        expected_result = f"https://example.com/image_for_{query.replace(' ', '_')}.jpg"
        actual_result = search_images(query, dry_run=False)
        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()
