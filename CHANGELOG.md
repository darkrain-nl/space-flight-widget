# Changelog

All notable changes to the Space Flight Widget will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2026-06-05

### Added
- **Clickable Version Link**: Wrapped the version metadata string in a hyperlink pointing to the widget's official preview site (`https://darkrain-nl.github.io/space-flight-widget/`) so users can easily find and configure it. Added hover transition styles to match the theme.

### Fixed
- **Multi-Instance and Re-injection Rendering**: Scoped all DOM query selectors within the parent widget container (`widgetEl`) of the executing script to prevent ID collisions when multiple widgets are embedded on the same page or when the widget is dynamically re-injected in the preview page.
- **Local Fetching State**: Moved the `isFetching` state variable from the global `window` object to a local script closure scope to prevent one widget's pending request from blocking another instance's fetches.
- **Metadata Output Formatting**: Improved metadata text concatenation to prevent trailing bullet bugs when status parts are empty.

## [1.0.1] - 2026-06-05

### Fixed
- **Refresh Button Visibility**: Ensure the manual refresh button remains visible and functional during fetch errors and fallback states (when no launch is scheduled or displayed).

## [1.0.0] - 2026-06-05

### Added
- **Multi-Language Support**: Fully translated user interface and API status badges in English (`en`), French (`fr`), Italian (`it`), German (`de`), Spanish (`es`), and Dutch (`nl`).
- **Inline Styling**: Pure inline styles to ensure the widget bypasses strict forum BBCode sanitizers that strip `<style>` tags.
- **Smart Proximity-Based Caching**: Integrates local caching via `localStorage`. Implements dynamic request TTL based on launch proximity (from 2 mins near launch to 30 mins when days away) to conserve API usage.
- **API Throttle Management**: Monitors `/api-throttle` endpoint, dynamically skipping network fetches when near the rate limit, and parsing the HTTP 429 throttle duration to schedule the next refresh.
- **Hold & Failure Alerts**: Dynamic status card warning box displaying critical launch updates from the API like hold reasons, failure reasons, and weather concerns.
- **Fallback State**: Clean fallback UI in case no launches match configuration (allowed rockets list, time window).
- **Quality & Constraints Test Suite**: Automated tests under `tests/` verifying ES5 compatibility, inline styles, XSS DOM sinks (innerHTML), localization key completeness, size budgets, and BBCode/smiley bug regressions.
- **CI Workflow**: Configured GitHub Actions CI running unit tests, minification builds, and Ruff checks/formatting on all pushes and pull requests.
- **Shared Global State**: Switched to global window state properties (`window.spaceWidgetLastFetchTime`, `window.spaceWidgetCurrentThrottle`) to resolve widget initialization race conditions.
