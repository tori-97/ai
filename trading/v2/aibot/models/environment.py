"""
    * Environment
"""
class Environment():
    def __init__(self, start_balance: float) -> None:
        self.start_balance = start_balance
        self.balance = self.start_balance

        self._position = None
        self._steps_open = 0

    def reset(self):
        self._position = None
        self._steps_open = 0

    def _hold_position(self, day: dict):
        """
            if position is not none:
                add rewards if profit is over 0
                reduce rewards if profit is under 0
            else:
                remove one reward for each step position is none
        """
        rewards = 10


        if self._position is not None:
            open_amount = self._position['open_amount']
            side = self._position['side']
            current_amount = self._position['amount'] * day.get('close')

            if side == 'BULL':
                diff = current_amount - open_amount
            elif side == "BEAR":
                diff = open_amount - current_amount

            if diff > 0:
                rewards += diff * 0.025
            else:            
                rewards = 0

        else:
            rewards = 0        


        return rewards

    def _open_position(self, day: dict, side: str, amount: float):
        """
            get 20 rewards to open new position
        """
        rewards, done, info = 20, False, None

        if self._position is not None:
            rewards = 0

        else:

            if self.balance < amount:
                rewards = 0
                done = True
                info = "no-balance"
            else:
                self._position = {
                    'open_at': day.get("time"),
                    'open_price': day.get("close"),
                    'open_amount': day.get("close") * amount,
                    'side': side,
                    'amount': amount
                }

                self.balance -= round(amount, 2)

        return rewards, done, info

    def _close_position(self, day: dict):
        """
            if profit is over 0
                get profit + small bonus
            if profit is under 0
                remove total rewards - profit
        """
        rewards = 100

        if self._position is None:
            rewards = 0
        
        else:
            side = self._position.get('side')

            self._position['close_price'] = day.get('close')
            self._position['close_at'] = day.get('time')
            self._position['close_amount'] = day.get('close') * self._position['amount']

            if side == "BULL":
                self._position['profit'] = round(self._position.get('close_amount') - self._position.get("open_amount"), 2)
            elif side == "BEAR":
                self._position['profit'] = round(self._position.get("open_amount") - self._position.get('close_amount'), 2)

            if self._position['profit'] > self._position['amount']:
                self.balance += round(self._position['profit'], 2)
            elif self._position['profit'] <= self._position['amount']:
                self.balance -= round(self._position['profit'], 2)

            rewards *= self._position['profit'] * 0.25

        return rewards

    def step(self, action: str, day: dict):
        done, rewards, info = False, 0, None

        invest_amount = self.balance * 0.75

        if action == "HOLD":
            rewards = self._hold_position(day)
        elif action == "BULL":
            rewards, done, info = self._open_position(day, "BULL", invest_amount)

        elif action == "BEAR":
            rewards, done, info = self._open_position(day, "BEAR", invest_amount)

        elif action == "CLOSE":
            rewards = self._close_position(day)
            info = self._position
            done = True
        
        if self._position is not None:
            self._steps_open += 1

        return done, rewards, info

    def getState(self, day: dict, action: str):
        return [
            # day.get("time"),
            day.get("open"),
            day.get("close"),
            day.get("high"),
            day.get("low"),
            day.get("volume"),
            
            1 if action == "HOLD" else 0,
            1 if action == "BULL" else 0,
            1 if action == "BEAR" else 0,
            1 if action == "CLOSE" else 0,
        ]
