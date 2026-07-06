# Changelog

All notable changes to the Space Flight Widget will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.16] - 2026-07-06

### Fixed
- **Stable Control Pill**: The navigation/refresh control pill no longer shifts position between launches. It previously flipped between an inline and a wrapped position depending on whether the per-launch avatar thumbnail was shown (which changes the title column's width); the title now always fills the first line so the pill consistently wraps to its own line, right-aligned to the stable column edge, independent of the avatar, title text, and timer.

## [1.0.15] - 2026-07-05

### Fixed
- **Decade Label Translation**: Launches with "Decade" precision now render a translated label via the new `decadeOf` i18n key in all six languages, instead of hardcoded English "Decade of <year>".

### Changed
- **CI Without Live API Dependency**: The test suite validates the widget's API field expectations against a checked-in fixture; the live API is only checked by the daily version-update workflow, where a failure correctly blocks an unverified automated bump.
- **Safer Minification**: The build strips comments with a string/regex-aware scanner (literals containing comment markers can no longer be corrupted), re-validates the minified output, and rejects line endings that automatic semicolon insertion would reinterpret. The quality tests reuse the same scanner.
- **Hardened API Version Updater**: The daily version bump replaces only the anchored API URL (it can never touch other version-like strings), validates the scraped version, verifies the new endpoint is reachable, and fails loudly if the replacement did not land exactly.
- **Deploy-Time Build**: GitHub Pages regenerates `dist/widget.min.html` and the `index.html` widget block from source at deploy time, so the live site can never serve a stale committed artifact.

## [1.0.14] - 2026-07-05

### Added
- **Multiple Widgets Per Page**: All timer and refresh state is now per-instance, with a registry that only cleans up a replaced instance (or one removed from the document). Two or more widgets on one page count down and refresh independently instead of the newest one freezing the others.
- **Hidden-Tab Quota Protection**: Scheduled data fetches are skipped while the tab is hidden and resume (immediately, if overdue) when it becomes visible again, preserving the shared 15-requests/hour API quota.
- **Language List Consistency Test**: The supported-language list must now be identical in the widget's i18n object, `embed.html` and the preview page's selector, enforced by the test suite.

### Fixed
- **Broken Avatar Images**: Removed the `encodeURI` call that double-encoded already-encoded API image URLs, added an `onerror` fallback that hides the avatar instead of showing a broken image icon, and widened the pages' CSP `img-src` so thumbnails from any HTTPS host render.
- **Status Handling Keyed by Stable IDs**: Launch status translation, badge color, hold detection and refresh cadence are now driven by the API's numeric `status.id` instead of English status names. This fixes hold detection that could never match real API data, and adds missing translations for "Launch Failure", "Partial Failure" and "Payload Deployed" in all six languages.
- **Stale Error States**: The rate-limit and error displays now hide the local-time line and stop the countdown timer, matching the no-launch state (shared `showMessageState` helper).
- **`data-days` Upper Bound**: The widget itself now enforces the documented 1-365 day window instead of relying on the preview/embed wrappers.
- **Safer Rate-Limit Retry**: The 429 retry delay now falls back to the structured throttle data and a 5-minute floor instead of hammering a throttled API every 30 seconds when the error prose changes.

### Changed
- **Leaner API Usage**: The launches query is bounded to the configured display window (`net__lte`), shrinking payloads by ~90% for default configurations, and the throttle status moved to its own localStorage key so cache updates no longer re-serialize the full launch payload multiple times per cycle.
- **Shared Page Assets**: The widget load/configure/mount pipeline and the light-theme stylesheet now live once in `assets/` and are shared by the preview page and `embed.html`, so the embed code users copy is produced by exactly the code path that renders their iframe.
- **Test Suite Reuses Build Logic**: `tests/test_quality.py` imports `build.py`'s script extraction and validation instead of maintaining drifting copies; the dist regression test now enforces the full build ruleset.

## [1.0.12] - 2026-07-05

### Fixed
- **Unsupported Language Crash**: The warning-box labels in `showLaunch` now use the shared i18n fallback, so an unsupported `data-lang` value no longer throws a `TypeError` and leaves the widget permanently stuck on "Loading...".
- **Coarse Date Precision Mapping**: Aligned `formatCoarseDate` with the Launch Library `net_precision` enumeration (8–11 = Quarters 1–4, 12/13 = Year Halves, 15 = Fiscal Year, 16 = Decade). Launches with "Quarter 1" precision previously rendered as "Decade of <year>".
- **Refresh Timer Leaks**: All refresh scheduling now goes through a `scheduleFetch()` helper that clears the previously scheduled fetch first, preventing duplicate polling loops (and doubled API quota usage) after slow-network error and rate-limit paths.
- **Preview Page Cache Wipe**: The preview page no longer clears the widget's `localStorage` cache on every page load; the cache is cleared only when the simulation toggle actually changes or leftover simulated data is detected.
- **Preview Rebuild Storms & Races**: The preview's `updateWidget` is debounced (150ms) with a stale-response guard, and the widget template fetch now checks `res.ok` and reports failures via toast instead of injecting an error page into the embed code output.
- **Stale Footer Version**: The static footer fallback text showed `v1.0.2`; it now matches the widget version (previously only corrected at runtime).

### Changed
- **Build & CI Guardrails**: `build.py` now anchors the `index.html` splice region to the widget block and fails loudly on missing markers; CI verifies that the committed `dist/` and `index.html` artifacts are in sync with `src/widget.html`.

## [1.0.11] - 2026-06-28

### Fixed
- **Control Pill Position Shift**: Prevent layout/control pill shift when cycling between precise launches (with a countdown timer) and coarse launches (with a date string) by assigning a consistent width (272px) to the right-hand container elements.

## [1.0.10] - 2026-06-17

### Added
- **Hold Reason Translation Support**: Added translation logic for the warning box to render `launch.holdreason` using the i18n `holdReason` keys (previously defined but unused).

### Fixed
- **In-flight Status Translation**: Added translation and upcoming lists mapping support for the `"Launch in Flight"` status (equivalent to `"In Flight"`).

## [1.0.9] - 2026-06-17

### Added
- **Countdown Hold Behavior**: Automatically freeze the countdown timer when a launch status is "On Hold" (preventing incorrect count-up `T+` display).
- **On Hold Duration Restriction**: Keep "On Hold" launches in the active list for up to 60 minutes after their scheduled launch time (unless actual flight starts or the launch is scrubbed/postponed).
- **Fast Dynamic Refresh Rate**: Enforce rapid cache updates (every 2 minutes under healthy API quotas, 5 minutes under conserved/depleted quotas) when a launch is on hold to quickly reflect status changes.
- **On Hold Theme Feedback**: Custom orange/yellow visual branding applied to the `T-` sign box and symbol during holds.

## [1.0.8] - 2026-06-15

### Added
- **Unified Controls Pill Layout**: Grouped navigation buttons (Previous, Next, and a new Home/Reset button) along with the Refresh button into a single right-aligned, cohesive controls group to stabilize layout and prevent shifting when the title changes.
- **Home Navigation Action**: Added a target/focus Home button between Previous and Next chevrons to allow quick resetting of the selection to the nearest upcoming/future launch.

### Changed
- **WCAG Accessibility & Focus Indicator Upgrades**: 
  - Increased button target sizes from 16px to 24px for improved touch target accessibility (WCAG 2.5.8).
  - Implemented focus rings on all interactive buttons and links utilizing `onfocus` and `onblur` event mapping (WCAG 2.4.7).
  - Enhanced contrast of meta-text from #64748b to #94a3b8 in dark theme to satisfy contrast requirements (WCAG 1.4.3).
  - Applied `aria-label` tags to all button components (WCAG 4.1.2).
  - Avoided hover underline clipping on the main launch name link by transitioning `border-bottom-color` instead of `text-decoration`.

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
