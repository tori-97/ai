import os
import random
from collections import deque

import torch
import torch.nn as nn

from ai_trader.trader.model import DQN_Model

device = ("cuda:0" if torch.cuda.is_available() else "cpu")

class Agent():
    EPSILON = 0

    def __init__(self, name: str = "Gaspar", lr: float = 0.0025, gamma: float = 0.98, batch_size: int = 50, model_hidden_layers: int = 64, brain_fpath: str = "brain.pth", optim_fpath: str = "optim.pth") -> None:
        self._name = name
        self.LR = lr
        self.GAMMA = gamma
        self.BATCH_SIZE = batch_size

        # TODO: Secure against path injection
        self._brain_fpath = os.path.join(os.getcwd(), f"ai_trader/data/model/{brain_fpath}")
        self._optim_fpath = os.path.join(os.getcwd(), f"ai_trader/data/model/{optim_fpath}")

        self._n_games = 0

        self._model   = DQN_Model(10, model_hidden_layers, 4)
        self._model.to(device)
        self._optim   = torch.optim.Adam(self._model.parameters(), lr=self.LR)
        self._loss_fn = nn.MSELoss()
        self._memory  = deque(maxlen=100_000)

    @property
    def n_trades(self): return self._n_games

    @n_trades.setter
    def n_trades(self, val): self._n_games = val

    def get_action(self, state):
        self.EPSILON = 80 - self._n_games
        final_move = [0,0,0,0]
        decision_made_by = ""
        pred_percent = {"hold": 0.00, "long": 0.00, "short": 0.00, "sell": 0.00}

        if random.randint(0, 200) < self.EPSILON:
            move = random.randint(0, 3)
            final_move[move] = 1
            decision_made_by = "random"
        else:
            if isinstance(state, list):
                state = torch.tensor(state, dtype=torch.float32, device=device)

                with torch.no_grad():
                    decision_made_by = "bot"
                    pred = self._model(state)
                    final_move[torch.argmax(pred).item()] = 1
                    pred_percent = {
                        "hold": round(pred[0].item(), 2),
                        "long": round(pred[1].item(), 2),
                        "short": round(pred[2].item(), 2),
                        "sell": round(pred[3].item(), 2),
                    }


        return final_move, decision_made_by, pred_percent

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

    def optimize_long_memory(self):
        if len(self._memory) > self.BATCH_SIZE:
            mini_sample = random.sample(self._memory, self.BATCH_SIZE)
        
        else:
            mini_sample = self._memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.optimize(states, actions, rewards, next_states, dones)

    def remember(self, state, action, rewards, next_state, done):
        self._memory.append((state, action, rewards, next_state, done))
    
    def save(self):
        torch.save(self._model.state_dict(), self._brain_fpath)
        torch.save(self._optim.state_dict(), self._optim_fpath)
        
        return True

    def load(self):
        try:
            brain = torch.load(self._brain_fpath)
            optim = torch.load(self._optim_fpath)
        except FileNotFoundError:
            return False, "File not found"
        except Exception as e:
            return False, f"{e}"
        else:
            self._model.load_state_dict(brain)
            self._optim.load_state_dict(optim)
        
        return True