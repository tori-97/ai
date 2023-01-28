<template>
    <div class="button">
        <div v-if="icon" class="icon">
            <i :class="icon"></i>
        </div>
        <div class="label">
            <slot />
        </div>
    </div>
</template>
<script lang='ts' setup>

    import { defineProps } from 'vue';

    defineProps<{
        icon?: string
    }>()

</script>
<style lang='scss' scoped>

    .button {
        width: auto;
        height: 2rem;

        background-color: #333;
        box-shadow: 0px 0px 4px 0px #222;
        color: #cacaca;

        border-radius: .2rem;

        display: flex;
        align-items: center;
        justify-content: center;

        padding: .4rem;

        .icon {
            margin: .25rem;

            i {
                font-size: .88rem;
            }

            display: flex;
            align-items: center;
            justify-content: center;
        }

        .label {
            font-size: .8rem;
            font-weight: 500;

            display: flex;
            align-items: center;
            justify-content: center;

            &::selection {
                background-color: transparent;
            }
        }

        &:hover {
            background-color: #be8f16;
            color: #222;
            cursor: pointer;
        }
    }
</style>