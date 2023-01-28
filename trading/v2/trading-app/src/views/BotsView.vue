<template>
    <container id="bots-view">
        
    </container>
</template>
<script lang="ts" setup>
    import container from '@/components/AppContainer.vue'
import { RootType } from '@/utils/types';

    import { defineExpose, onMounted, getCurrentInstance } from 'vue';

    let ins = getCurrentInstance()
    const root = ins?.root.exposed as RootType

    onMounted(() => {
        root.send2Server({
            query: "bot-get-all"
        })
    })

    const getAll = () => {
        console.log("get-all")
    }

    defineExpose({
        getAll
    })


</script>
<style lang="scss" scoped>

    #bots-view {
        width: 90%;

        background-color: #333;
        box-shadow: 0px 0px 4px 0px #222;


    }

</style>
