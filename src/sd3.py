import argparse
import os
import sys

from dotenv import load_dotenv
from loguru import logger
from api.sd3api import SD3API

class SD3Options:
    def __init__(self):
        self.prompt = None
        self.negative = None
        self.ratio = None
        self.format = None
        self.valid = False
        self._setOptions()

    def _processArguments(self):
        def addArguments(parser):
            parser.add_argument('-p', '--prompt', required=True, type=str, help='the prompt to pass to the AI model')
            parser.add_argument('-n', '--negative', required=False, type=str, help='negative for what you don\'t want in the image')
            parser.add_argument('-r', '--ratio', required=False, type=str, help='output image aspect ratio')
            parser.add_argument('-f', '--format', required=False, type=str, help='output image format')
            return parser

        parser = argparse.ArgumentParser(description='SD3 Image Generation Options')
        parser = addArguments(parser)

        if len(sys.argv) < 2:
            parser.print_help()
            sys.exit(1)
        else:
            return parser.parse_args()

    def _setOptions(self):
        args = self._processArguments()
        self.prompt = getattr(args, 'prompt', 'masterpiece, banana orbiting the earth')
        self.negative = getattr(args, 'negative', None)
        self.ratio = getattr(args, 'ratio', '16:9')
        self.format = getattr(args, 'format', 'png')
        self.valid = True
        return self


class SD3:
    def __init__(self):
        self.options = SD3Options()

    def run(self):
        if not self.options.valid:
            logger.error("Invalid command line arguments.")
            return

        logger.info(f"Running SD3 with options: prompt='{self.options.prompt}', negative='{self.options.negative}', ratio='{self.options.ratio}', format='{self.options.format}'")
        self._createServices()
        result = self._processCommand()
        print(result)
        return result

    def _createServices(self):
        load_dotenv()  # Load environment variables from .env file
        self.api = SD3API(apiKey=os.getenv('API_KEY_STABILITYAI'))

    # update this allow reading specific news, historical news, current news, or all news.
    # add tests for this and release.  then you should be able to start playing with stuff.
    def _processCommand(self):
        logger.trace(f"Processing command line arguments: {self.options}")

        result = self.api.generateImage(prompt=self.options.prompt, negative=self.options.negative, ratio=self.options.ratio, imageFormat=self.options.format)
        return result


def main():
    app = SD3()
    return app.run()

# Remember that to run these, use python -m src.sd3 as they are modules.
if __name__ == "__main__":
    main()
