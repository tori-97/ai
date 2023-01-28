# app

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

=========================================================
    <!-- <link rel="icon" href="<%= BASE_URL %>favicon.ico"> -->
    <!-- <link rel="shortcut icon" href="favicon.png" type="image/x-icon" /> -->
    <!-- <title><%= htmlWebpackPlugin.options.title %></title> -->



### Aitrading
```Runs trading simulation and real trades on iqoption```

#### Application:
```Vue3js pwa app```

#### Views:

- [] Home:
	> Show last added bots
	> Show last training statistics

- [] Bots_:
	> List all available bots
	> creates new bots
	> able to edit and delete bots

 - [] Training:
	> able to create new trainings
	> shows stock graph
	> show bots threads on graphs during training
	> show threads statistics
	> annotation on click show bot env balance?
  
- [] Data_:
	> Shows symbols with those periods available
	> shows downloadable symbols
	> able to update symbols
		> shows progressbar on buttons
	> open data preview (Modal)

- [] Settings:
	> Shows default training parameters 
	> able to edit training defaults
	> able to reset all data (bots,symbols)

————————
- [] BotsViewComponents:
        •  Modal Createbot
	•  Modal EditBot
	•  Modal: DeleteBot
	•  Modal: ShowBot
	
	•  List: BotsGroup
	•  Bot

- [] TrainingViewComponents:
	•  NewTrainingModal
	•  StockGraph


## Backend:
Python websocket

