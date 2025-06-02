# Features

## Search Provider Pattern (Integrated)

This feature refactors the image search functionality to use a provider pattern. This allows for more flexible and extensible search capabilities.

Key components:
- **Provider Abstract Base Class (`src.providers.Provider`)**: Defines the interface for all search providers.
- **`GoogleSearchProvider` (`src.theSearcher.GoogleSearchProvider`)**: The initial concrete implementation, using the existing Google image search logic.
- **`SerpAPIProvider` (`src.providers.serp_api_provider.SerpAPIProvider`)**: A placeholder provider for future integration with SerpAPI. It currently simulates search behavior.

This abstraction makes it easier to:
- Add new search providers (e.g., Bing, DuckDuckGo) in the future.
- Switch between providers based on configuration or other criteria.
- Test search functionality in isolation by mocking provider implementations.
