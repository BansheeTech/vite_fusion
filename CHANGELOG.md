# Changelog

All notable changes to this project will be documented in this file.

## [0.0.9] - 2024-02-20

### Added
- Smart manifest caching system
  - Persistent cache in production
  - Auto-refresh every 30s in development
- Dynamic nonce generation support
- Singleton cache manager class
- Type hints for all public methods

### Changed
- **Performance:** 90% reduction in filesystem operations
- **Security:** Nonces now regenerate per request if enabled and needed
- **Compatibility:** Requires Python 3.8+
- **Dependencies:** Formal Flask 3.x support
- **Refactor:** Code is cleaner and easier to understand for any possible forks

### Fixed
- CSS import resolution in nested dependencies
- Manifest path detection in multi-worker environments
- Error handling for missing entries
- Development mode hot-reloading

### Removed
- Implicit filesystem watcher dependency

## [0.0.8] - 2024-01-15
- Added support for different dist paths, check readme dist_path flag

