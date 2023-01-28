<template>
    <div ref="modal" class="modal">
        <div class="modal-title">
            <div class="brand">Create new bot</div>
            <div @click="close" class="close-btn">
                <i class="fas fa-times-circle"></i>
            </div>
        </div>
        <div class="modal-body">
            <div class="row">
                <div class="col">
                    <div class="label">Name:</div>
                    <div class="value">
                        <input
                            type="text"
                            v-model="name"
                            placeholder="Gaspar"
                        />
                    </div>
                </div>
                <div class="col">
                    <div class="label">LearningRate:</div>
                    <div class="value">
                        <input
                            type="text"
                            v-model="learning_rate"
                            placeholder="0.0025"
                        />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <div class="label">Gamma:</div>
                    <div class="value">
                        <input
                            type="text"
                            v-model="gamma"
                            placeholder="0.998"
                        />
                    </div>
                </div>
                <div class="col">
                    <div class="label">HiddenLayers:</div>
                    <div class="value">
                        <input
                            type="text"
                            v-model="hidden_layers"
                            placeholder="43"
                        />
                    </div>
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button @click="close">Cancel</button>
            <button @click="create_new_bot">Create</button>
        </div>
    </div>
</template>
<script lang="ts" setup>
    import {
        ref,
        onMounted,
        defineExpose,
        getCurrentInstance,
        ComponentInternalInstance,
    } from 'vue'

    import { RootType } from '@/utils/types'

    let instance: ComponentInternalInstance

    const root = ref<RootType>()
    const modal = ref<InstanceType<typeof HTMLDivElement> | null>(null)
    const name = ref<InstanceType<typeof String> | null>(null)
    const learning_rate = ref<InstanceType<typeof Number> | null>(null)
    const gamma = ref<InstanceType<typeof Number> | null>(null)
    const hidden_layers = ref<InstanceType<typeof Number> | null>(null)

    onMounted(() => {
        instance = getCurrentInstance() as ComponentInternalInstance
        root.value = instance.root.exposed as RootType
    })

    const open = () => {
        if (!modal.value) return false
        modal.value.style.display = 'flex'
    }
    const close = () => {
        if (!modal.value) return false
        modal.value.style.display = 'none'
    }

    const create_new_bot = () => {
        root.value?.send2Server({
            query: 'bot-create',
            data: {
                name: name.value,
                lr: learning_rate.value,
                gamma: gamma.value,
                hidden_layers: hidden_layers.value,
            },
        })
        console.log("[+] Creating new bot...")
    }

    defineExpose({
        open,
        close,
    })
</script>
<style lang="scss" scoped>
    .modal {
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
            min-height: 2.4rem;

            background-color: #333;

            display: flex;
            align-items: center;
            justify-content: space-between;

            padding: 0.8rem;

            .brand {
                font-size: 0.99rem;
                font-weight: 500;
            }
            .close-btn {
                color: #666;
                i {
                    font-size: 1.22rem;
                }

                &:hover {
                    color: #555;
                    cursor: pointer;
                }
            }
        }

        .modal-body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;

            .row {
                display: flex;
                align-items: center;
                align-content: center;

                padding: 0.4rem;

                .col {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    align-content: center;

                    padding: 0.4rem;

                    &:nth-child(odd) {
                        .label {
                            min-width: 4rem;
                            max-width: 4rem;
                        }
                    }

                    .label {
                        min-width: 8rem;
                        max-width: 8rem;
                        height: 2rem;

                        display: flex;
                        align-items: center;
                        justify-content: flex-start;

                        font-size: 0.99rem;
                    }
                    .value {
                        display: flex;
                        align-items: center;
                        justify-content: center;

                        input {
                            max-width: 8rem;

                            border: none;
                            border-radius: 0.2rem;

                            background-color: #222;
                            color: #cacaca;
                            box-shadow: 0px 0px 4px 0px #333;

                            padding: 0.4rem;
                            margin-left: 0.4rem;

                            font-size: 0.88rem;

                            &:focus {
                                outline: none;
                            }
                        }
                    }
                }
            }
        }

        .modal-footer {
            width: 100%;

            display: flex;
            align-items: center;
            justify-content: flex-end;

            padding: 0 0.8rem;

            button {
                border: none;
                border-radius: 0.2rem;

                font-size: 0.88rem;

                background-color: #222;
                color: #cacaca;

                width: 6rem;
                height: 2rem;

                margin: 0.5rem;

                &:nth-child(1) {
                    background-color: #666;
                    color: #222;

                    &:hover {
                        color: #bebebe;
                    }
                }

                &:focus {
                    outline: none;
                }

                &:hover {
                    background-color: #333;
                    cursor: pointer;
                }
            }
        }
    }
</style>
