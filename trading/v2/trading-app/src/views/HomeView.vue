<template>
    <container id="home">
        <div class="widget" id="bots-list">

        </div>
        <div class="widget" id="trainings-list">

        </div>
        <div class="widget" id="active-bots-list">

        </div>
    </container>
</template>
<script lang="ts" setup>
    import Container from "@/components/AppContainer.vue"
    import ClientMessageModal from "@/components/AppClientMessage.vue"

    import { onMounted, ref, defineExpose } from 'vue';

    let cmessage = ref<InstanceType<typeof ClientMessageModal> | null>(null)

    onMounted(() => {
        

        console.log(cmessage.value?.showMessage("test", "test"))
        console.log("Home mounted !!")
    })

    const sayHello = () => {
        console.log("Say Hello")
    }

    defineExpose({
        sayHello
    })

</script>
<style lang="scss" scoped>

    #home { 
        width: 90%;
        background-color: #333;

        display: flex;
        align-items: flex-start;
        justify-content: center;
        flex-wrap: wrap;

        padding: 1.2rem;

        .widget { 

            width: 20%;
            height: 22rem;

            background-color: #222;
            border-radius: .4rem;

            margin: .4rem;

            &:nth-child(2){
                min-width: 50%;
            }
        }
    }

</style>
