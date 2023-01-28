from time import sleep
from threading import Thread, Lock
import random
from tools.AiTrader.lib import Agent, Environment


class TrainingRoom(Thread):
    def __init__(self, 
        handler,
        data: list,
        name: str,
        balance: float, min_balance: float,
        lr: float, gamma: float, batch_size: int,
        min_episodes: int, max_episodes: int,
        discounter_rate: int,
        train_speed: float
    ) -> None:
        super().__init__()

        self.handler        = handler
        self.data           = data
        self.name           = str(name)
        self.balance        = float(balance)
        self.min_balance    = float(min_balance)
        self.lr             = float(lr)
        self.gamma          = float(gamma)
        self.batch_size     = int(batch_size )
        self.discounter_rate= int(discounter_rate)
        self.min_episodes   = int(min_episodes)
        self.max_episodes   = int(max_episodes)
        self.current_episode = 0
        self.training_speed = train_speed

        self._killed        = False
        self.paused         = False
        self.locker         = Lock()

        self.agent          = Agent(self.name, self.balance, self.lr, self.gamma, self.batch_size, self.discounter_rate)
        self.env            = Environment(self.agent.balance)
    
    def _paused(self):
        while self.paused:
            self.handler.report(inner_task={
                "name": "status",
                "data": "paused"
            })            

            sleep(1)
        self.locker.release()
    
    def pause(self, on: bool):
        if on:
            self.paused = True
        else:
            self.paused = False
        
    def kill(self): self._killed = True

    def _train_step(self, row, nrow):
        # get state
        state = self.env.getState(row, self.agent.current_action)
        # get action
        self.agent.current_action, predictions, decision_made_by = self.agent.get_action(state)
        # # do environment step
        done, rewards, info = self.env.step(self.agent.translate_action_to_human(self.agent.current_action), row)
        # # get next state
        next_state = self.env.getState(nrow, self.agent.current_action)
        # # optimize agent
        self.agent.train_short(state, self.agent.current_action, rewards, next_state, done)
        # # remember agent
        self.agent.remember(state, self.agent.current_action, rewards, next_state, done)

        return done, predictions, decision_made_by, rewards, info

    def _training(self):
        break_out = False
        break_msg = ""

        # Training info:

        self.agent.load()

        for episode in range(1, self.max_episodes + 1):
            self.current_episode = episode

            if self._killed:
                break

            self.__check_pause()
            # print(f"Episode: {episode}")
            self.env.reset()

            if break_out:
                break

            for day in range(len(self.data) - 1):
                if self._killed:
                    break_out = True

                self.__check_pause()

                if int(self.env.balance) <= 0:
                    break_out = True
                    break_msg = "No balance anymore !!"
                    
                if break_out:
                    break
            
                today = self.data[day]

                if (day + 1) > len(self.data):
                    tomorrow = today
                else:
                    tomorrow = self.data[day + 1]

                done, predictions, decision_made_by, rewards, info = self._train_step(today, tomorrow)
                done = False

                if done:
                    self.env.reset()
                    self.agent.train_long()

                # Update Training Infos
     
                self.handler.report(inner_task={
                    'name': 'update',
                    'data': {
                        'id': self.name,
                        'episode': episode,
                        'day': day,
                        'balance': round(self.env.balance, 2),
                        'predictions': predictions,
                        'decision_made_by': decision_made_by,
                        'rewards': rewards,
                        'info': info
                    }
                })

                # sleep(random.uniform(0.05, 0.25))
                sleep(self.training_speed)

        self._killed = True

    def __check_pause(self):
        if self.paused:
            self.locker.acquire()
            self._paused()

    def run(self):
   
        while not self._killed:
            self.__check_pause()
            self._training()

        print(f"Thread: {self.name} is done")
        self.handler.report(inner_task={
            "name": "game-over",
            "data": self.name
        })