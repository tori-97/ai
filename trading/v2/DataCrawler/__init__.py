from selenium.webdriver import Firefox
from selenium.webdriver.common.service import Service

import os

class Browser():

    def __init__(self) -> None:
        self.GECKO_PATH = os.path.join(os.getcwd(), "ForexCrawler/lib/gecko-64")

        self._service = Service(executable=self.GECKO_PATH)
        self._browser = Firefox(service=self._service)
       
        print(self.GECKO_PATH)


__all__ = [
    "Browser"
]