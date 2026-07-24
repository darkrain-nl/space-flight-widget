import json
import os
import unittest
import urllib.error
import urllib.request

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIXTURE_PATH = os.path.join(BASE_DIR, "tests", "fixtures", "launches_upcoming.json")

# By default the schema is validated against the checked-in fixture, so CI
# neither depends on nor spends quota of the live rate-limited API. The
# api-update workflow sets LIVE_API_TEST=1 to validate the real API before
# opening an automated version-bump PR.
LIVE_MODE = os.environ.get("LIVE_API_TEST") == "1"


class TestSpaceDevsAPI(unittest.TestCase):
    def validate_schema(self, data):
        self.assertIn("results", data)
        results = data["results"]
        self.assertIsInstance(results, list)

        # If there are results, validate the schema of the first item
        if len(results) > 0:
            launch = results[0]
            self.assertIn("name", launch)
            self.assertIn("net", launch)
            self.assertIn("net_precision", launch)
            self.assertIn("rocket", launch)
            self.assertIn("status", launch)

            # Validate net_precision id
            self.assertIn("id", launch["net_precision"])
            self.assertIsInstance(launch["net_precision"]["id"], int)

            # Validate status id (drives translation, badge color and hold logic)
            self.assertIn("id", launch["status"])
            self.assertIsInstance(launch["status"]["id"], int)

            # Validate rocket configuration and families
            rocket = launch["rocket"]
            self.assertIn("configuration", rocket)
            config = rocket["configuration"]
            self.assertIn("name", config)
            self.assertIn("families", config)
            self.assertIsInstance(config["families"], list)

            # Validate families array element schema if not empty
            if len(config["families"]) > 0:
                family = config["families"][0]
                self.assertIn("name", family)

    def test_upcoming_launches_schema_fixture(self):
        """The widget's field expectations hold for the checked-in API fixture."""
        with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.validate_schema(data)

    @unittest.skipUnless(
        LIVE_MODE,
        "Live API check runs only with LIVE_API_TEST=1 (api-update workflow)",
    )
    def test_upcoming_launches_schema_live(self):
        """The widget's field expectations hold for the live API (gated: rate-limited, shared quota)."""
        url = "https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=5"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                self.assertEqual(response.status, 200)
                data = json.loads(response.read().decode())
                self.validate_schema(data)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(
                    "\n[WARNING] Space Devs API v2.3.0 returned 429 (Rate Limited). Skipping schema verification."
                )
                self.skipTest("API Rate Limit Exceeded")
            else:
                self.fail(f"HTTP error occurred: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            # In live mode a hard failure is correct: it blocks the automated
            # version-bump PR rather than shipping an unverified API change.
            self.fail(f"Failed to reach the API server: {e.reason}")


if __name__ == "__main__":
    unittest.main()
