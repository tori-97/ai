<template>
    <div ref="custom_modal" class="modal">
        <header>
            <slot name="header" />
        </header>
        <main>
            <slot />
        </main>
        <footer>
            <slot name="footer" />
        </footer>
    </div>
</template>
<script lang="ts" setup>

    import { ref, defineExpose } from "vue"

    const custom_modal = ref<HTMLDivElement>()

    const open = () => {
        if(!custom_modal.value) return false
        custom_modal.value.style.display = "flex";
    }

    const close = () => {
        if(!custom_modal.value) return false
        custom_modal.value.style.display = "none";
    }

    defineExpose({
        open,
        close
    })

</script>
<style lang="scss" scoped>

    .modal { 
        width: auto;
        height: auto;

        background-color: #222;
        box-shadow: 0px 0px 4px 0px #333;
        color: #bebebe;

        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);

        border-radius: .3rem;

        padding: .8rem;

        display: none;
        flex-direction: column;
        align-items: center;
        gap: .4rem;

        overflow: hidden;

        header {
            width: 100%;
            height: 3rem;
            min-height: 3rem;

            background-color: #333;
            border-radius: .2rem;

            display: flex;
            align-items: center;
            justify-content: space-between;

            padding: .6rem;
        }

        main{
            width: 100%;
            height: 100%;

            background-color: #333;
            border-radius: .2rem;

            display: flex;
            align-items: center;
            justify-content: center;
        }
        footer{
            width: 100%;
            height: 2rem;
            min-height: 3rem;

            background-color: #333;
            border-radius: .2rem;

            display: flex;
            align-items: center;
            justify-content: flex-end;

            padding: .6rem;
        }
    }

</style>
