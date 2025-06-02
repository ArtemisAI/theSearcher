import unittest
from src.theSearcher import GoogleSearchProvider # Updated import

class TestTheSearcher(unittest.TestCase):

    def setUp(self):
        self.provider = GoogleSearchProvider() # Instantiate the provider

    def test_search_images_dry_run(self):
        query = "test_query_dry_run"
        # Expected result updated to match GoogleSearchProvider output
        expected_result = f"Dry run: Searched for '{query}' via Google"
        actual_result = self.provider.search(query, dry_run=True)
        self.assertEqual(actual_result, expected_result)
        # We might also want to check stdout, but that requires more complex test setup (e.g., redirecting sys.stdout)
        # For now, we'll rely on the return value matching.

    def test_search_images_live_run(self):
        query = "test_query_live"
        # Expected result updated to match GoogleSearchProvider output
        expected_result = f"https://example.com/image_for_{query.replace(' ', '_')}.jpg"
        actual_result = self.provider.search(query, dry_run=False)
        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()
