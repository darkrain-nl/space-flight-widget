import unittest
import urllib.request
import urllib.error
import json

class TestSpaceDevsAPI(unittest.TestCase):
    def test_upcoming_launches_schema(self):
        url = "https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=5"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                self.assertEqual(response.status, 200)
                data = json.loads(response.read().decode())
                
                self.assertIn('results', data)
                results = data['results']
                self.assertIsInstance(results, list)
                
                # If there are results, validate the schema of the first item
                if len(results) > 0:
                    launch = results[0]
                    self.assertIn('name', launch)
                    self.assertIn('net', launch)
                    self.assertIn('net_precision', launch)
                    self.assertIn('rocket', launch)
                    
                    # Validate net_precision id
                    self.assertIn('id', launch['net_precision'])
                    self.assertIsInstance(launch['net_precision']['id'], int)
                    
                    # Validate rocket configuration and families
                    rocket = launch['rocket']
                    self.assertIn('configuration', rocket)
                    config = rocket['configuration']
                    self.assertIn('name', config)
                    self.assertIn('families', config)
                    self.assertIsInstance(config['families'], list)
                    
                    # Validate families array element schema if not empty
                    if len(config['families']) > 0:
                        family = config['families'][0]
                        self.assertIn('name', family)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("\n[WARNING] Space Devs API v2.3.0 returned 429 (Rate Limited). Skipping schema verification.")
                self.skipTest("API Rate Limit Exceeded")
            else:
                self.fail(f"HTTP error occurred: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            self.fail(f"Failed to reach the API server: {e.reason}")

if __name__ == '__main__':
    unittest.main()
