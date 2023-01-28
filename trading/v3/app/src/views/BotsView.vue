<template>
    <div class="view">
        <def-navbar class="top-bar">
            <def-btn @click="create_bot_modal?.modal?.open" icon="fas fa-plus-circle">Create Bot</def-btn>
        </def-navbar>
        <def-container class="container">
            <div class="bots-group" v-if="bots.length > 0">
                <div class="bot" v-for="bot in bots" :key="bot.name">
                     <div class="bot-info">{{ bot.name }}</div>
                    <!--<div class="bot-info">Lr: {{ bot.lr }}</div>
                    <div class="bot-info">HL: {{ bot.hidden_layers }}</div>
                    <div class="bot-info">Gamma: {{ bot.gamma }}</div>
                    <div class="bot-info">DR: {{ bot.discounter_rate }}</div> -->
                    <div class="bot-options">
                        <def-btn @click="edit_bot_modal?.open(bot)" icon="fas fa-edit"></def-btn>
                        <def-btn @click="delete_bot(bot.name)" icon="fas fa-trash"></def-btn>
                    </div>
                </div>
            </div>
            <div class="bots-group-empty" v-else>
                Oh no you don't have anybots yet !!
            </div>
        </def-container>
    </div>


    <CreateBotModal ref="create_bot_modal"></CreateBotModal>
    <EditBotModal ref="edit_bot_modal"></EditBotModal>
</template>
<script lang='ts' setup>

    import CreateBotModal from "@/components/views/bots/CreateBotModal.vue"
    import EditBotModal from "@/components/views/bots/EditBotModal.vue"

    import { onMounted, ref, getCurrentInstance, defineExpose } from "vue"
    import Root from "@/manager"

    const create_bot_modal = ref<InstanceType<typeof CreateBotModal> | null>(null)
    const edit_bot_modal = ref<InstanceType<typeof EditBotModal> | null>(null)

    interface BotsViewBotsType{
        discounter_rate: number
        gamma: number
        hidden_layers: number
        lr: number
        name: string
    }

    const bots = ref<Array<BotsViewBotsType>>([])
    
    const instance = getCurrentInstance()
    const app = instance?.root.exposed?.app as Root


    const refresh_page = () => {
        app.comunicate('bots', 'bots.get.all', null)
    }


    onMounted(() => {
        refresh_page()
        app.notification("Welcome to bots")
    })


    const updateBots = (_bots: any) => { bots.value = _bots }

    const delete_bot = (name: string) => {

        app.comunicate('bots', 'bots.delete', {
            name: name
        })
    }

    const notification = (message: string) => {
        app.notification(message)
    }


    defineExpose({
        updateBots,
        refresh_page,
        create_bot_modal,
        edit_bot_modal,
        notification
    })

</script>
<style lang='scss' scoped>


    .view { 
        width: 100%;
        height: 100%;

        display: flex;
        flex-direction: column;
        align-items: center;

        .top-bar {
            background-color: #cacaca;
            box-shadow: 0px 0px 2px 0px #bebebe;

            height: 2.8rem;
        }

        .container {

            transition-duration: 250ms;

            .bots-group{
                width: 100%;
                height: 100%;

                display: flex;
                flex-direction: column;
                align-items: center;

                gap: .2rem;

                padding: .4rem;

                .bot {
                    width: 90%;
                    height: 2.8rem;

                    background-color: #555;

                    display: flex;
                    align-items: center;

                    padding: .4rem;

                    border-radius: .2rem;

                    gap: .6rem;

                    .bot-info {
                        width: auto;
                        white-space: nowrap;

                    }
                    .bot-options {
                        width: 100%;

                        display: flex;
                        align-items: center;
                        justify-content: flex-end;

                        gap: .4rem;

                        padding: .2rem;
                    }
                }
            }

            .bots-group-empty {
                width: 100%;
                height: 100%;

                display: flex;
                align-items: center;
                justify-content: center;
            }
        }


    }


</style>