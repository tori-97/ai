<template>
    <div class="loader">
        <div class="spinner"></div>
        <div class="msg">{{ msg }}</div>
    </div>
</template>
<script lang="ts" setup>

    import { defineProps } from "vue"

    defineProps<{
        msg: string
    }>()

</script>
 <style lang="scss" scoped>

    @keyframes spin {
        to { 
            transform: rotate(360deg);
        }
    }

    .loader { 
        width: 100%;
        height: 100%;

        background-color: #bebebe;
        color: #222;

        position: absolute;

        display: flex;
        align-items: center;
        justify-content: center;

        overflow: hidden;

        transition-duration: 280ms;

        .spinner { 
            display: inline-block;
            width: 22rem;
            height: 22rem;

            border-radius: 50%;
            border: solid .2rem #cacaca;
            border-top: solid .2rem #222;

            animation: spin 780ms ease-in-out infinite;

            overflow: hidden;

        }

        .msg { 
            max-width: 22rem;
            max-height: 22rem;

            position: absolute;

            padding: 1.8rem;
            margin: 1rem;

            overflow: hidden;
            overflow-y: auto;

            font-size: .88rem;
            font-weight: 500;

            transition-duration: 280ms;

        }
    }
</style>
