<template>
    <div class="message">
        <div class="title">{{ title }}</div>
        <div class="body">{{ text }}</div>
    </div>
</template>
<script lang="ts" setup>

    import { ref, defineExpose } from 'vue';

    const title = ref("")
    const text = ref("")

    const showMessage = (_title: string, _text: string) => {
        title.value = _title
        text.value = _text

        const msg = document.querySelector(".message") as HTMLDivElement
        msg.style.top = "1rem";

        setTimeout(()=> {
            msg.style.top = "-10rem"
        }, 2500)
    }

    defineExpose({
        showMessage
    })



</script>
 <style lang="scss" scoped>
    .message { 
        width: 60%;

        background-color: #bebebe;
        color: #222;
        
        position: absolute;
        top: -10rem;

        border-radius: .4rem;
        z-index: 99;

        transition-duration: 280ms;

        .title { 
            width: 100%;
            height: 2rem;
            background-color: #333;
            color: #cacaca;

            display: flex;
            align-items: center;

            padding: .8rem;
            font-size: .99rem;
            font-weight: 500;
        }

        .body {
            width: 100%;
            height: 100%;

            display: flex;
            align-items: center;
            justify-content: center;

            padding: .8rem;

            font-size: .88rem;
            font-weight: 400;

            overflow: hidden;
            overflow-y: auto;

        }
    }

</style>
