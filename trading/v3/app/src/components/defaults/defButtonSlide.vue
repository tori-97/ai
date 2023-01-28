<template>
    <!-- 
         :style="{'justify-content': _clicked ? 'flex-end' : 'flex-start'}"
     -->
    <div ref="btn_slider" class="button clicked">
        <div :class="`slider ${_clicked ? 'clicked' : ''}`"></div>
    </div>
</template>
<script lang='ts' setup>

    import { onMounted, ref, StyleValue } from 'vue';

    let _clicked = ref<boolean>(false)

    const btn_slider = ref<HTMLDivElement>()


    const clickedButton = () => {
        if (!_clicked.value){
            _clicked.value = true
        }else { 
            _clicked.value = false
        }
    }

    onMounted(() => {
        btn_slider.value?.addEventListener("click", clickedButton)
    })




</script>
<style lang='scss' scoped>

    .button {
        width: auto;
        min-width: 3.2rem;
        height: 1.3rem;

        background-color: #222;
        box-shadow: 0px 0px 4px 0px #222;
        color: #cacaca;

        border-radius: 5rem;

        display: flex;
        align-items: center;
        overflow: hidden;
        transition-duration: 1s;
        position: relative;

        .slider { 
            width: 1.2rem;
            height: 1.2rem;

            background-color: #cacaca;

            border-radius: 50%;
            
            position: absolute;
            right: 2rem;

            transition-duration: 280ms;

        }
        
        .clicked {
            right: 0;   
            
            background-color: #444;
        }

        &:hover {
            cursor: pointer;
        }
    }



</style>