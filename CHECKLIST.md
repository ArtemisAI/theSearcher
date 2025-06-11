# Project Checklist

## General Development
- [ ] Code follows established coding standards.
- [ ] All new functions and classes are documented with docstrings.
- [ ] Configuration is managed via environment variables or a config file (not hardcoded).
- [ ] Secrets (like API keys) are not committed to the repository.
- [ ] Dependencies are listed in a `requirements.txt` or similar.
- [ ] Code is well-commented, especially complex logic.
- [ ] Error handling is implemented for expected failure points.
- [ ] Logging is implemented for important events and errors.

## Testing
- [ ] Unit tests cover core functionality.
- [ ] Unit tests cover edge cases and potential failure modes.
- [ ] Integration tests verify interactions between components.
- [ ] All tests pass before merging code.
- [ ] Test coverage is monitored and maintained/improved.

## Documentation
- [ ] `README.md` is up-to-date with project description, setup, and usage instructions.
- [ ] `ROADMAP.md` reflects the current project plan and vision.
- [ ] `TODO.md` is regularly updated with current tasks.
- [ ] Architectural decisions are documented (e.g., in `docs/ARCHITECTURE.md`).
- [ ] User documentation is clear and helpful (if applicable).

## "theSearcher" Project Specific
- [ ] Google API key is correctly configured in the environment.
- [ ] Image search queries are formulated effectively.
- [ ] Image download and saving logic handles potential errors (e.g., network issues, disk full).
- [ ] Folder iteration logic correctly finds all target directories.
- [ ] Existing image check works as expected.
- [ ] Logging provides clear insight into the image search and download process for each folder.

## Before Release / Deployment
- [ ] All items in `TODO.md` for the current milestone are completed.
- [ ] Final review of code changes.
- [ ] All tests are passing in the CI environment.
- [ ] Documentation has been updated.
- [ ] Version number is updated (if applicable).
