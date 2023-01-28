import os

class DataSet():
    def __init__(self, symbol: str, period: str) -> None:
        self._symbol = symbol
        self._period = period
        self._split_at = ","

    def read(self, maxsize: int = 10):
        # data = None
        fpath =  os.path.join(os.getcwd(), f"aibot/data/train_data/{self._symbol} - {self._period}.csv")

        try:
            file = open(fpath)
        except FileNotFoundError:
            print("File dont exists !!")

            return None
        
        lines = file.readlines()
        header = lines[0].split(self._split_at)

        if maxsize == -1:
            body = lines[1::]
        else:
            body = lines[1:maxsize + 1]

        data = []

        for row in body:
            column = row.split(self._split_at)
            _row = {}
            
            for i in range(len(column)):

                h = self._escape_string(header[i])
                c = self._escape_string(column[i])

                _row[h] = c

            data.append(_row)

        file.close()

        return data

    def _escape_string(self, string: str):
        if "\n" in string:
            string = string.replace("\n", "")
        
        if self.is_int(string):
            string = int(string)
        elif self.is_float(string):
            string = float(string)
        
        return string

    def is_int(self, string):
        try:
            data = int(string)
        except ValueError:
            return False
        
        return True

    def is_float(self, string):
        try:
            data = float(string)
        except ValueError:
            return False
        
        return True