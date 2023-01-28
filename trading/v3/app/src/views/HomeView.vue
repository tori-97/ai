<template>
    <div class="view">
        <def-container class="container"></def-container>
        <!-- <def-loader class="loading"> </def-loader> -->
    </div>
</template>
<script lang="ts" setup>
    import { getCurrentInstance } from 'vue'
    import Root from '@/manager'

    const instance = getCurrentInstance()
    const app = instance?.root.exposed?.app as Root
</script>
<style lang="scss" scoped>
    .view {
        width: 100%;
        height: 100%;

        display: flex;
        flex-direction: column;
        align-items: center;

        .container {
            transition-duration: 250ms;

            display: flex;
            flex-wrap: wrap;
            justify-items: flex-start;
            justify-content: center;
            align-items: flex-start;
            align-content: flex-start;
            gap: 0.4rem;

            overflow: hidden;
            overflow-y: auto;

            padding: 0.5rem;
        }

        .loading {
            width: 100%;
            position: absolute;
        }
    }
</style>
