import unittest
import subprocess
import sys

class TestTheSearcherIntegration(unittest.TestCase):

    def test_script_runs_dry_run(self):
        """Test that the script runs with --dry-run and exits cleanly."""
        process = subprocess.run(
            [sys.executable, "-m", "src.theSearcher", "--input", "test_integration", "--dry-run"],
            capture_output=True,
            text=True,
            check=False  # Check manually
        )
        self.assertEqual(process.returncode, 0, f"Process failed with error: {process.stderr}")
        self.assertIn("Dry run: Would search for images related to 'test_integration'.", process.stdout)
        self.assertIn("Result: Dry run: Searched for 'test_integration'", process.stdout)

    def test_script_runs_live_run(self):
        """Test that the script runs a live run and exits cleanly."""
        process = subprocess.run(
            [sys.executable, "-m", "src.theSearcher", "--input", "test_integration_live"],
            capture_output=True,
            text=True,
            check=False  # Check manually
        )
        self.assertEqual(process.returncode, 0, f"Process failed with error: {process.stderr}")
        self.assertIn("Live run: Searching for images related to 'test_integration_live'...", process.stdout)
        self.assertIn("Result: https://example.com/image_for_test_integration_live.jpg", process.stdout)

if __name__ == '__main__':
    unittest.main()
