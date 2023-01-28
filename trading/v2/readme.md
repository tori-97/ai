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
- [ ] create bots view
- [ ] Custom add annotations to show all bot positions
- [ ] Adding multithreading to bot
- [ ] Add pause & stop mode to bot





# UI:
    - views:
        - Home:
            * shows currents statistics and bots
        - bots:
            * Bots Manager
        - training:
            * Training Manager
    
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


## Structure:
    websockets:
        __init__.py
        __main__.py
        configuration.py (host, port)
        lib/
            __init__.py
            client.py
            frame.py
            response.py
        tasks/
            __init__.py
            handler.py
            