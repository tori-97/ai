<template>
    <div @click="download_symbol" ref="symbol" :class="`symbols ${_available ? 'available': 'non-available'}`">
        <div ref="progress" class="progress"></div>
        <div v-if="!loading" class="content">
            {{ name }}
        </div>
        <div class="symbol-spinner" v-else>
            <i class="fas fa-spinner fa-spin"></i>
        </div>
    </div>
</template>
<script lang="ts" setup>
    import { defineExpose, ref, defineProps, getCurrentInstance, watch } from 'vue'
    import manager from '@/manager'

    const inst = getCurrentInstance()
    const app = inst?.root.exposed?.app as manager

    const props = defineProps<{
        name: string,
        available: boolean
    }>()

    const symbol = ref<HTMLDivElement>()
    const progress = ref<HTMLDivElement>()
    let loading = ref<boolean>(false)
    const _available = ref<boolean>(props.available)

    const load = (amount: number) => {
        if (!progress.value) return false
        progress.value.style.width = amount + '%'
    }

    const download_symbol = () => {
        if(_available.value) return false

        app.comunicate('data', 'data.manager.symbols.update', {
            name: props.name,
        })
        loading.value = true
    }

    watch(loading, (val, oldVal) => {
        if ( val === false && oldVal === true ){
            if(!progress.value) return false
            progress.value.style.display = "none";
        }
    })

    defineExpose({
        load,
        loading,
        _available
    })
</script>
<style lang="scss" scoped>
    .symbols {
        width: auto;
        min-width: 6rem;
        height: 3rem;

        white-space: nowrap;

        overflow: hidden;

        background-color: #999;
        box-shadow: 0px 0px 4px 0px #222;
        color: rgb(26, 145, 15);

        display: flex;
        align-items: center;
        justify-content: flex-start;

        border-radius: 0.45rem;

        font-size: 0.88rem;
        font-weight: 500;

        cursor: pointer;

        position: relative;

        transition-duration: 280ms;

        .progress {
            width: 0%;
            height: 100%;

            background-color: rgba(51, 51, 51, 0.708);

            position: absolute;

            display: flex;
            align-items: center;
            justify-content: center;

            transition-duration: 280ms;

            overflow: hidden;
        }

        .content {
            width: 100%;

            display: flex;
            align-items: center;
            justify-content: center;

            padding: 0.4rem;
        }

        .symbol-spinner {
            width: 100%;
            height: 100%;

            display: flex;
            align-items: center;
            justify-content: center;
        }
    }

    .available {
        background-color: #208020;
        color: #111;
        box-shadow: 0px 0px 2px 0px #222;
    }

    .non-available {
        background-color: #222;
        color: #cacaca;
    }
</style>
