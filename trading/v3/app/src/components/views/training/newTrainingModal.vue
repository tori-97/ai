<!-- @format -->

<template>
    <def-modal ref="modalComp">
        <template #header>
            <div class="title">New training</div>
            <div @click="modalComp?.close" class="close-btn">
                <i class="fas fa-times-circle"></i>
            </div>
        </template>

        <div class="form">
            <div
                class="form-group"
                v-for="key in Object.keys(configuration)"
                :key="key">
                <div class="label">
                    {{
                        key.replaceAll('_', ' ').charAt(0).toLocaleUpperCase() +
                        key.replaceAll('_', ' ').slice(1)
                    }}
                </div>
                <div class="value">
                    <select
                        @change="bot_on_change"
                        v-if="key === 'name'"
                        v-model="configuration.name">
                        <option
                            v-for="bot in available.bots"
                            :key="bot.name"
                            :value="bot.name">
                            {{ bot.name }}
                        </option>
                    </select>
                    <select
                        @change="symbol_on_change"
                        v-else-if="key === 'symbol'"
                        v-model="configuration.symbol">
                        <option
                            v-for="symbol in available.symbols"
                            :key="symbol"
                            :value="symbol">
                            {{ symbol }}
                        </option>
                    </select>
                    <select
                        v-else-if="key === 'period'"
                        v-model="configuration.period">
                        <option
                            v-for="period in available.period"
                            :key="period"
                            :value="period">
                            {{ period }}
                        </option>
                    </select>
                    <select
                        v-else-if="key === 'train_data_amount'"
                        v-model="configuration.train_data_amount">
                        <option
                            v-for="train_data_amount in available.train_data_amount"
                            :key="train_data_amount"
                            :value="train_data_amount">
                            {{ train_data_amount }}%
                        </option>
                    </select>
                    <input
                        v-else-if="
                            key === 'min_threads' ||
                            key === 'min_episodes' ||
                            key === 'max_episodes'
                        "
                        type="number"
                        v-model="configuration[key]" />
                    <def-btn-slide
                        v-else-if="
                            key === 'shuffled' || key === 'run_forever'
                        "></def-btn-slide>
                    <input v-else type="text" v-model="configuration[key as keyof ConfigurationType]" />
                </div>
            </div>
        </div>

        <template #footer>
            <div class="btn-group">
                <def-btn @click="modalComp?.close" class="btn">Cancel</def-btn>
                <def-btn @click="new_training" class="btn">Create</def-btn>
            </div>
        </template>
    </def-modal>
</template>
<script lang="ts" setup>
    import Modal from '@/components/defaults/defModal.vue'
    import { defineExpose, onMounted, ref, getCurrentInstance, Ref } from 'vue'
    import App from '@/manager'

    const modalComp = ref<InstanceType<typeof Modal>>()

    interface ConfigurationType {
        name: Ref<string>
        symbol: Ref<string>
        period: Ref<string>
        train_data_amount: Ref<number>
        shuffled: Ref<boolean>
        min_threads: Ref<number>
        run_forever: Ref<boolean>
        balance: Ref<number>
        min_balance: Ref<number>
        lr: Ref<number>
        gamma: Ref<number>
        discounter_rate: Ref<number>
        batch_size: Ref<number>
        min_episodes: Ref<number>
        max_episodes: Ref<number>
        train_speed: Ref<number>
    }

    const configuration = ref<ConfigurationType>({
        name: ref<string>(''),
        balance: ref<number>(1000),
        min_balance: ref<number>(500),
        lr: ref<number>(0.0025),
        gamma: ref<number>(0.989),
        discounter_rate: ref<number>(20),
        batch_size: ref<number>(100),
        min_episodes: ref<number>(1),
        max_episodes: ref<number>(3),
        symbol: ref<string>('EURUSD'),
        period: ref<string>('D1'),
        train_data_amount: ref<number>(4),
        min_threads: ref<number>(3),
        train_speed: ref<number>(1),
        shuffled: ref<boolean>(false),
        run_forever: ref<boolean>(false),
    })

    const available = ref({
        bots: ref<Array<ConfigurationType>>([]),
        symbols: ref<Array<string>>([]),
        period: ref<Array<string>>(['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1']),
        train_data_amount: ref<Array<string>>([
            '1',
            '2',
            '3',
            '4',
            '5',
            '10',
            '20',
            '30',
            '40',
            '50',
            '60',
            '70',
            '80',
            '90',
            '100',
        ])
    })

    const app = getCurrentInstance()?.root.exposed?.app as App

    onMounted(() => {
        app.comunicate('training', 'bots.get.all', null)
        app.comunicate('training', 'data.manager.symbols.all', null)
    })

    const updateAvailableBots = (bots: Array<ConfigurationType>) => {
        available.value.bots = bots as any
    }
    const updateAvailableSymbols = (symbols: Array<string>) => {
        available.value.symbols = symbols
    }
    const updateAvailablePeriods = (periods: Array<string>) => {
        available.value.period = periods
    }

    const bot_on_change = () => {
        // Call bot configuration
        app.comunicate('training', 'bots.get', {
            name: configuration.value.name,
        })
    }
    const symbol_on_change = () => {
        // call symbol periods
        app.comunicate('training', 'data.manager.symbols.periods', {
            name: configuration.value.symbol
        })
    }

    const new_training = () => {
        // creates new training

        const tmp = {}
        Object.assign(tmp, configuration.value)
        app.comunicate('training', 'trainings.start', tmp)
        window.localStorage.setItem("train-info", JSON.stringify(tmp))
        modalComp.value?.close()
    }

    const update_configuration = (_configuration: {name: string, lr: number, gamma: number, discounter_rate: number}) => {
        // update bot configuration
        configuration.value.name = _configuration.name
        configuration.value.lr = _configuration.lr
        configuration.value.gamma = _configuration.gamma
        configuration.value.discounter_rate = _configuration.discounter_rate
    }

    defineExpose({
        modalComp,
        updateAvailableBots,
        updateAvailablePeriods,
        updateAvailableSymbols,
        update_configuration,
        configuration
    })
</script>
<style lang="scss" scoped>
    .title {
        &::selection {
            background-color: transparent;
        }
        cursor: default;
    }

    .close-btn {
        cursor: pointer;
    }

    .form {
        width: 32rem;

        padding: 0.6rem;

        display: flex;
        flex-direction: column;
        align-items: center;

        gap: 0.35rem;

        .form-group {
            width: 100%;

            display: flex;
            align-items: center;
            justify-content: center;

            .label {
                width: 100%;
                height: 2rem;

                display: flex;
                align-items: center;

                &::selection {
                    background-color: transparent;
                }

                cursor: default;
            }

            .value {
                width: 100%;

                display: flex;
                align-items: center;
                justify-content: flex-end;

                input,
                select {
                    border: none;
                    border-radius: 0.35rem;
                    width: 100%;
                    height: 2.2rem;

                    padding: 0.4rem;

                    background-color: #222;
                    color: #bebebe;
                }
            }
        }
    }

    .btn-group {
        display: flex;
        align-items: center;
        gap: 0.4rem;

        .btn {
            min-width: 6rem;
            background-color: #222;

            &:hover {
                color: #222;
            }

            &:nth-child(1) {
                background-color: #444;

                &:hover {
                    background-color: #222;
                    color: #bebebe;
                }
            }
        }
    }
</style>
