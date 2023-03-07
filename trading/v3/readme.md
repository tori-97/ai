# Ai Trading app

## requires:
    - backend:
        - aibot
        - webapi
        - websocket
    
    - frontend:
        - ai-trading-application



## TODO:

- [x] Adapt start training modal
- [x] create bots view
- [x] Custom add annotations to show all bot positions
- [x] Adding multithreading to bot
- [x] Add pause mode to bot
- [x] Add stop mode to bot ( is still not work , will need also to be checked during training runntime)
- [ ] Find Max and min values for train speed , to not have bots flying
- [ ] Home Add Bots Counter with traingings success
- [x] Add threads Sections in sidebar to show each bot with each balance, episode, day
- [ ] Add ClientMessage to Application to shows popups on pages
- [ ] Add message between starting stop threads and stopped threads and the same for pausing threads
- [ ] Try to add tasks running in the background to be able to change pages ( probably with task ids could this work)

# UI:
    - views:
        - Home:
            * shows currents statistics and bots
        - bots:
            * Bots Manager
                - needs to be able to:
                    - create
                    - edit
                    - delete
                    - open details
        - bot:
            * BotInfoPage:
                - needs to be able to:
                    - list all trainings
                        - training:
                            - id
                            - episodes
                            - days
                            - maxprofit
                            - etc...

                    - list all records:
                        - episodes
                        - days reached
                        - profit
                        - balance
                        - trades
                            - shorts counter
                            - longs counter

                    - list trainings statistics:
                        - bot success
                        - bot wins amount
                        - bot looses amount
                        - bot loss mean amount

        - training-room:
            * Training Room
                - needs to be able to:
                    - start training
                        * Botname
                        * traindataamount
                        * balance
                        * learning-rate
                        * gamma
                        * batchsize
                        * max-epsiodes
                        * min-epsiodes

                        * symbol
                        * period

                        * build training rows
                        * drag training rows to change sortiment

                    - pause training
                    - stop training
                    - list training information
                        - information:
                            * episodes
                            * days
                            * resets
                            * rewards
                            * decisionby
                        - records
                            * maxepisodes
                            * maxdays
                            * maxprofit
                            * maxbalance
                            * maxtrades
                            * maxrewards
                    - list predictions information:
                        * hold
                        * close
                        * bull
                        * bear
                    - list trades information
                        * open price
                        * open at
                        * close price
                        * close at
                    - show graph
                        * days
                        * closes
        - Data:
            * Data Manager
    
# WebSocket:
```
request:
    {
        query: string,
        view: string,
        params: {custom?}
    }

response:
    {
        name: query,
        view: string, 
        done: boolean,
        data: {custom?},
        client_msg: string | null,
        inner_task: task
    }
```

## tasks:
```
# Client:
    - client-is-open
    - client-is-closed

    # Bots:
        - bots-create 
            * params: {
                name: string,
                lr: float,
                hidden_layers: int,
                gamma: float,
                discounter_rate: int
            }
        - bots-update
            * params: {
                name: string or null,
                lr: float or null,
                hidden_layers: int or null,
                gamma: float or null
            }
        - bots-delete
            * params: { name: string }
        - bots-get
            * params: { name: string }

    # Training:
        - trainings-start
            * params: {
                bot_name: string,
                train_data_percentage: int,
                balance: float,
                lr: float,
                gamma: float,
                batch_size: int,
                max_episodes: int,
                min_episodes: int,
                symbol: string,
                period: string,
            }
        - trainings-pause
            * params: { id: int }
        - trainings-stop
            * params: { id: int }

        # subtasks:
            - load  | returns charts data
                * data: {
                    date_range: [],
                    closes: []
                }
            - status | returns training status
                * data:{
                    "episodes": {
                        "current": number,
                        "max": number,
                        "percentage_done": number
                    },
                    "days": {
                        "current": number,
                        "max": number,
                        "percentage_done": number
                    },
                    "max_profit": number,
                    "max_balance": number,
                    "balance": number,
                    "profit": number,
                    "trades": number,
                    "rewards": number,
                    "last_decision": number,
                    "prediction": {
                        hold: number,
                        close: number,
                        bull: number,
                        bear: number,
                        max: string
                    },
                    "bot": { 
                        "day": number, 
                        "trades": [{
                            open_at: number,
                            open_price: number,
                            open_amount: number,
                            close_at: number,
                            close_price: number,
                            close_amount: number,
                            side: number,
                            profit: number,
                            amount: number
                        }] 
                    }
                }
            - error | return error msg when something wents wrong internaly
                * data: {
                    msg: string
                }

```
            
