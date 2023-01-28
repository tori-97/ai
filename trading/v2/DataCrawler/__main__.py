from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from bs4 import BeautifulSoup

from DataCrawler.constants import currencySymbols

from time import sleep
import shutil, os, re

""""
Download data from there = https://data.forexsb.com/data-app
"""

class Browser():
    DATA_PATH = os.path.join(os.getcwd(), "DataCrawler/data")

    def __init__(self) -> None:
        self._options = webdriver.FirefoxOptions()
        self._options.headless = True
        self._driver = webdriver.Firefox(options=self._options)
        self._timeout = 10

    def find_element(self, id):
        return WebDriverWait(self._driver, self._timeout).until(EC.visibility_of_element_located((By.ID, id)))

    def sleep(self, time):
        sleep(time)
    
    @property
    def soup(self):
        return BeautifulSoup(self._driver.page_source, "html.parser")

    @property
    def selected_symbol(self):
        self.sleep(1.5)
        return self.find_element("select-symbol")

    @selected_symbol.setter
    def selected_symbol(self, val):
        symbol = Select(self.selected_symbol)
        symbol.select_by_value(val)

    @property
    def load_data(self):
        self.sleep(2.5)
        return self.find_element("btn-load-data")
    
    @property
    def links(self):
        self.sleep(2.5)
        table =  self.find_element("table-acquisition")
        links = table.find_elements(By.TAG_NAME, "a")
        return links

    @property
    def symbols_list(self):
        s = Select(self.selected_symbol)
        return [s.get_attribute("value") for s in s.options if "──────" != s.get_attribute("value")]

    def download_files(self):
        for link in  self.links:
            link.click()
        
        downloads_folder = os.listdir("/home/tori/Downloads")
        
        for f in downloads_folder:
            if ".csv" in f:
                shutil.move(os.path.join(f"/home/tori/Downloads/", f), os.path.join(os.getcwd(), f"DataCrawler/data/{f}"))
    
    def sort_files(self, symbol):
        free_files = [ f for f in os.listdir(self.DATA_PATH) if os.path.isfile(os.path.join(self.DATA_PATH, f))]
        
        symbol_path = os.path.join(self.DATA_PATH, symbol)
        
        try:
            os.mkdir(symbol_path)
        except FileExistsError:
            pass

        for file in free_files:
            f_path = os.path.join(self.DATA_PATH, file)

            if symbol not in f_path:
                continue

            fname = file.split(".")[0]
            real_fname = re.search("[A-Z]+", fname).group(0)
            real_period = re.search("[0-9]+", fname).group(0)

            shutil.move(f_path, os.path.join(symbol_path, file))

    def adapt_files(self, symbol: str):
        files = os.listdir(os.path.join(self.DATA_PATH, symbol))

        for f in files:
            self.adapt_file(os.path.join(os.path.join(self.DATA_PATH, symbol), f), symbol)

    def adapt_file(self, f_path, symbol):
        with open(f_path) as f:
            data = f.read()
        check_header = data.split("\n")[0]

        if re.match("[a-zA-Z]", check_header):
            print("Has header", check_header)
            return False

        fname = os.path.split(f_path)[-1].split(".")[0]
        period = int(re.search(r"[0-9]+", fname).group(0))

        
        if period == 1:
            period = "M1"
        elif period == 5:
            period = "M5"
        elif period == 15:
            period = "M15"
        elif period == 30:
            period = "M30"
        elif period == 60:
            period = "H1"
        elif period == 240:
            period = "H4"
        elif period == 1440:
            period = "D1"


        symbol_path = os.path.join(self.DATA_PATH, symbol)        

        with open(os.path.join(symbol_path, f"{symbol} - {period}.csv"), "w+") as f:
            data = data.replace("\t", ",")
            f.write("time,open,high,low,close,volume\n")
            f.write(data)
        
        os.remove(f_path)

        return True
        
    def run(self):
        print("[+] Initiating Browser...")
        self._driver.get("https://data.forexsb.com/data-app")

        symbols = self.symbols_list

        for i in range(len(symbols)):    
            print("="*50)
            print(f"[+] Selecting symbol: '{symbols[i]}'")
            self.selected_symbol = symbols[i]
            self.load_data.click()
            print("[+] Loading data...")
            self.download_files()       
            self.sort_files(symbols[i])
            print("[+] Sorting files...")
            self.adapt_files(symbols[i])
            print("[+] Adapting files...")
            print(f"[+] {i + 1}/{len(symbols) + 1} symbols downloaded !!")
            # print("="*50)

        self._driver.close()
        print("[+] Every data is updated !! ")


def main():
    b = Browser()
    b.run()

    """
        todo:
            - add a resume function to resume update on last folder downloaded (if last run was incomplete)
    """



if __name__ == '__main__': 
    main()