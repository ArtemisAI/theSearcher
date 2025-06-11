import os

def iterate_album_folders(root_path: str):
    """
    Iterates through all immediate subdirectories within the given root_path.

    Args:
        root_path: The path to the root directory containing album folders.

    Yields:
        str: The full path to each subdirectory (album folder).
    """
    for entry in os.listdir(root_path):
        full_path = os.path.join(root_path, entry)
        if os.path.isdir(full_path):
            yield full_path
