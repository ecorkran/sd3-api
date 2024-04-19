import base64
import os
import requests
from dotenv import load_dotenv


class SD3API:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.baseUrl = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    def generateImage(self, prompt, negative=None, ratio='16:9', imageFormat='png'):
        headers = {
            'authorization': f'Bearer {self.apiKey}',
            'accept': 'application/json',
        }
        files = {
            'none': '',
        }
        payload = {
            "prompt": prompt,
            "negative_prompt": negative,
            "aspect_ratio": ratio,
            "seed": 0,
            "output_format": imageFormat,
        }

        try:
            response = requests.post(self.baseUrl, headers=headers, files=files, data=payload)
            if response.status_code == 200:
                json = response.json()
                return response.status_code, json['seed'], base64.b64decode(json['image']),

            return response.status_code, 0, None

        except requests.exceptions.RequestException as e:
            print(e)
            return 500, 0, e.response


# Example usage
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('API_KEY_STABILITY')
    sd3_api = SD3API(apiKey=api_key)
    result = sd3_api.generateImage(prompt="A scenic mountain landscape", ratio="16:9", imageFormat="png")
    print(result)
