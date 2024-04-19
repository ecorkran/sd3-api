import unittest
import base64
import requests

from unittest.mock import patch, Mock
from src.api.sd3api import SD3API


class TestSD3API(unittest.TestCase):
    @patch('src.api.sd3api.requests.post')
    def testGenerateImageSuccess(self, mockPost):
        # Setup mock response data
        mockResponse = Mock()
        expectedSeed = 123456
        expectedImageData = base64.b64encode(b"fake_image_data").decode()
        mockResponse.json.return_value = {
            'seed': expectedSeed,
            'image': expectedImageData
        }
        mockResponse.status_code = 200
        mockPost.return_value = mockResponse

        # Call generateImage
        sd3Api = SD3API(apiKey="dummy_api_key")
        statusCode, seed, imageData = sd3Api.generateImage(prompt="A scenic mountain landscape")

        # Assert the status code, seed, and image data are as expected
        self.assertEqual(statusCode, 200)
        self.assertEqual(seed, expectedSeed)
        self.assertEqual(imageData, b"fake_image_data")

    @patch('src.api.sd3api.requests.post')
    def testGenerateImageFailure(self, mockPost):
        # Setup mock to raise a request exception
        mockPost.side_effect = requests.exceptions.RequestException("API failure")

        # Call generateImage
        sd3Api = SD3API(apiKey="dummy_api_key")
        statusCode, seed, imageData = sd3Api.generateImage(prompt="A scenic mountain landscape")

        # Assert a failure status code is returned
        self.assertEqual(statusCode, 500)
        self.assertEqual(seed, 0)
        self.assertIsNone(imageData)


if __name__ == '__main__':
    unittest.main()
