# Changelog

All notable changes to the Space Flight Widget will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
