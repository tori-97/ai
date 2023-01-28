<template>
    <div class="view">
        <def-navbar class="top-bar" brand="Symbols:">

        </def-navbar>
        <def-container v-if="!loading" class="container">
            <SymbolComponent 
                
                v-for="symbol in symbols" 
                :key="symbol" 
                :name="symbol"
                :ref="`symbol_${symbol}`"
                :available="checkIfSymbolIsAvailable(symbol)"
            ></SymbolComponent>
        </def-container>
        <def-loader v-else class="loading">
          {{ loading_msg }}
        </def-loader>
    </div>
</template>
<script lang='ts' setup>

    import SymbolComponent from "@/components/views/data/SymbolComponent.vue";

    import { onMounted, ref, getCurrentInstance, defineExpose } from "vue"
    import Root from "@/manager"

    const instance = getCurrentInstance()
    const app = instance?.root.exposed?.app as Root

    const symbols = ref([])
    const symbols_available = ref([])
    const loading = ref<boolean>(false)
    const loading_msg = ref<string>("")

    onMounted(() => {
        loading.value = true
        app.comunicate('data', 'data.manager.symbols.available', null)
        app.comunicate('data', 'data.manager.symbols.downloadable', null)
        loading_msg.value = "Requesting symbols..."
    })


    const checkIfSymbolIsAvailable = (symbol: string) => {
        if ( symbols_available.value.indexOf(symbol as never) !== -1 ){
            return true
        }
        return false
    }

    const listSymbols = () => {
        return instance?.refs
    }

    defineExpose({
        symbols,
        symbols_available,
        listSymbols,
        checkIfSymbolIsAvailable,
        loading,
        loading_msg
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
            color: #111;

            height: 2.8rem;
        }

        .container {
            transition-duration: 250ms;

            display: flex;
            flex-wrap: wrap;
            justify-items: flex-start;
            justify-content: center;
            align-items: flex-start;
            align-content: flex-start;
            gap: .4rem;

            overflow: hidden;
            overflow-y: auto;

            padding: .5rem;

      
        }

    }


</style>