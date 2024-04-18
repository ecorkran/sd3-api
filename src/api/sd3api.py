import os
import requests
from dotenv import load_dotenv


class SD3API:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.baseUrl = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    def generateImage(self, prompt, negative=None, ratio='16:9', imageFormat='jpeg'):
        headers = {
            'authorization': f'Bearer {self.apiKey}',
            'accept': 'image/*',
#            'content-type': 'multipart/form-data',
#            'output_format': imageFormat,
        }
        files = {
            'none': '',
        }
        payload = {
            "prompt": prompt,
            "negative_prompt": negative,
            "aspect_ratio": ratio,
            "seed": 0,
            "output_format": 'jpeg',
        }

        # todo: just return the image here?  or allow save to file as well.  ideally both because we might
        # todo: want to display it not just save.
        response = requests.post(self.baseUrl, headers=headers, files=files, data=payload)
        if response.status_code == 200:
            with open("./dog-wearing-glasses.jpeg", 'wb') as file:
                file.write(response.content)

        return response.json()


# Example usage
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('API_KEY_STABILITY')
    sd3_api = SD3API(apiKey=api_key)
    result = sd3_api.generateImage(prompt="A scenic mountain landscape", ratio="16:9", imageFormat="png")
    print(result)
