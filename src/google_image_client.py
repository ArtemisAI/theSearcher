import requests
import json
import os
import logging

logger = logging.getLogger(__name__)

def search_album_art_on_google(api_key: str, custom_search_engine_id: str, query: str) -> list[dict] | None:
    """
    Searches for album art on Google Custom Search JSON API.

    Args:
        api_key: Your Google API Key.
        custom_search_engine_id: Your Google Custom Search Engine ID (CX).
        query: The search query, typically the album name.

    Returns:
        A list of dictionaries, where each dictionary represents an image result
        and contains at least a 'link' key with the image URL.
        Returns None if an error occurs during the API request or if no items are found.
        Prints an error message to stderr in case of failure.

    Raises:
        requests.exceptions.RequestException: For network issues or timeouts.
                                              (This is handled internally and an error message is printed,
                                               None is returned instead of raising)
    """
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': custom_search_engine_id,
        'q': query,
        'searchType': 'image',
        'num': 5,  # Number of search results
        'imgSize': 'LARGE', # Aim for large images
        'alt': 'json'
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

        data = response.json()

        if 'items' not in data or not data['items']:
            logger.info(f"No image results found for query: {query}")
            return [] # Return empty list if no items found

        # Extract relevant information, primarily the image links
        image_results = []
        for item in data['items']:
            image_info = {'link': item.get('link')}
            if 'title' in item:
                image_info['title'] = item.get('title')
            if 'snippet' in item:
                image_info['snippet'] = item.get('snippet')
            # Add other useful fields if necessary, e.g., item.get('image', {}).get('height')
            image_results.append(image_info)

        return image_results

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while searching for '{query}': {http_err} - Status: {response.status_code if 'response' in locals() else 'N/A'}", exc_info=True)
        return None
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Request timed out while searching for '{query}': {timeout_err}", exc_info=True)
        return None
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred during the request for '{query}': {req_err}", exc_info=True)
        return None
    except json.JSONDecodeError as json_err:
        logger.error(f"Error decoding JSON response for '{query}': {json_err}", exc_info=True)
        return None

if __name__ == '__main__':
    # This is an example of how to use the function.
    # You'll need to set your API_KEY and CX_ID as environment variables
    # or replace os.environ.get() with your actual key and ID.

    # IMPORTANT: Do not commit your API key or CX ID directly into the code.
    # Use environment variables or a config file for sensitive data.

    # Example: Fetch API key and CX ID from environment variables
    # test_api_key = os.environ.get("GOOGLE_API_KEY")
    # test_cx_id = os.environ.get("GOOGLE_CSE_ID")
    # test_query = "Pink Floyd The Wall"

    # if not test_api_key or not test_cx_id:
    #     logger.error("Please set GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables for testing.")
    # else:
    #     # Example: to use this test, you'd need to setup logging first
    #     # from ..logging_utils import setup_logging # Assuming logging_utils is one level up
    #     # setup_logging(logging.DEBUG)
    #     logger.info(f"Searching for: {test_query}")
    #     results = search_album_art_on_google(test_api_key, test_cx_id, test_query)
    #     if results is not None:
    #         if results:
    #             logger.info(f"Found {len(results)} images:")
    #             for i, img in enumerate(results):
    #                 logger.info(f"  {i+1}. Link: {img.get('link')}")
    #                 if 'title' in img:
    #                     logger.info(f"     Title: {img.get('title')}")
    #         else:
    #             logger.info("No results found.")
    #     else:
    #         logger.error("Search failed.")
    pass # Keep the __main__ block, but pass for now
