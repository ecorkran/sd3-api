import os
import unittest
from dotenv import load_dotenv
from src.api.sd3api import SD3API

# This test costs 6.5 cents to run.
class IntegrationSD3API(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.apiKey = os.getenv('API_KEY_STABILITY')
    def testGenerateImageIntegration(self):
        if os.getenv('RUN_INTEGRATION_TESTS') != 'true':
            self.skipTest("Skipping integration test")

        apiKey = os.getenv('API_KEY_STABILITY')
        sd3Api = SD3API(apiKey=apiKey)
        statusCode, seed, imageData = sd3Api.generateImage(prompt="A scenic mountain landscape", ratio="16:9", imageFormat="png")

        self.assertEqual(statusCode, 200)
        self.assertIsInstance(seed, int)
        self.assertIsNotNone(imageData)


if __name__ == '__main__':
    unittest.main()
