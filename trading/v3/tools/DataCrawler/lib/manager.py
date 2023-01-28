import os
import random

from tools.DataCrawler.lib.parser import parser


class Manager():
    __BASE_PATH = os.path.join(os.getcwd(), "backend/data/train_data")
    
    def __init__(self) -> None:
        pass

    @property
    def list_symbols_available(self):
        """
            List all symbols names with periods.
        """
        _symbols_data = {}
        symbols = os.listdir(self.__BASE_PATH)

        for symbol in symbols:
            periods = self.getSymbolPeriodsByName(symbol)
            _symbols_data[symbol] = periods
            
        return _symbols_data

    def getSymbolPeriodsByName(self, name: str):
        """
            List all symbol periods by name
        """
        try:
            symbol_periods = os.listdir(os.path.join(self.__BASE_PATH, name))
        except FileNotFoundError:
            return None

        symbol_times = []

        for period in symbol_periods:
            file_name = period.split(".")[0]
            _period = file_name.split("-")[-1].strip()
            symbol_times.append(_period)

        return symbol_times

    def getSymbol(self, name: str = "EURUSD", period: str = "D1" ,amount: int = 100, shuffled: bool = False):
        """
            * returns an json object with time,open,close,high,low,volume
        """

        FILE_PATH = os.path.join(self.__BASE_PATH, f"{name}/{name} - {period.upper()}.csv")

        data = []

        try:
            with open(FILE_PATH) as f:
                tmp = f.readlines()
        except FileNotFoundError:
            return None, "Invalid symbol !"
            

        header = tmp[0].split(",")
        body = tmp[1::]

        for i in range(len(body)):
            row = body[i]
            columns = row.split(",")

            _row = {}
            for j in range(len(columns)):
                
                column = self.__parse_column(columns[j])
                header_col = self.__parse_column(header[j])
                _row[header_col] = column

            data.append(_row)

        if int(amount) > 100:
            return None, "Amount is to high , max is 100"
        elif int(amount) < 0:
            return None, "Amount is to low , min is 0"

        data_amount_percentage = int((len(body)) * (int(amount) / 100))
        data = data[0:data_amount_percentage]

        if shuffled == "true" or shuffled == "True":
            data = random.sample(data, len(data))
        
        return data, "success"

    def __getSymbolGen(self, name: str, period: str):
        
        for row in self.getSymbol(name, period):
            yield row

    def __parse_column(self, string: str):
        if "\n" in string:
            string = string.replace("\n", "")

        if parser.is_int(string):
            return int(string)
        elif parser.is_float(string):
            return float(string)
        elif  parser.is_str(string):
            return str(string)