<template>
    <div ref="popup" class="popup">{{ message }}</div>
</template>
<script lang="ts" setup>

    import { ref, defineExpose } from "vue"

    const message = ref<string>('')
    const popup = ref<HTMLDivElement>()

    const showMessage = (_message: string) => {
        if(!popup.value) return false

        message.value = _message as string
        popup.value.style.bottom = "1rem"

        setTimeout(() => {
            if(!popup.value) return false
            popup.value.style.bottom = "-10rem"   
            
        }, 2000)
    }
    
    defineExpose({
        showMessage
    })
</script>
<style lang="scss" scoped>

    .popup { 
        width: 18rem;
        height: 3rem;

        background-color: #111;
        box-shadow: 0px 0px 4px 0px #222;
        color: #bebebe;

        border-radius: .4rem;

        position: absolute;
        bottom: -10rem;
        right: 1rem;

        display: flex;
        align-items: center;
        flex-wrap: wrap;

        padding: .4rem;

        font-size: .88rem;

        transition-duration: 280ms;
    }

</style>
