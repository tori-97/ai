import pandas as pd
from datetime import timedelta

from ai_trader.exceptions import InvalidDataFile

class TradingEnvironment():
    def __init__(self, symbol: str = "EURUSD", period: str = "D1", start_balance: float = 10000.00 ) -> None:
        
        self._symbol = symbol
        self._period = period
        self._start_balance = start_balance
        self._balance = self._start_balance

        self.days = self._get_data()      

        self._trades = []
        self._position = None
        self._current_action = 0 # hold
        self.minimun_trades_need = 10

    @property 
    def trades(self):
        return self._trades
    
    @trades.setter
    def trades(self, val): self._trades = val

    @property
    def start_balance(self): return self._start_balance

    @start_balance.setter
    def start_balance(self, val): self._start_balance = val

    @property
    def balance(self): return self._balance
    
    @balance.setter
    def balance(self, val): self._balance = val
        
    def _get_data(self) -> pd.DataFrame:
        """
            * Find requested file in data folder and returns pandas dataframe
        """
        try:
            dframe = pd.read_csv(f"./ai_trader/data/{self._symbol} - {self._period}.csv")
        except FileNotFoundError:
            raise InvalidDataFile("No Data File found !!")
        else:
            dframe.time = pd.to_datetime(dframe.time)
               
        return dframe
    
    def reset(self): 
        self._position = None
        self._current_action = 0
        
    def step(self, action: list, current_day): 
        done = False
        rewards = -100
        profit = 0
        buy = None
        close = None

        if action[0] == 1: # HOLD
            self._current_action = 0
            if self._position is None:
                rewards += 100
            elif self._position is not None:
                open_time = self._position.get("open_time")
                diff = current_day.time - open_time

                if int(diff.days) >= 3:
                    rewards += -500
                    # profit = self._sell_position(current_day.close, current_day.time)
                    # done = True
                    # self._position = None
                    # close = current_day.close

        elif action[1] == 1: # LONG
            self._current_action = 1
            if self._position is None and self._balance > 0:
                self._buy_position(current_day.close, current_day.time, "long", (self._balance * 0.25))
                buy = current_day.close
                rewards += 110

        elif action[2] == 1: # SHORT
            self._current_action = 2
            if self._position is None and self._balance > 0:
                self._buy_position(current_day.close, current_day.time, "short", (self._balance * 0.25))
                buy = current_day.close
                rewards += 110

        elif action[3] == 1: # SELL
            self._current_action = 3
            if self._position is not None:
                profit = self._sell_position(current_day.close, current_day.time)
                done = True
                rewards += profit * 0.25
                self._position = None
                close = current_day.close
            else:
                rewards -= 100

        diff = self.balance - self.start_balance

        if self.balance > self.start_balance:
            rewards += diff * 0.15
        elif self.balance < self.start_balance:
            rewards -= diff * 0.1
        
        total_trades = len(self._trades)

        if total_trades < self.minimun_trades_need:
            rewards += -300

        return done, rewards, profit, (buy, close)
    
    def get_state(self, current_day):
        if isinstance(current_day, dict):
            return [
                current_day.get("time"),
                current_day.get("open"),
                current_day.get("close"),
                current_day.get("high"),
                current_day.get("low"),
                current_day.get("volume"),

                1 if self._current_action == 0 else 0,
                1 if self._current_action == 1 else 0,
                1 if self._current_action == 2 else 0,
                1 if self._current_action == 3 else 0
            ]

        else:

            return [
                current_day.time.timestamp(),
                current_day.open,
                current_day.close,
                current_day.high,
                current_day.low,
                current_day.volume,

                1 if self._current_action == 0 else 0,
                1 if self._current_action == 1 else 0,
                1 if self._current_action == 2 else 0,
                1 if self._current_action == 3 else 0
            ]

    def _buy_position(self, close, time, direction, amount): 
        self._position = {
            "open_price": close,
            "open_time": time,
            "direction": direction,
            "amount": amount
        }

        self._balance -= amount
   
    def _sell_position(self, close, time):
        self._position["close_price"] = close
        self._position["close_time"] = time
        self._position["profit"] = self._calculate_profit()

        if self._position.get("profit") > 0:
            self._balance += self._position.get("profit") + self._position.get("amount")
        elif self._position.get("profit") < 0:
            self._balance +=  self._position.get("amount") - self._position.get("profit")

        self._trades.append(self._position)

        return self._position.get("profit")

    def _calculate_profit(self):
        open_price = (self._position.get("open_price")) * self._position.get("amount")
        close_price = (self._position.get("close_price")) * self._position.get("amount")
        profit = 0

        if self._position.get('direction') == "long":
            profit = close_price - open_price
        elif self._position.get('direction') == "short":
            profit = open_price - close_price
        
        return profit
