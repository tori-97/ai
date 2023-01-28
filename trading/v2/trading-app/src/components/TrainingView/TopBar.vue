<template>
    <div class="content-top-bar">
        <div class="options">
            <button @click="open_new_bot_modal">Create new bot</button>
            <button
                class="start-training-btn"
                @click="open_start_training_modal"
            >
                Start training
            </button>
        </div>
        <div class="live-screen">
            <div class="label">Status:</div>
            <div id="status-light" class="value"></div>
        </div>
    </div>
</template>
<script lang="ts" setup>
    import { getCurrentInstance, onMounted, ref, defineExpose } from 'vue'

    import CreateNewBotModal from '@/components/TrainingView/popups/CreateNewBotModal.vue'
    import StartTrainingModal from '@/components/TrainingView/popups/StartTrainingModal.vue'

    let new_bot_modal = ref<InstanceType<typeof CreateNewBotModal> | null>(null)
    let start_training_modal = ref<InstanceType<
        typeof StartTrainingModal
    > | null>(null)

    onMounted(() => {
        const inst = getCurrentInstance()
        const parent = inst?.root?.exposed?.training_view.value

        if (parent) {
            new_bot_modal.value = parent.create_new_bot_modal
            start_training_modal.value = parent.start_training_modal
        }

    })

    // Component Functions
    const open_new_bot_modal = () => {
        new_bot_modal.value?.open()
    }
    const open_start_training_modal = () => {

        const el = document.querySelector(".start-training-btn")

        if(!el) return false

        console.log(el.textContent)
        if ( el.textContent?.trim() === "Start training" ){
            start_training_modal.value?.open()
        }else { 
            // stop training
            console.log("stop training")
        }

    }

    type ModeType = 'running' | 'stopped' | 'pause' | 'error'

    const setStatus = (mode: ModeType) => {
        const el = document.getElementById('status-light')
        if (!el) return false
        const style = el.style
        let is_pulsing = true

        const pulse_status = (on: boolean) => {
            if (on === true) {
                el.className = 'value is-pulsing'
            } else {
                el.className = 'value'
            }
        }

        if (mode === 'running') {
            style.backgroundColor = 'green'
        } else if (mode === 'stopped') {
            style.backgroundColor = '#bebebe'
            is_pulsing = false
        } else if (mode === 'error') {
            style.backgroundColor = 'red'
        } else if (mode === 'pause') {
            style.backgroundColor = 'orange'
        }

        pulse_status(is_pulsing)
    }

    defineExpose({
        setStatus,
    })
</script>
<style lang="scss" scoped>
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.08);
        }
        100% {
            transform: scale(1);
        }
    }

    .content-top-bar {
        width: 100%;
        height: 2.8rem;
        min-height: 2.8rem;

        border-bottom: solid 1px #333;

        display: flex;
        align-items: center;
        justify-content: space-between;

        padding: 0.4rem;

        .options {
            button {
                width: 8rem;
                min-width: 8rem;
                height: 1.7rem;

                background-color: #333;
                color: #cacaca;
                box-shadow: 0px 0px 4px 0px #222;

                border: none;
                border-radius: 0.2rem;

                margin: 0.4rem;

                font-size: 0.88rem;
                font-weight: 500;

                &:focus {
                    outline: none;
                }

                &:hover {
                    background-color: #444;
                    cursor: pointer;
                }
            }
        }

        .live-screen {
            display: flex;
            align-items: center;

            .label {
                font-size: 0.88rem;
                margin: 0.5rem;
            }
            .value {
                min-width: 1rem;
                min-height: 1rem;
                width: 1rem;
                height: 1rem;

                background-color: #bebebe;
                box-shadow: 0px 0px 4px 0px #222;

                border-radius: 50%;
                margin-right: 0.5rem;
            }
        }
    }

    .is-pulsing {
        animation: pulse 1s ease-in-out infinite;
    }
</style>
