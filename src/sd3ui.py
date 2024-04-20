import io
import os
from PIL import Image
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger
from src.api.sd3api import SD3API
from src.ui.homepage import HomePage


class SD3UI:
    def __init__(self):
        def getEnvPath(envVar, default):
            return os.getenv(envVar) or default

        self.basePath = getEnvPath('BASE_PATH', os.getcwd())
        self.inputImagePath = os.path.normpath(os.path.join(self.basePath, getEnvPath('INPUT_PATH', 'input'), getEnvPath('INPUT_IMAGE_PATH', 'images')))
        self.outputTxt2ImgPath = os.path.normpath(os.path.join(self.basePath, getEnvPath('OUTPUT_PATH', 'output'), getEnvPath('TXT2IMG_PATH', 'txt2img')))
        self.outputImg2ImgPath = os.path.normpath(os.path.join(self.basePath, getEnvPath('OUTPUT_PATH', 'output'), getEnvPath('IMG2IMG_PATH', 'img2img')))
        self.serverName = os.getenv('UI_SERVER_NAME')
        self.serverPort = os.getenv('UI_SERVER_PORT')

        self.baseName = "image"
        self.dateFormat = "%Y%m%d%H"
        self.imageFormat = "png"

    def runui(self):
        self._createServices()
        HomePage.launchUI(self.generateImage)

    def _createServices(self):
        self.api = SD3API(apiKey=os.getenv('API_KEY_STABILITY'))

    # Function to generate a non-conflicting filename with a base, date, and incrementing index.
    def generateFileName(self, baseName, dateFormat, outputPath, fileExtension):

        # Get the current time and format it as a string.
        date_str = datetime.now().strftime(dateFormat)
        index = 1  # Start index at 1 for each run
        while True:
            # Generate a filename with the base name, date, and index.
            filename = f"{baseName}-{date_str}-{index}.{fileExtension}"
            file_path = os.path.join(outputPath, filename)

            # Check if the file already exists. If it doesn't, break out of the loop.
            if not os.path.exists(file_path):
                break
            index += 1  # Increment the index if the file exists.

        return file_path

    @staticmethod
    def convertBytesToImage(byte_data):
        image_stream = io.BytesIO(byte_data)
        image = Image.open(image_stream)
        return image

    # Generate an image and save it to a (mostly) non-conflicting filename.
    def generateImage(self, prompt="masterpiece, a large banana floating in space",
                      negative=None, ratio='16:9', imageFormat='png', seed=0):
        status, seed, image = self.api.generateImage(prompt=prompt, negative=negative, ratio=ratio, imageFormat=imageFormat, seed=seed)

        if status == 200:
            filePath = self.generateFileName(self.baseName, self.dateFormat, self.outputTxt2ImgPath, self.imageFormat)

            with open(filePath, 'wb') as file:
                file.write(image)

            return SD3UI.convertBytesToImage(image), seed

        else:
            logger.error(f"Failed to generate image.  Status: {status}, content: {image}")

        return image, seed


def main():
    load_dotenv()
    app = SD3UI()
    return app.runui()


# Remember that to run these, use python -m src.sd3 as they are modules.
if __name__ == "__main__":
    main()
