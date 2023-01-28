interface WebSocketResultType {
    name: string
    done: boolean
    msg: string
    is_client_msg: boolean
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    body: Array | object
}

// SidePanel types

interface PositionsType {
    side: string
    open_at: string
    open_price: number
    close_at: string
    close_price: number
    amount: number
    profit: number
}

interface InformationType {
    episodes: {
        current: number
        max: number
        percentage_done: number
    }
    days: {
        current: number
        max: number
        percentage_done: number
    }
    max_profit: number
    max_balance: number
    balance: number
    profit: number
    trades: number
    rewards: number
    last_decision: string
    bot: {
        day: number
        trades: Array<PositionsType>
    }
}

interface PredictionsType {
    hold: number
    sell: number
    bull: number
    bear: number
    max: string
}

interface infoType {
    bots: Array<string>
    symbols: Array<Array<string>>
}

interface botType {
    info: {
        name: string
        lr: number
        gamma: number
        hidden_layers: number
    }
    defaults: {
        training: {
            balance: number
            batch_size: number
            train_data_percentage: number
            max_episodes: number
            period: string
            symbol: string
            min_episodes: number
        }
    }
    counter: {
        amount_trades: number
        amount_trainings: number
        amount_episodes: number
    }
    records: {
        max_episodes: number
        max_balance: number
        max_profit: number
    }
}

interface TrainingViewType {
    create_new_modal: {
        value: {
            open: () => void
            close: () => void
        }
    }
    start_training_modal: {
        value: {
            open: () => void
            close: () => void
            update_modal: (info: infoType) => void
            updateBotDefaultInformation: (info: botType) => void
            updatePeriods: (periods: Array<string>) => void
        }
    }
    graph: {}
    side_panel: {}
    topbar: {}
}

interface RootType {
    current_view: string
    training_view: null,
    send2Server: (data: object) => void
    sendConfirmation: () => void
    is_loading: boolean
}

interface PageInfoType {
    current_view: string
    training: {
        symbol: string
        period: string
        times: Array<string>
        closes: Array<number>
    }
}

export {
    RootType,
    TrainingViewType,
    PageInfoType,
    WebSocketResultType,
    InformationType,
    PredictionsType,
    PositionsType,
    botType,
    infoType,
}
