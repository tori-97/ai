import os
import random

from collections import deque
import torch
import torch.nn as nn

from aibot.models.dqn import DQN_Model

device = ("cuda:0" if torch.cuda.is_available() else "cpu")


class Agent():
    N_GAMES = 0
    EPSILON = 0
    GAMMA   = 0.98
    BATCH_SIZE = 1024
    DISCOUNTER = 20
    LR = 0.0035

    BOTS_FOLDER_PATH = os.path.join(os.getcwd(), "aibot/data/bots/")

    def __init__(self, name: str, balance: float, lr: float, gamma: float, batch_size: int) -> None:
        self._name = name
        self.balance = balance
        self.LR = lr
        self.GAMMA = gamma
        self.BATCH_SIZE = batch_size

        self.current_action = "HOLD"

        self._model = DQN_Model(9, 45, 4)
        self._model.to(device=device)

        self._optim = torch.optim.Adam(self._model.parameters(), lr=self.LR)
        self._loss_fn = nn.MSELoss()

        self.memory = deque(maxlen=100_000)

        self._is_running = True
        self.trades = []

    def get_action(self, state):
        self.EPSILON = self.DISCOUNTER - self.N_GAMES
        final_move = [0,0,0,0]
        decision_made_by = ""

        if random.randint(0, 200) < self.EPSILON:
            move = random.randint(0, 2)
            final_move[move] = 1
            HOLD, CLOSE, BULL, BEAR = 0,0,0,0
            _max_arg = self.translate_action_to_human(final_move)

            if _max_arg == "HOLD":
                HOLD = 100.00
            elif _max_arg == "CLOSE":
                CLOSE = 100.00
            elif _max_arg == "BULL":
                BULL = 100.00
            elif _max_arg == "BEAR":
                BEAR = 100.00

            predictions = {
                "hold": HOLD,
                "sell": CLOSE,
                "bull": BULL,
                "bear": BEAR,
                "max": _max_arg
            }
        
            decision_made_by = "random"
        else:

            state_tensor = torch.tensor(state, dtype=torch.float32, device=device)

            with torch.no_grad():
                pred = self._model(state_tensor)
                total = pred.sum()
                argmax = torch.argmax(pred).item()
                final_move[argmax] += 1

                predictions = {
                    "hold": round(float((total / 100) * pred[0].item()), 2),
                    "sell": round(float((total / 100) * pred[1].item()), 2),
                    "bull": round(float((total / 100) * pred[2].item()), 2),
                    "bear": round(float((total / 100) * pred[3].item()), 2),
                    "max": self.translate_action_to_human(final_move)
                }

                decision_made_by = "Bot"
        
        return final_move, predictions, decision_made_by  

    def translate_action_to_human(self, action: list):

        if action[0] == 1:
            return "HOLD"
        elif action[1] == 1:
            return "CLOSE"
        elif action[2] == 1:
            return "BULL"
        elif action[3] == 1:
            return "BEAR"

    def translate_action_to_machine(self, action: str):

        if action == "HOLD":
            return [1,0,0,0]
        elif action == "CLOSE":
            return [0,1,0,0]
        elif action == "BULL":
            return [0,0,1,0]
        elif action == "BEAR":
            return [0,0,0,1]

    def train_long(self): 
        if len(self.memory) > self.BATCH_SIZE:
            mini_sample = random.sample(self.memory, self.BATCH_SIZE)
        
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.optimize(states, actions, rewards, next_states, dones)

    def train_short(self,_state, _action, _reward, _next_state, _done): 
        self.optimize(_state, _action, _reward, _next_state, _done)

    def optimize(self, _state, _action, _reward, _next_state, _done):
        
        state = torch.tensor(_state, dtype=torch.float32, device=device)
        action = torch.tensor(_action, dtype=torch.float32, device=device)
        rewards = torch.tensor(_reward, dtype=torch.float32, device=device)
        next_state = torch.tensor(_next_state, dtype=torch.float32, device=device)
        done = _done

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            rewards = torch.unsqueeze(rewards, 0)
            next_state = torch.unsqueeze(next_state, 0)
            done = (_done, )
        
        pred = self._model(state)
        
        target = pred.clone()
        for idx in range(len(done)):
            q_new = rewards[idx]
            if not done[idx]:
                q_new = rewards[idx] + self.GAMMA * torch.max(self._model(next_state[idx]))
            target[idx][torch.argmax(action[idx]).item()] = q_new

        self._optim.zero_grad()
        loss = self._loss_fn(target, pred)
        loss.backward()
        self._optim.step()

        return loss.item()

    def remember(self, _state, _action, _reward, _next_state, _done):
        self.memory.append((_state, _action, _reward, _next_state, _done))

    def save_current_status(self): 
        fpath  = os.path.join(self.BOTS_FOLDER_PATH, self._name)

        brain = self._model.state_dict()
        optim = self._optim.state_dict()

        torch.save(brain, os.path.join(fpath, "brain.pth"))
        torch.save(optim, os.path.join(fpath, "optim.pth"))

        return True

    def load(self):
        fpath  = os.path.join(self.BOTS_FOLDER_PATH, self._name)

        if "brain.pth" not in os.listdir(fpath) or "optim.pth" not in os.listdir(fpath):
            return False

        brain = torch.load(os.path.join(fpath, 'brain.pth'))
        optim = torch.load(os.path.join(fpath, 'optim.pth'))

        self._model.load_state_dict(brain)
        self._optim.load_state_dict(optim)

        return False

