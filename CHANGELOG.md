# Changelog

All notable changes to the Space Flight Widget will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.7] - 2026-06-12

### Added
- **Extended Launch Visibility & Smart Selection**: Extended the visibility of recently completed launches from 15 minutes to 12 hours. Added default selected index fallback logic to show the first upcoming launch on load if the past launch is older than 30 minutes.
- **Manual Launch Selection Retention Window**: Retain the user's manual launch selection in `localStorage` on page reload for up to 30 minutes after liftoff, matching the critical window default selection logic.

## [1.0.6] - 2026-06-07

### Fixed
- **Infinite Fetch Loop API Spam**: Cooled down API fetches when a launch has passed by returning a 5-minute cache TTL.
- **T+ Count-up Display Filter**: Prevented recently launched or in-flight missions from being immediately filtered out, ensuring T+ count-up and simulation modes work properly.
- **Orphaned Safety Timeout**: Cleared active safety timeouts on script initialization to prevent background memory leaks.

## [1.0.5] - 2026-06-07

### Added
- **Fetch Timeout Protection**: Added a `fetchWithTimeout` wrapper with a 15-second timeout around all API `fetch()` calls to prevent indefinite network hangs. Added a 30-second safety timeout that force-resets the `isFetching` flag as a failsafe.
- **Simulator Cache Warning**: Added a warning label below the "Simulate Launch Liftoff (T-10s)" checkbox on the preview page explaining that toggling clears the local browser cache.

### Changed
- **Configuration Panel Layout**: Redesigned the preview page configuration controls into a clean 2×2 grid layout with labels above inputs, structured checkbox section with properly aligned warning text, and a wider `.instructions` container with polished shadow and border-radius.

### Fixed
- **Fetch Hanging Bug**: Fixed a critical bug where the widget could get permanently stuck in "Refreshing..." state if an API fetch never resolved (e.g., network timeout). The `isFetching` flag was never reset, blocking all future refresh attempts indefinitely.

## [1.0.4] - 2026-06-07

### Added
- **Local Time & Date Display**: Convert and display the launch's UTC date and time into the viewer's local browser timezone under the launch pad location.
- **Liftoff Celebration (T-0 Animation)**: Added a smooth, pulsing green glow effect on the `T+` sign container when a launch occurs, creating a dynamic visual celebration of liftoff.
- **Light Theme Adaptation**: Added CSS overrides for the local time element under the light theme in both the index preview and embed environments.

### Fixed
- **Rate Limit Loading Hang**: Fixed a bug where the widget would hang indefinitely on the `LOADING...` state with no manual refresh button visible if the API rate limit was reached and no cached data was present in local storage.

## [1.0.3] - 2026-06-07

### Added
- **Multi-Launch Navigation**: Added Back (`<`) and Forward (`>`) navigation button controls in a slick inline pill next to the countdown title, allowing users to cycle through up to 5 upcoming launches matching their filters.
- **Selection Persistence**: Implemented browser `localStorage` caching for the selected launch ID. The widget retains the user's manual selection upon page reload until the launch takes place, at which point it automatically falls back to the default upcoming launch.
- **CSS Light Theme Support**: Added adaptive light theme CSS style overrides for the navigation control container and buttons to match index and embed environments.

### Changed
- **Default Rocket Tracking**: Changed the default rocket filter configuration to not select any specific rockets on load. This allows the widget to track all upcoming launches by default if no configuration is provided. Removed default checks on preview page checkboxes.

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
