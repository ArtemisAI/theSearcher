import unittest
import os
import shutil
import tempfile
from src.folder_utils import iterate_album_folders

class TestIterateAlbumFolders(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_root_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Remove the temporary directory after tests."""
        shutil.rmtree(self.test_root_dir)

    def test_empty_directory(self):
        """Test with an empty root directory."""
        result = list(iterate_album_folders(self.test_root_dir))
        self.assertEqual(result, [])

    def test_directory_with_files_only(self):
        """Test with a directory containing only files."""
        open(os.path.join(self.test_root_dir, "file1.txt"), 'a').close()
        open(os.path.join(self.test_root_dir, "file2.mp3"), 'a').close()

        result = list(iterate_album_folders(self.test_root_dir))
        self.assertEqual(result, [])

    def test_directory_with_subdirectories(self):
        """Test with a directory containing subdirectories and files."""
        # Create subdirectories
        album1_path = os.path.join(self.test_root_dir, "Album1")
        os.makedirs(album1_path)

        band2_path = os.path.join(self.test_root_dir, "Band2")
        os.makedirs(band2_path)

        # This is a nested subdirectory, should not be yielded directly by iterate_album_folders
        # if it's only looking for immediate subdirectories.
        album_x_path = os.path.join(band2_path, "AlbumX")
        os.makedirs(album_x_path)

        # Create a file in a subdirectory, should not affect the result
        open(os.path.join(album1_path, "song.mp3"), 'a').close()
        # Create a file in the root, should be ignored
        open(os.path.join(self.test_root_dir, "root_song.flac"), 'a').close()

        expected_paths = sorted([
            album1_path,
            band2_path
        ])

        result = sorted(list(iterate_album_folders(self.test_root_dir)))
        self.assertEqual(result, expected_paths)

    def test_directory_with_mixed_content(self):
        """Test with a directory containing a mix of files and subdirectories."""
        # Create files
        open(os.path.join(self.test_root_dir, "notes.txt"), 'a').close()
        open(os.path.join(self.test_root_dir, "image.jpg"), 'a').close()

        # Create subdirectories
        sub_dir1_path = os.path.join(self.test_root_dir, "My Album A")
        os.makedirs(sub_dir1_path)

        sub_dir2_path = os.path.join(self.test_root_dir, "Another Artist - Album B")
        os.makedirs(sub_dir2_path)

        # Add a file into a subdirectory
        open(os.path.join(sub_dir1_path, "track1.ogg"), 'a').close()

        expected_paths = sorted([
            sub_dir1_path,
            sub_dir2_path
        ])

        result = sorted(list(iterate_album_folders(self.test_root_dir)))
        self.assertEqual(result, expected_paths)

    def test_non_existent_directory(self):
        """Test with a non-existent root path."""
        non_existent_path = os.path.join(self.test_root_dir, "does_not_exist")
        # Expecting FileNotFoundError or similar, depending on os.listdir behavior
        with self.assertRaises(FileNotFoundError):
            list(iterate_album_folders(non_existent_path))

    def test_path_is_a_file(self):
        """Test when the root_path provided is actually a file."""
        file_path = os.path.join(self.test_root_dir, "a_file.txt")
        open(file_path, 'a').close()
        # Expecting NotADirectoryError or similar
        with self.assertRaises(NotADirectoryError):
            list(iterate_album_folders(file_path))

if __name__ == '__main__':
    unittest.main()
