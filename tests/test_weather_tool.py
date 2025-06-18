import sys
import types
import unittest
from unittest.mock import patch

# Provide a minimal requests module if requests isn't installed
if 'requests' not in sys.modules:
    mock_requests = types.ModuleType('requests')
    def dummy_get(*args, **kwargs):
        raise AssertionError('requests.get should be patched in tests')
    mock_requests.get = dummy_get
    sys.modules['requests'] = mock_requests

from tools import WeatherTool

class WeatherToolTest(unittest.TestCase):
    def test_run_with_dict(self):
        tool = WeatherTool("weather", "dummy_key")
        with patch('tools.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "main": {"temp": 15},
                "weather": [{"description": "clear sky"}]
            }
            result = tool.run({"location": "Paris"})
            self.assertIn("Paris", result)
            called_kwargs = mock_get.call_args.kwargs
            self.assertEqual(called_kwargs['params']['q'], 'Paris')

if __name__ == '__main__':
    unittest.main()
