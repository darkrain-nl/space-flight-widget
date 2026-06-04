# 🚀 Space Flight Widget

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![API](https://img.shields.io/badge/API-The%20Space%20Devs-10b981)](https://thespacedevs.com/)
[![Built with Vanilla JS](https://img.shields.io/badge/JavaScript-Vanilla-f7df1e?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

Embed upcoming heavy-lift rocket launches directly into your forum or website. A lightweight, responsive countdown widget powered by [The Space Devs API](https://thespacedevs.com/).

### Previews
<p align="center">
  <a href="https://darkrain-nl.github.io/space-flight-widget/">
    <img src="assets/preview.gif?v=3" alt="Active Launch" width="700" />
  </a>
  <a href="https://darkrain-nl.github.io/space-flight-widget/">
    <img src="assets/preview.png" alt="No Launch Fallback" width="350" />
  </a>
</p>

*Live Preview: [https://darkrain-nl.github.io/space-flight-widget/](https://darkrain-nl.github.io/space-flight-widget/)*


## ✨ Features
- **Multi-Language Support**: Fully translated interface and launch statuses in English (`en`), French (`fr`), Italian (`it`), German (`de`), Spanish (`es`), and Dutch (`nl`) (dynamic API-provided metadata like hold reasons and pad locations remains in English). English is the default.
- **BBCode Compatible**: Built entirely with inline styles and ES5 Javascript to bypass strict forum sanitizers and `[html]` tags.
- **Detailed Launch Metadata**: Displays launch status badges (e.g. *Go for Launch*, *TBD*, *Successful*, *On Hold*, *Postponed*, *Cancelled*), launch service provider, launch pad location, and weather launch probability (%).
- **Hold & Failure Alerts**: Dynamic warning alerts integrated directly into the widget to show critical launch updates like **Hold Reason**, **Failure Reason**, and **Weather Concerns** based on API updates.
- **Smart Logic**: Automatically displays a fallback message if there isn't a launch scheduled within the configured time window (default: 7 days, configurable via `data-days`).
- **Offline & Rate-Limit Resilient**: Caches launch data in `localStorage`. If the API hits rate limits (HTTP 429) or goes offline, the widget gracefully falls back to the cached data to keep the countdown ticking seamlessly.
- **Smart Auto-Refreshing**: Adapts refresh intervals based on launch proximity and rate limits, conserving API request budget while staying responsive.
- **Zero Dependencies**: Pure HTML and JavaScript. No external CSS stylesheets or libraries required.

## 🛠️ How to Embed
1. Visit the [live preview page](https://darkrain-nl.github.io/space-flight-widget/) to dynamically configure your language, rockets, and days ahead, then click **Copy Embed Code**.
2. Paste the generated code into your website or forum's HTML embed block (e.g., using `[html]...[/html]`).

*Alternatively, you can manually copy the raw code from [`dist/widget.min.html`](dist/widget.min.html) and edit the `data-lang`, `data-rockets`, and `data-days` attributes yourself.*

### ⚙️ Configuration Options

All configuration is done via `data-*` attributes on the widget's root `<div>`:

| Attribute | Description | Default | Example |
|---|---|---|---|
| `data-lang` | Display language (`en`, `fr`, `it`, `de`, `es`, `nl`) | `en` | `data-lang="nl"` |
| `data-rockets` | Comma-separated list of rocket names/families to track | All major rockets | `data-rockets="starship, falcon heavy"` |
| `data-days` | Number of days ahead to look for upcoming launches (positive integer) | `7` | `data-days="14"` |

**Example with all options:**
```html
<div id="space-countdown-widget" data-lang="en" data-rockets="starship, falcon heavy" data-days="14" ...>
```

## 🤝 How to Contribute
We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for important technical rules you need to follow when developing for this widget (like our strict BBCode parsing constraints).

### Quick Start
1. Fork the repo and clone it locally.
2. Make your edits in `src/widget.html`. **Do not edit `dist/widget.min.html` or `index.html` directly.**
3. Run the build script to compile and minify:
   ```bash
   python3 build.py
   ```
4. Open `index.html` in your browser to preview your changes.

## 📡 Automated Updates
This repository uses a GitHub Action to automatically monitor and update to the latest version of The Space Devs API. When the API updates, a Pull Request is automatically generated to update the widget. Please note that after an update is merged, you will still need to manually copy and paste the new code from `dist/widget.min.html` to update the widget on your forum or website.

## 📜 Attribution
Launch data is provided by [The Space Devs](https://thespacedevs.com/).

## ⚖️ License
MIT License. See `LICENSE` for more information.
