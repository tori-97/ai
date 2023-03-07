# Backend:

Available Tasks:

# Client

---

| works | name             | description |
| ----- | ---------------- | ----------- |
| [x]   | client.is.open   |
| [x]   | client.is.closed |

# Bots

| works | name                       | Parameters                        | description            |
| ----- | -------------------------- | --------------------------------- | ---------------------- |
| [x]   | bots.create                | {name: str}                       | create bot             |
| [x]   | bots.get                   | {name: str}                       | get bot byname         |
| [x]   | bots.get.all               | None                              | get all bots           |
| [x]   | bots.delete                | {name: str}                       | delete one bot by name |
| [x]   | bots.delete.all            | None                              | Delete all bot files   |
| [x]   | bots.reset                 | {name: str}                       | Reset Bot by name      |
| [x]   | bots.update.name           | {name: str, new_name: str}        | change bot's name      |
| [x]   | bots.update.learningrate   | {name: str, lr: float}            | change bot's lr        |
| [x]   | bots.update.hiddenlayers   | {name: str, hidden_layers: int}   | change bot's hl        |
| [x]   | bots.update.gamma          | {name: str, gamma: float}         | change bot's gamma     |
| [x]   | bots.update.discounterrate | {name: str, discounter_rate: int} | change bot's dr        |
| []    | bots.update.all            | {name: str, info: ''}             | change bot's info      |

# Data

| works | name                              | Parameters                                   | description                              |
| ----- | --------------------------------- | -------------------------------------------- | ---------------------------------------- |
| [x]   | data.manager.symbols              | name=GBPCHF,period=H1,maxlen=10,shuffle=true | get symbol by name                       |
| [x]   | data.manager.symbols.all          | None                                         | get all symbols names                    |
| [x]   | data.manager.symbols.update       | {name: str                                   | update symbol by name                    |
| [x]   | data.manager.symbols.available    | None                                         | get available symbols                    |
| [x]   | data.manager.symbols.all.update   | None                                         | update all symbols                       |
| [x]   | data.manager.symbols.downloadable | None                                         | get list of symbols possible to download |
| [x]   | data.manager.symbols.periods      | {name: str}                                  | get symbols available periods            |

# Trainings:

| works | name             | Parameters                                                                                                                                                                | description     |
| ----- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| []    | trainings.start  | {name: str, traindataamount: int, balance: float, lr: float, gamma: float, batch_size: int, min_episodes: int, max_episodes: int, symbol: str, period: str, threads: int} | start training  |
| []    | trainings.pause  | {id: int}                                                                                                                                                                 | pause training  |
| []    | trainings.resume | {id: int}                                                                                                                                                                 | resume training |
| []    | trainings.stop   | {id: int}                                                                                                                                                                 | stop training   |
