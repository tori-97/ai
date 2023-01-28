<template>
    <div ref="modal" class="modal">
        <div class="modal-title">
            <div class="title">Start Training</div>
            <div class="close-btn" @click="close"><i class="fas fa-times-circle"></i></div>
        </div>
        <div class="modal-body">
            <div class="row">
                <div class="col">
                    <div class="label">Bot:</div>
                    <div class="value">
                        <select v-model="info.bot.value" @change="onChangeBotSelection">
                            <option v-for="bot in available_bots" :key="bot" :value="bot">{{ bot }}</option>
                        </select>
                    </div>
                </div>
                <div class="col">
                    <div class="label">TrainDataPercentage:</div>
                    <div class="value">
                        <input type="text" v-model="info.train_data_percentage.value" />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <div class="label">Balance:</div>
                    <div class="value">
                        <input type="text"  v-model="info.balance.value" />
                    </div>
                </div>
                <div class="col">
                    <div class="label">LearningRate:</div>
                    <div class="value">
                        <input type="text" v-model="info.lr.value" />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <div class="label">Gamma:</div>
                    <div class="value">
                        <input type="text" v-model="info.gamma.value" />
                    </div>
                </div>
                <div class="col">
                    <div class="label">BatchSize:</div>
                    <div class="value">
                        <input type="text" v-model="info.batchsize.value"/>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <div class="label">Max Episodes: </div>
                    <div class="value">
                        <input type="text" v-model="info.max_episodes.value"/>
                    </div>
                </div>
                <div class="col">
                    <div class="label">Min. Episodes: </div>
                    <div class="value">
                        <input type="text" v-model="info.min_episodes.value"/>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <div class="label">Symbol:</div>
                    <div class="value">
                        <select @change="onChangeSymbol" v-model="info.symbol.value">
                            <option v-for="bot in available_symbols" :key="bot" :value="bot">{{ bot }}</option>
                        </select>
                    </div>
                </div>
                <div class="col">
                    <div class="label">Period:</div>
                    <div class="value">
                        <select v-model="info.period.value">
                            <option v-for="bot in available_periods" :key="bot" :value="bot">{{ bot }}</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button @click="close">Cancel</button>
            <button @click="start_training">Start</button>
        </div>
    </div>
</template>
<script lang="ts" setup>
    import { ref, onMounted, defineExpose, getCurrentInstance, ComponentInternalInstance } from 'vue'
    import { RootType, PageInfoType, botType, infoType } from "@/utils/types"

    let instance: ComponentInternalInstance;
    
    const root              = ref<RootType>()
    const modal             = ref<InstanceType<typeof HTMLDivElement> | null>(null)
    const available_bots    = ref<Array<string>>([])
    const available_periods = ref<Array<string>>([])
    const available_symbols = ref<Array<string>>([])
    // const is_running        = ref(false)

    let info = {
        max_episodes: ref<number>(),
        min_episodes: ref<number>(),
        balance: ref<number>(),
        lr: ref<number>(),
        gamma: ref<number>(),
        batchsize: ref<number>(),
        bot: ref<string>(),
        train_data_percentage: ref<number>(),
        period: ref<string>(),
        symbol: ref<string>(),
    }

    onMounted(() => {
        instance = getCurrentInstance() as ComponentInternalInstance
        root.value = instance.root.exposed as RootType
    })

    const open = () => {
        if(!modal.value) return false

        root.value?.send2Server({
            query: "modal-training-load",

        })

        modal.value.style.display = "flex"
    }

    const close = () => {
        if (!modal.value) return false

        modal.value.style.display = "none"
    }

    const start_training = () => {

        const balance = info.balance.value
        const lr = info.lr.value
        const gamma = info.gamma.value
        const batch_size = info.batchsize.value
        const bot = info.bot.value
        const train_data_percentage = info.train_data_percentage.value
        const period = info.period.value
        const symbol = info.symbol.value
        const max_episodes = info.max_episodes.value
        const min_episodes = info.min_episodes.value
        
        // Guard:
        if ( !balance || !lr || !gamma || !batch_size  || !bot || !train_data_percentage || !period || !symbol || !max_episodes || !min_episodes) return false

        

        root.value?.send2Server({
            query: "training-start",
            config: {
                balance: parseFloat(balance.toLocaleString()), 
                learning_rate: parseFloat(lr.toLocaleString()),
                gamma: parseFloat(gamma.toLocaleString()),
                batch_size: parseInt(batch_size.toLocaleString()),
                bot: bot,
                train_data_percentage: parseFloat((train_data_percentage / 100).toLocaleString()),
                period: period,
                symbol: symbol,
                max_episodes: parseInt(max_episodes.toLocaleString()),
                min_episodes: parseInt(min_episodes.toLocaleString())
            }
        })

        
        close()

        const page_info = window.localStorage.getItem("page-info") as string 
        const pinfo = JSON.parse(page_info) as PageInfoType

        pinfo.training.symbol = symbol
        pinfo.training.period = period


        const el = document.querySelector(".start-training-btn")

        if(!el) return false
        el.textContent = "Stop training"


    }

    const onChangeBotSelection = () => {
        const bot_name = info.bot.value
        if(!bot_name) return false

        root.value?.send2Server({
            query: "bot-get-config",
            name: bot_name
        })
    }

    const onChangeSymbol = () => {
        root.value?.send2Server({
            query: "training-datasets-periods",
            symbol: info.symbol.value
        })
    }

    const update_modal = (info: infoType) => {
        const bots = info.bots
        available_bots.value = bots
        const symbols = Object.keys(info.symbols)
        available_symbols.value = symbols
    }
  
    const updateBotDefaultInformation = (_info: botType) => {
        info.max_episodes.value = _info.defaults.training.max_episodes
        info.balance.value = _info.defaults.training.balance
        info.lr.value = _info.info.lr
        info.gamma.value = _info.info.gamma
        info.batchsize.value = _info.defaults.training.batch_size
        info.train_data_percentage.value = _info.defaults.training.train_data_percentage
        info.period.value = _info.defaults.training.period
        info.min_episodes.value = _info.defaults.training.min_episodes
    }

    const updatePeriods = (periods: Array<string>) => {
        available_periods.value = periods
    }

    defineExpose({
        open,
        close,
        update_modal,
        updateBotDefaultInformation,
        updatePeriods
    })
</script>
<style lang="scss" scoped>
    .modal {
        width: 32rem;

        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);

        display: none;
        flex-direction: column;
        align-items: center;

        background-color: #444;
        box-shadow: 0px 0px 4px 0px #222;

        border-radius: 0.4rem;

        overflow: hidden;

        .modal-title {
            width: 100%;
            height: 2rem;
            min-height: 2.6rem;

            background-color: #333;

            display: flex;
            align-items: center;
            justify-content: space-between;

            padding: 0 0.8rem;

            .close-btn {
                color: #bebebe;

                &:hover {
                    color: #222;
                    cursor: pointer;
                }
            }
        }

        .modal-body {
            width: 100%;
            height: 100%;

            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;

            padding: 0.4rem;

            .row {
                width: 100%;
                display: flex;
                align-items: center;
                align-content: center;

                padding: 0.4rem;


                .col {
                    width: 100%;
                    height: 2.3rem;

                    display: flex;
                    align-items: center;
                    justify-content: center;

                    .label {
                        width: 100%;
                    }
                    .value {
                        width: 100%;

                        input, select {
                            width: 100%;
                            min-height: 2rem;
                            height: 2rem;

                            border: none;
                            border-radius: 0.2rem;

                            background-color: #222;
                            color: #cacaca;
                            box-shadow: 0px 0px 4px 0px #333;

                            padding: 0.4rem;

                            &:focus {
                                outline: none;
                            }
                        }
                        select { 
                            min-height: 2rem;
                        }

                        margin: 0.8rem;
                    }
                }
            }
        }

        .modal-footer {
            width: 100%;
            height: 2rem;
            min-height: 3rem;

            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: .5rem;

            padding: 0.55rem;



            button {
                border: none;
                border-radius: 0.2rem;

                font-size: 0.88rem;

                background-color: #222;
                color: #cacaca;

                width: 6rem;
                height: 2rem;

                &:focus {
                    outline: none;
                }

                &:hover {
                    background-color: #111;
                    cursor: pointer;
                }

                &:nth-child(1){
                    background-color: #333;

                    &:hover {
                        background-color: #222;
                    }
                }
            }
        }
    }
</style>
