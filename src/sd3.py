import argparse
import os
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger
from src.api.sd3api import SD3API


class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, max_help_position=50, width=120, **kwargs)


class SD3Options:
    def __init__(self):
        self.prompt = None
        self.negative = None
        self.ratio = None
        self.format = None
        self.valid = False
        self.outputTxt2ImgPath = None
        self.outputImg2ImgPath = None
        self.inputImagePath = None
        self.baseName = "image"
        self.dateFormat = "%Y%m%d%H"
        self._setOptions()

    def _processArguments(self):
        def addArguments(_parser):
            _parser.add_argument('-p', '--prompt', required=False, type=str, default='masterpiece, banana orbiting the earth',
                                 help='the prompt to pass to the AI model')
            _parser.add_argument('-n', '--negative', required=False, type=str, help='negative for what you don\'t want in the image')
            _parser.add_argument('-r', '--ratio', required=False, type=str, default='16:9', help='output image aspect ratio')
            _parser.add_argument('-f', '--format', required=False, type=str, default='png', help='output image format')
            return _parser

        parser = argparse.ArgumentParser(
            description='SD3 Image Generation Options',
            formatter_class=CustomHelpFormatter,
        )
        parser = addArguments(parser)

        return parser.parse_args()

    def _setOptions(self):
        def getEnvPath(envVar, default):
            return os.getenv(envVar) or default

        args = self._processArguments()
        self.prompt = getattr(args, 'prompt')
        self.negative = getattr(args, 'negative')
        self.ratio = getattr(args, 'ratio')
        self.format = getattr(args, 'format')
        self.valid = True

        basePath = getEnvPath('BASE_PATH', os.getcwd())
        self.inputImagePath = os.path.normpath(os.path.join(basePath, getEnvPath('INPUT_PATH', 'input'), getEnvPath('INPUT_IMAGE_PATH', 'images')))
        self.outputTxt2ImgPath = os.path.normpath(os.path.join(basePath, getEnvPath('OUTPUT_PATH', 'output'), getEnvPath('TXT2IMG_PATH', 'txt2img')))
        self.outputImg2ImgPath = os.path.normpath(os.path.join(basePath, getEnvPath('OUTPUT_PATH', 'output'), getEnvPath('IMG2IMG_PATH', 'img2img')))

        return self


class SD3:
    def __init__(self):
        self.options = SD3Options()

    def run(self):
        if not self.options.valid:
            logger.error("Invalid command line arguments.")
            return

        logger.info(
            f"Running SD3 with options: prompt='{self.options.prompt}', negative='{self.options.negative}', ratio='{self.options.ratio}', format='{self.options.format}'")
        self._createServices()
        result = self._processCommand()
        return result

    def _createServices(self):
        self.api = SD3API(apiKey=os.getenv('API_KEY_STABILITY'))

    # Function to generate a non-conflicting filename with a base, date, and incrementing index.
    @staticmethod
    def generateFileName(baseName, dateFormat, outputPath, fileExtension):

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

    # update this allow reading specific news, historical news, current news, or all news.
    # add tests for this and release.  then you should be able to start playing with stuff.
    def _processCommand(self):
        logger.trace(f"Processing command line arguments: {self.options}")

        # only command supported right now is text2image.
        status, seed, image = self.api.generateImage(prompt=self.options.prompt, negative=self.options.negative, ratio=self.options.ratio,
                                                     imageFormat=self.options.format)

        if status == 200:
            filePath = self.generateFileName(self.options.baseName, self.options.dateFormat, self.options.outputTxt2ImgPath, self.options.format)

            with open(filePath, 'wb') as file:
                file.write(image)

        else:
            logger.error(f"Failed to generate image.  Status: {status}, content: {image}")

        return status == 200


def main():
    load_dotenv()
    app = SD3()
    return app.run()


# Remember that to run these, use python -m src.sd3 as they are modules.
if __name__ == "__main__":
    main()
