<template>
    <navbar />

    <Home ref="home_view" v-if="current_view == 'home'" />
    <Training ref="training_view" v-else-if="current_view == 'training'" />
    <Bots ref="bots_view" v-else-if="current_view == 'bots'" /> 

    <loader v-if="is_loading" :msg="loading_msg" />
    <ClientMessageModal ref="client_message" />
</template>

<script lang="ts" setup>
    import Home from '@/views/HomeView.vue'
    import Training from '@/views/TrainingView.vue'
    import Bots from '@/views/BotsView.vue'

    import Navbar from "@/components/AppNavbar.vue"
    import Loader from "@/components/AppLoader.vue"

    import ClientMessageModal from "@/components/AppClientMessage.vue"

    import { defineExpose, onMounted, ref } from 'vue'
    import { WebSocketResultType, PageInfoType } from './utils/types'

    const web_socket_url = 'ws://localhost:9001/trading'
    const is_prod_mode = true
    let is_loading = ref(is_prod_mode) // set to true after development

    let loading_msg = ref('Welcome to ai trading')
    const current_view = ref('home')

    let client_message = ref<InstanceType<typeof ClientMessageModal> | null>(null)
    let home_view = ref<InstanceType<typeof Home> | null>(null)
    let training_view = ref<InstanceType<typeof Training> | null>(null)
    let bots_view = ref<InstanceType<typeof Bots> | null>(null)

    let ws = new WebSocket(web_socket_url)

    ws.addEventListener('open', () => {
        console.log('[+] Websocket is opened...')
        send2Server({ query: 'client-is-open' })
    })

    ws.addEventListener('close', () => {
        console.log('[+] Websocket is closed...')
        send2Server({ query: 'client-is-closed' })
    })

    ws.addEventListener('error', () => {
        console.log('[!] Websocket has an error')
        training_view.value?.topbar?.setStatus("error")
    })

    ws.addEventListener('message', async (ev) => {
        console.log('[+] Websocket sends new message !!')

        let task = null as WebSocketResultType | null
        let is_json = false

        if (typeof ev.data === 'string') {
            try {
                task = JSON.parse(ev.data) as WebSocketResultType
                is_json = true
            } catch (e) {
                console.error('[!] data could not be parsed...')
            }
        }

        if (!is_json || !task) return false
        
        const page_info = window.localStorage.getItem("page-info") as string 
        const pinfo = JSON.parse(page_info) as PageInfoType

        // TrainingView Tasks
        if (task.name === "bot-create"){
            if ( task.done )  training_view.value?.create_new_bot_modal?.close()

        }else if ( task.name === "modal-training-load" ){
            training_view.value?.start_training_modal?.update_modal(task.body)

        }else if ( task.name === "bot-get-config" ){
            training_view.value?.start_training_modal?.updateBotDefaultInformation(task.body)

        }else if ( task.name === 'training-start' ){
            training_view.value?.topbar?.setStatus("running")


            if ( task.msg === "load-data" ){
                training_view.value?.graph?.updateChart(
                    task.body.symbol,
                    task.body.time,
                    task.body.closes
                )

                if ( pinfo.training.times.length === 0 && pinfo.training.period !== task.body.period && pinfo.training.symbol !== task.body.symbol ){
                    pinfo.training.times = task.body.time
                    pinfo.training.closes = task.body.closes
                    pinfo.training.symbol = task.body.symbol
                    pinfo.training.period = task.body.period
                }else { 
                    training_view.value?.graph?.resetBotPosition()
                }

                window.localStorage.setItem("page-info", JSON.stringify(pinfo))

            }else if ( task.msg === "update" ){
                
                training_view.value?.graph?.moveBot(task.body.bot.day)
                training_view.value?.side_panel?.setInformation(task.body)
                training_view.value?.side_panel?.setPredictions(task.body.prediction)
            }else if ( task.msg === "reset-episode" ){
                training_view.value?.graph?.resetBotPosition()
            }else if ( task.msg === "end" ){
                training_view.value?.topbar?.setStatus("stopped")
            }else if ( task.msg === "pause" ){
                training_view.value?.topbar?.setStatus("pause")
            }
        }else if ( task.name === 'training-datasets-periods'){
            training_view.value?.start_training_modal?.updatePeriods(task.body)
        }

        if ( task.is_client_msg ){
            client_message.value?.showMessage("Information", task.msg)
        }

        sendConfirmation() 
    })
    onMounted(() => {
        let save_page_info = window.localStorage.getItem("page-info") as string

        if ( !save_page_info ){
            window.localStorage.setItem("page-info", JSON.stringify({
                current_view: current_view.value,
                training: {
                    symbol: "",
                    times: [],
                    closes: [],
                    period: ""
                }
            }))
        }

        const page_info = JSON.parse(save_page_info) as PageInfoType

        if(page_info){
            current_view.value = page_info.current_view
        }
        
        setLoadingMessage(
            'Connection to server will be established now...',
            2000,
            is_prod_mode, // change to true after develop
        )
        // if (ws.is_connected) {
        //     setLoadingMessage('Connection is established...', 3000, true)
        // }
        setLoadingMessage(
            'Application is making last preparations...',
            4000,
            false,
        )
    })

    const setLoadingMessage = (
        message: string,
        time: number,
        loading: boolean,
    ) => {
        setTimeout(() => {
            loading_msg.value = message
            setTimeout(() => {
                is_loading.value = loading
            }, time + 1000)
        }, time)
    }

    const send2Server = (data: string | object) => {
        if (typeof data === 'object') {
            data = JSON.stringify(data)
        }
        ws.send(data)
    }

    const sendConfirmation = () => {
        send2Server({
            task: 'confirm-query',
            done: true,
            msg: 'message successfully arrived',
        })
    }

    defineExpose({
        current_view,
        training_view,
        send2Server,
        sendConfirmation,
        is_loading
    })
</script>

<style lang="scss">
    * {
        margin: 0;
        padding: 0;

        box-sizing: border-box;

        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
            Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue',
            sans-serif;
        font-size: 0.99rem;
    }

    #app {
        width: 100%;
        height: 100vh;

        display: flex;
        flex-direction: column;
        align-items: center;

        background-color: #111;
        color: #cacaca;

        overflow: hidden;
    }
</style>
