import os


class parser():

    @classmethod
    def is_int(cls, string: str):
        try:
            int(string)
        except ValueError:
            return False
        return True

    @classmethod
    def is_float(cls, string: str):
        try:
            float(string)
        except ValueError:
            return False
        return True

    @classmethod
    def is_str(cls, string: str):
        try:
            str(string)
        except ValueError:
            return False
        return True
    
    @classmethod
    def is_bool(cls, string: str):
        try:
            bool(string)
        except ValueError:
            return False
        return True

class DataSet():
    __BASE_PATH = os.path.join(os.getcwd(), "DataCrawler/data")
    
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
        symbol_periods = os.listdir(os.path.join(self.__BASE_PATH, name))

        symbol_times = []

        for period in symbol_periods:
            file_name = period.split(".")[0]
            _period = file_name.split("-")[-1].strip()
            symbol_times.append(_period)

        return symbol_times

    def getSymbol(self, name: str, period: str, generator_mode: bool):
        """
            * returns an json object with time,open,close,high,low,volume
        """

        FILE_PATH = os.path.join(self.__BASE_PATH, f"{name}/{name} - {period}.csv")

        data = []

        with open(FILE_PATH) as f:

            tmp = f.readlines()

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

        # if not generator_mode:
        #     return data

        if not generator_mode:
            return data

        return self.__getSymbolGen(name, period)

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