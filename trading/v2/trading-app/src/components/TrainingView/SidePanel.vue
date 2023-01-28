<template>
    <div class="side-panel">

        <div class="section">
            <div class="section-title">Training Information</div>
            <div class="section-body">
                <ul id="trading-information-list">
                    <li>
                        <div class="label">Episodes:</div>
                        <div class="value">{{ episodes }}</div>
                    </li>
                    <li>
                        <div class="label">Days:</div>
                        <div class="value">{{ days }}</div>
                    </li>
                    <li>
                        <div class="label">MaxProfit:</div>
                        <div class="value">{{ max_profit }}</div>
                    </li>
                    <li>
                        <div class="label">MaxBalance:</div>
                        <div class="value">{{ max_balance }}</div>
                    </li>
                    <li>
                        <div class="label">Balance:</div>
                        <div class="value">{{ balance }}</div>
                    </li>
                    <li>
                        <div class="label">Profit:</div>
                        <div class="value">{{ profit }}</div>
                    </li>
                    <li>
                        <div class="label">Trades</div>
                        <div class="value">{{ trades }}</div>
                    </li>
                    <li>
                        <div class="label">Rewards:</div>
                        <div class="value">{{ rewards }}</div>
                    </li>
                    <li>
                        <div class="label">LastDecisionBy:</div>
                        <div class="value">{{ last_decision_made_by }}</div>
                    </li>
                </ul>
            </div>
        </div>

        <div class="section">
            <div class="section-title">Predictions</div>
            <div class="section-body" id="training-predictions">
                <div class="row">
                    <div class="col">
                        <div class="label">Hold:</div>
                        <div class="value">{{ predictions.hold.value }} %</div>
                    </div>
                    <div class="col">
                        <div class="label">Close:</div>
                        <div class="value">{{ predictions.sell.value }} %</div>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <div class="label">Bull:</div>
                        <div class="value">{{ predictions.bull.value }} %</div>
                    </div>
                    <div class="col">
                        <div class="label">Bear:</div>
                        <div class="value">{{ predictions.bear.value }} %</div>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <div class="label">MaxPrediction:</div>
                        <div class="value">{{ predictions.max.value }}</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">
                Trades
            </div>
            <div class="section-body" id="training-trades">
                <!-- amount: 7500
                close_amount: 9876.75
                close_at: "2007-01-03 00:00"
                close_price: 1.3169
                open_amount: 9954.3
                open_at: "2007-01-02 00:00"
                open_price: 1.32724
                profit: -77.54999999999927
                side: "BULL" -->

                
                    <div v-if="positions.length > 0" class="position-bg">
                        
                        <div class="position" v-for="position in positions" :key="position.side">
                            <div class="row">
                                <div class="col">
                                    <div class="label">Open at: [{{ position.open_at }}]</div>
                                    <div class="sep">|</div>
                                    <div class="label">Open price: [{{ position.open_price }}]</div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <div class="label">Close at: [{{ position.close_at }}]</div>
                                    <div class="sep">|</div>
                                    <div class="label">Close price: [{{ position.close_price }}]</div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <div class="label">Amount: [{{ parseFloat(position.amount.toLocaleString()) }}]</div>
                                    <div class="sep">|</div>
                                    <div class="label">Profit: [{{ position.profit }}]</div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <div class="label">side: {{ position.side }}</div>
                                </div>
                            </div>
                        </div>
                        
                    </div>
                    <div v-else class="position-empty">
                        No Positions closed yet !!
                    </div>

            </div>
        </div>
        
    </div>
</template>
<script lang="ts" setup>

    import { ref, defineExpose } from "vue"
    import { InformationType, PredictionsType, PositionsType } from "@/utils/types";

    const episodes = ref("")
    const days = ref("")
    const max_profit = ref()
    const max_balance = ref()
    const balance = ref()
    const profit = ref()
    const trades = ref()
    const rewards = ref()
    const last_decision_made_by = ref("")

    const predictions = {
        hold: ref(),
        sell: ref(),
        bull: ref(),
        bear: ref(),
        max: ref()
    }

    const positions = ref<Array<PositionsType>>([])

    const setInformation = (result: InformationType) => {
        episodes.value = `${result.episodes.current}/${result.episodes.max} ${result.episodes.percentage_done} %`
        days.value = `${result.days.current}/${result.days.max} ${result.days.percentage_done} %`
        max_profit.value = result.max_profit
        max_balance.value = result.max_balance
        balance.value = result.balance
        profit.value = result.profit
        trades.value = result.trades
        rewards.value = result.rewards
        last_decision_made_by.value = result.last_decision

        positions.value = result.bot.trades
    }

    const setPredictions = (prediction: PredictionsType) => {
        predictions.hold.value = prediction.hold
        predictions.sell.value = prediction.sell
        predictions.bull.value = prediction.bull
        predictions.bear.value = prediction.bear
        predictions.max.value  = prediction.max
    }

    defineExpose({
        setInformation,
        setPredictions
    })

</script>
<style lang="scss" scoped>
    .side-panel {
        width: 18rem;
        min-width: 18rem;
        height: 100%;

        background-color: #333;
        box-shadow: 0px 0px 4px 0px #222;

        display: flex;
        flex-direction: column;
        align-items: center;

    }

    .section {
        width: 100%;

        display: flex;
        flex-direction: column;
        align-items: center;

        .section-title {
            width: 100%;
            height: 2.2rem;
            min-height: 2.2rem;

            display: flex;
            align-items: center;

            padding: 0.4rem;

            font-size: 0.88rem;
            font-weight: 500;

            background-color: #444;
            color: #000;
        }

        .section-body {
            width: 100%;

            display: flex;
            flex-direction: column;
            align-items: center;
        }
    }

    #trading-information-list {
        width: 100%;
        list-style: none;

        display: flex;
        flex-direction: column;
        align-items: center;

        padding: 0.3rem;

        li {
            width: 100%;
            height: 1.6rem;

            display: flex;
            align-items: center;
            justify-content: space-between;

            padding: 0 0.45rem;
            margin: 0.1rem;

            .label,
            .value {
                width: 100%;
                height: 100%;

                display: flex;
                align-items: center;

                font-size: 0.99rem;
            }
            .value {
                justify-content: center;
                background-color: #222;

                border-radius: 0.2rem;

                font-size: 0.88rem;

                overflow: hidden;
            }
        }
    }
    #training-predictions {
        display: flex;
        flex-direction: column;
        align-items: center;

        padding: .4rem;

        .row {
            width: 100%;

            display: flex;
            align-items: center;


            .col {
                display: flex;
                align-items: center;
                justify-content: center;

                width: 100%;

                padding: .3rem;

                .label { 
                    width: 80%;
                }
                .label,
                .value {
                    display: flex;
                    align-items: center;
                    font-size: 0.99rem;
                }
                .value {
                    width: 100%;
                    max-width: 5rem;
                    min-width: 5rem;

                    justify-content: center;
                    background-color: #222;

                    border-radius: 0.2rem;
                    font-size: 0.88rem;
                    overflow: hidden;

                    white-space: nowrap;

                    padding: .35rem .6rem;
                }
            }

            &:nth-child(3){
                .label { 
                    margin-right: .5rem;
                }
                .value { 
                    max-width: 10rem;
                }
            }
        }
    }

    #training-trades {
        width: 100%;
        max-height: 25rem;

        overflow: hidden;
        overflow-y: auto;

        scrollbar-width: thin;
        scrollbar-color: #444 #333;
        
        .position { 
            width: 100%;
            background-color: #777;
            border-top: solid .1rem #666;
            border-bottom: solid .1rem #666;

            padding: .2rem;
            margin: .2rem;

            display: flex;
            flex-direction: column;
            align-items: center;
            
            .row { 
                width: 100%;
                display: flex;
                align-items: center;

                background-color: #222;
                padding: .3rem;
                

                .col { 
                    width: 100%;
                    height: 1.4rem;

                    display: flex;
                    align-items: center;
                    justify-content: center;

                    padding: .4rem;
                    
                    .label { 
                        width: 100%;
                        white-space: nowrap;

                        font-size: .66rem;
                        text-transform: capitalize;
                    }

                    .sep { 
                        margin: .2rem;
                    }
                }
            }
        }

        .position-empty { 
            font-size: .88rem;
            margin: .5rem;
        }
    }
</style>
