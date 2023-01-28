<template>
    <div ref="sidebar" class="sidebar">
        <div class="sidebar-group">
            <div
                class="sidebar-group-row"
                v-for="item in Object.keys(configuration)"
                :key="item"
            >
                <div class="label">
                    {{
                        item
                            .replaceAll('_', ' ')
                            .charAt(0)
                            .toLocaleUpperCase() +
                        item.replaceAll('_', ' ').slice(1)
                    }}
                </div>
                <div class="value">
                    {{ configuration[item as keyof typeof configuration] }}
                </div>
            </div>
        </div>
        <div class="threads">
            <div class="title">Threads:</div>
            <div class="content">
                <div class="thread" v-for="thread in threads" :key="thread.id">
                    <div class="thread-info">
                        <div class="label">Name</div>
                        <div class="value">{{ thread.id }}</div>
                    </div>

                    <div class="thread-info">
                        <div class="label">Episode</div>
                        <div class="value">{{ thread.episode }}</div>
                    </div>

                    <div class="thread-info">
                        <div class="label">Day</div>
                        <div class="value">{{ thread.day }}</div>
                    </div>

                    <div class="thread-info">
                        <div class="label">Balance</div>
                        <div class="value">{{ thread.balance }}</div>
                    </div>
                    <div class="thread-info">
                        <div class="label">DecisionBy</div>
                        <div class="value">{{ thread.decision_made_by }}</div>
                    </div>
                    <div class="thread-info">
                        <div class="label">Rewards</div>
                        <div class="value">{{ thread.rewards }}</div>
                    </div>
                    <div class="thread-info">
                        <div class="label">Info</div>
                        <div class="value">{{ thread.info }}</div>
                    </div>
                    <div class="preds">
                        <div class="label">Predictions</div>
                        <div class="value">
                            <div class="row">
                                <div class="col">
                                    Hold: {{ thread.predictions?.hold }} %
                                </div>
                                <div class="col">
                                    Close: {{ thread.predictions?.sell }} %
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    Bull:{{ thread.predictions?.bull }} %
                                </div>
                                <div class="col">
                                    Bear:{{ thread.predictions?.bear }} %
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">Max: {{ thread.predictions?.max }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
    import { ref, defineExpose, Ref } from 'vue'

    const sidebar = ref()

    const configuration = ref({
        max_episodes: ref<number>(0),
        threads_alive: ref<number>(0),
    })

    interface Thread {
        id: string
        episode: number
        day: number
        balance: number
        predictions: {
            hold: number
            sell: number
            bull: number
            bear: number
            max: string
        }
        decision_made_by: string
        rewards: number
        info: string
    }

    const threads = ref<Array<Thread>>([])

    const configureThreads = (_threads: any) => {
        for (let t in _threads) {
            threads.value.push({
                id: _threads[t],
                episode: 0,
                day: 0,
                balance: 0,
            })
        }
    }

    const updateThread = (config: Thread) => {
        let index = -1
        let i = 0
        for (; i < threads.value.length; i++) {
            if (threads.value[i].id == config.id) {
                index = i
            }
        }
        threads.value[index] = config

        threads.value.sort((a, b) => b.balance - a.balance)
    }

    const deleteThread = (config: Thread) => {
        let index = -1
        let i = 0
        for (; i < threads.value.length; i++) {
            if (threads.value[i].id == config.id) {
                index = i
            }
        }
        threads.value.splice(index, 1)
    }

    const setWidth = (val: string) => {
        sidebar.value.style.width = val
    }

    defineExpose({
        configuration,
        threads,
        updateThread,
        configureThreads,
        deleteThread,
        setWidth
    })
</script>
<style lang="scss" scoped>
    .sidebar {
        width: 0;
        height: 100%;

        background-color: #222;
        color: #cacaca;

        overflow: hidden;

        transition-duration: 280ms;

        .sidebar-group {
            display: flex;
            flex-direction: column;
            align-items: center;

            .sidebar-group-row {
                width: 100%;
                height: 2.4rem;

                display: flex;
                align-items: center;

                padding: 0.4rem;

                .label {
                    width: 100%;
                    white-space: nowrap;

                    font-size: 0.88rem;
                }
                .value {
                    width: 100%;
                    height: 100%;

                    display: flex;
                    align-items: center;
                    justify-content: center;

                    background-color: #333;

                    border-radius: 0.4rem;

                    padding: 0.32rem;
                }
            }
        }

        .threads {
            display: flex;
            flex-direction: column;
            align-items: center;

            overflow: hidden;

            .title {
                width: 100%;
                height: 2.2rem;

                display: flex;
                align-items: center;

                padding: 0.4rem;
            }

            .content {
                width: 100%;
                min-height: 20rem;
                height: 35rem;

                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.6rem;

                padding: 0.4rem;

                overflow: hidden;
                overflow-y: auto;

                .thread {
                    width: 100%;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 0.25rem;

                    padding: 0.4rem;

                    background-color: #444;

                    .thread-info {
                        width: 100%;
                        height: 2.2rem;

                        display: flex;
                        align-items: center;

                        border-radius: 0.2rem;
                        background-color: #333;
                        padding: 0.4rem;

                        .label {
                            width: 100%;
                            font-size: 0.88rem;
                        }
                        .value {
                            font-size: 0.88rem;
                            width: 100%;

                            display: flex;
                            flex-direction: column;

                            align-items: center;
                            justify-content: center;

                            white-space: nowrap;
                        }
                    }
                    .preds {
                        width: 100%;

                        display: flex;
                        flex-direction: column;
                        align-items: center;

                        .label {
                            width: 100%;
                            height: 2.2rem;

                            display: flex;
                            align-items: center;
                        }

                        .value {
                            width: 100%;
    
                            display: flex;
                            flex-direction: column;
                            align-items: center;

                            gap: .3rem;

                            .row {
                                width: 100%;
    
                                display: flex;
                                align-items: center;
                                gap: .2rem;

                                background-color: #222;

                                .col {
                                    width: 100%;
                                    height: 2.2rem;

                                    white-space: nowrap;

                                    display: flex;
                                    align-items: center;
                                    justify-content: center;

                                    padding: .4rem;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
</style>
