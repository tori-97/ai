from time import sleep
import os, json
import random

DATA_PATH = os.path.join(os.getcwd(), "backend/data/train_data")

from tools.DataCrawler import Browser, Manager

class Data():
    """
        * Handles train Data 
    """
    def __init__(self, handler) -> None:
        self.handler = handler
    
    # def _update(self, browser: Browser, symbol, i):
    #     print("="*50)
    #     print(f"[+] Selecting symbol: '{symbol}'")
    #     browser.selected_symbol = symbol
    #     browser.load_data.click()
    #     print("[+] Loading data...")
    #     browser.download_files()       
    #     browser.sort_files(symbol)
    #     print("[+] Sorting files...")
    #     browser.adapt_files(symbol)
    #     print("[+] Adapting files...")
    #     print("="*50)

    # def do_update_all(self):       
    #     browser = Browser()
    #     print("[+] Initiating Browser...")
    #     browser.get_page()

    #     symbols = browser.symbols_list

    #     updated = {}

    #     for i in range(len(symbols)): 
    #         error = "no errors"
            
    #         if symbols[i] in os.listdir(DATA_PATH):
    #             error = "Already exists !!"
    #             continue
            
    #         try:   
    #             self._update(browser, symbols[i], i)
    #         except Exception as e:
    #             error = "Something wents wrong !!"
            
    #         updated[symbols[i]] = {
    #             'at': str(datetime.now()),
    #             'error': error
    #         }

    #         self.handler.report(f"[+] {i + 1}/{len(symbols) + 1} symbols processed !!", inner_task = updated)

    #     browser.close()
    #     self.handler.report("[+] Every data is updated !! ", True)

    # def do_manager_get_available_symbols(self):
    #     manager = Manager()
    #     manager.list_symbols_available

        self._manager = Manager()

    def do_manager_symbols(self): 
        data = json.loads(self.handler.params)
        symbol_name = data.get("name")
        period = data.get("period")
        maxlen = data.get("maxlen")
        shuffle = data.get("shuffle")

        if symbol_name is None or period is None:
            self.handler.report("Symbol or period cannot be empty !!")
            return None
        
        symbol, msg = self._manager.getSymbol(symbol_name, period)
        
        if symbol is None:
            self.handler.report("Symbol or period don't exists !!")
            return None

        days = [ x.get('time') for x in symbol]
        closes = [ x.get('close') for x in symbol]

        if shuffle is not None:
            if isinstance(shuffle, str):
                if shuffle.lower() == "false":
                    shuffle = False
                elif shuffle.lower() == "true":
                    shuffle = True
            
            if shuffle:
                days = random.sample(days, len(days))
                closes = random.sample(closes, len(closes))

        if maxlen is not None:
            maxpercent = int(len(days) * (int(maxlen) / 100))
            days = days[0:maxpercent]
            closes = closes[0:maxpercent]

        self.handler.report(data={"days": days, "closes": closes, "data_len": len(closes), 'symbol': symbol_name, 'period': period}, done=True)

    def do_manager_symbols_all(self):
        symbols = list(self._manager.list_symbols_available.keys())
        self.handler.report(data=symbols)
        
    def do_manager_symbols_update(self):
        data = json.loads(self.handler.params)
        symbol_name = data.get("name")

        browser = Browser(True)
        browser.get_page()
        available = browser.symbols_list

        if symbol_name.upper() not in available:
            self.handler.report("Symbol is not available to download !!")
            browser.close()
            return None

        self.handler.report(f"[+] Selecting symbol: '{symbol_name}'", data={
            'name': symbol_name,
            'load': 10
        })
        browser.selected_symbol = symbol_name
        browser.load_data.click()
        self.handler.report("[+] Loading data...", data={
            'name': symbol_name,
            'load': 25
        })
        browser.download_files()      
        # browser.move_files(symbol_name)    
        browser.sort_files(symbol_name)
        self.handler.report("[+] Sorting files...", data={
            'name': symbol_name,
            'load': 50
        })
        browser.adapt_files(symbol_name)
        self.handler.report("[+] Adapting files...", data={
            'name': symbol_name,
            'load': 75
        })

        browser.close()
        sleep(2)
        self.handler.report("[+] Symbol updated !!", data={
            'name': symbol_name,
            'load': 100
        }, done=True)

    def do_manager_symbols_available(self):
        symbols = self._manager.list_symbols_available
        self.handler.report(done=True, data=symbols)

    def do_manager_symbols_all_update(self):
        browser = Browser(True)
        browser.get_page()
        available = browser.symbols_list

        for i in range(len(available)):
            symbol_name = available[i]

            browser.selected_symbol = symbol_name
            browser.load_data.click()
            browser.download_files()   
            browser.move_files(symbol_name)    
            browser.sort_files(symbol_name)
            browser.adapt_files(symbol_name)

            self.handler.report(f"[+] Updating {i+ 1}/{len(available) + 1} [{(100 / (len(available) + 1)) * (i + 1):.2f} %] symbols...")
            sleep(1)

        browser.close()
        sleep(2)
        self.handler.report("[+] Symbols updated !!")

    def do_manager_symbols_downloadable(self): 
        self.handler.report("Loading symbols..")
        browser = Browser(True)
        browser.get_page()
        available = browser.symbols_list
        browser.close()
        self.handler.report(done=True, data=available)

    def do_manager_symbols_periods(self): 
        name = json.loads(self.handler.params).get("name")

        if name is None:
            self.handler.report("You need provide a symbol name !!")
            return None

        periods = self._manager.getSymbolPeriodsByName(name)

        if periods is None:
            self.handler.report("Symbol cannot be empty !!", done=False)
            return None

        self.handler.report(data=periods, done=True)

