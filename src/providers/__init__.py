from abc import ABC, abstractmethod
# Removed: from .serp_api_provider import SerpAPIProvider
# Consumers will now import SerpAPIProvider directly from its module.

class Provider(ABC):
    """
    Abstract base class for search providers.
    """

    @abstractmethod
    def search(self, query: str, dry_run: bool = False) -> str:
        """
        Performs a search for the given query.

        Args:
            query: The search query.
            dry_run: If True, simulates the search without making actual calls.

        Returns:
            A string representing the search result (e.g., an image URL or a message).
        """
        pass
