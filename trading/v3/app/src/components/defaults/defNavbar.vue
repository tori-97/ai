<template>
    <div class="navbar">
        <div v-if="brand" class="brand" @click="brand_on_click">
            {{ brand }}
        </div>
        <div class="extend" :style="{'justify-content': justify, 'align-items': align, 'width': width}">
            <slot />
        </div>
    </div>
</template>
<script lang='ts' setup>

    import { defineProps } from 'vue';

    defineProps<{
        brand?: string,
        brand_on_click?: any
        justify?: "center" | "flex-start" | "flex-end" | "space-between",
        align?: "center" | "flex-start" | "flex-end" | "space-between",
        width?: string
    }>()


</script>
<style lang='scss' scoped>

    .navbar { 
        width: 100%;
        height: 3.2rem;

        background-color: #222;
        color: #bebebe;
        box-shadow: 0px 0px 4px 0px #222;

        display: flex;
        align-items: center;
        justify-content: space-between;

        padding: .65rem;

        .brand { 
            width: 100%;

            font-size: 1.33rem;
            cursor: pointer;

            &::selection {
                background-color: transparent;
            }
        }

        .extend {
            display: flex;
            align-items: center;
            gap: .4rem;
            
        }
    }


</style>