# Security Policy

This project is a static widget that acts as a client for the **public and official The Space Devs API**. It does not store, process, or handle any user-specific data. All launch information is fetched directly from the API in the user's browser.

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please report it via the "Private vulnerability reporting" feature in this repository. We appreciate your efforts to responsibly disclose your findings.

## API Abuse and Rate Limiting

To prevent accidental abuse of The Space Devs API, the widget caches the most recent payload in the visitor's browser (`localStorage`). In the event of an `HTTP 429 Too Many Requests` error, the widget reads the API's suggested timeout duration, suspends further network requests until the timeout expires, and renders the widget using the local cache to maintain a seamless user experience.
