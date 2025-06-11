import os
import requests
import shutil
import logging

logger = logging.getLogger(__name__)

# Mapping of common image content types to file extensions
CONTENT_TYPE_TO_EXTENSION = {
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'image/webp': '.webp',
    # Add more mappings as needed
}
DEFAULT_EXTENSION = '.jpg'

def check_for_existing_image(folder_path: str) -> bool:
    """
    Checks if a common album art image file exists in the given folder.

    It looks for files with common album art names (like 'cover', 'folder')
    and common image extensions (like '.jpg', '.png'). The checks are
    case-insensitive.

    Args:
        folder_path: The absolute path to the folder to check.

    Returns:
        True if a common album art image is found, False otherwise.
    """
    common_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    common_filenames = ['cover', 'folder', 'albumart', 'front']

    if not os.path.isdir(folder_path):
        # Or raise an error, or log a warning, depending on desired handling
        return False

    for filename_with_ext in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename_with_ext)
        if os.path.isfile(file_path):
            name_part, ext_part = os.path.splitext(filename_with_ext)

            name_part_lower = name_part.lower()
            ext_part_lower = ext_part.lower()

            if name_part_lower in common_filenames and ext_part_lower in common_extensions:
                return True

    return False

def _determine_image_extension(image_url: str, content_type: str | None = None) -> str:
    """
    Determines the image file extension from the URL or Content-Type header.
    """
    # Attempt to get from URL first
    try:
        url_path = requests.utils.urlparse(image_url).path
        url_ext = os.path.splitext(url_path)[1].lower()
        if url_ext in CONTENT_TYPE_TO_EXTENSION.values():
            return url_ext
    except Exception:
        pass # Ignore errors in URL parsing for this step

    # If Content-Type is provided and valid, use it
    if content_type:
        content_type_lower = content_type.split(';')[0].strip().lower()
        if content_type_lower in CONTENT_TYPE_TO_EXTENSION:
            return CONTENT_TYPE_TO_EXTENSION[content_type_lower]

    # Default if unable to determine
    logger.warning(f"Could not determine extension for {image_url} from URL or Content-Type. Defaulting to {DEFAULT_EXTENSION}.")
    return DEFAULT_EXTENSION

def download_image(image_url: str, save_path_without_extension: str) -> str | None:
    """
    Downloads an image from a URL and saves it to a specified path.

    The function attempts to determine the correct file extension from the
    image URL or the Content-Type header. If not determinable, defaults to '.jpg'.

    Args:
        image_url: The URL of the image to download.
        save_path_without_extension: The full path to save the image to,
                                     excluding the file extension.

    Returns:
        The full path to the saved image (including extension) if successful,
        None otherwise. Prints an error message to stderr in case of failure.
    """
    try:
        # First, try a HEAD request to get Content-Type without downloading the body
        head_response = requests.head(image_url, timeout=10, allow_redirects=True)
        head_response.raise_for_status()
        content_type = head_response.headers.get('Content-Type')
        logger.debug(f"HEAD request for {image_url} successful. Content-Type: {content_type}")
        extension = _determine_image_extension(image_url, content_type)
    except requests.exceptions.RequestException as head_err:
        logger.warning(f"HEAD request failed for {image_url}: {head_err}. Attempting to determine extension from URL path or defaulting.", exc_info=True)
        # Fallback to guessing extension from URL directly if HEAD fails
        extension = _determine_image_extension(image_url) # content_type will be None

    full_save_path = save_path_without_extension + extension

    try:
        # Now make the GET request to download the actual image
        response = requests.get(image_url, stream=True, timeout=15)
        response.raise_for_status()  # Check for HTTP errors

        # Ensure the directory exists
        save_directory = os.path.dirname(full_save_path)
        if save_directory: # Only create if dirname is not empty (i.e. not saving in current dir)
             os.makedirs(save_directory, exist_ok=True)

        with open(full_save_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        logger.info(f"Image successfully downloaded and saved to {full_save_path}")
        return full_save_path

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while downloading {image_url}: {http_err}", exc_info=True)
        return None
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Request timed out while downloading {image_url}: {timeout_err}", exc_info=True)
        return None
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred downloading {image_url}: {req_err}", exc_info=True)
        return None
    except IOError as io_err:
        logger.error(f"File error occurred while saving image to {full_save_path}: {io_err}", exc_info=True)
        return None
