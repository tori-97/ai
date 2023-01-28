<template>
    <div class="loading">
        <div class="spinner">
        </div>
        <div class="message">
            <slot />
        </div>
    </div>
</template>
<script lang="ts" setup></script>
<style lang="scss" scoped>
   @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        10% {
            transform: rotate(36deg);
        }
        20% {
            transform: rotate(72deg);
        }
        30% {
            transform: rotate(108deg);
        }
        40% {
            transform: rotate(144deg);
        }
        50% {
            transform: rotate(180deg);
        }
        60% {
            transform: rotate(216deg);
        }
        70% {
            transform: rotate(252deg);
        }
        80% {
            transform: rotate(288deg);
        }
        90% {
            transform: rotate(324deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    .loading {
        width: 100%;
        height: 100%;

        background-color: #333;
        color: #cacaca;

        display: flex;
        align-items: center;
        justify-content: center;

        overflow: hidden;

        transition-duration: 1s;

        position: relative;

        .spinner {
            width: 35rem;
            height: 35rem;

            transition-duration: 1s;

            // background-color: #111;

            border-radius: 50%;
            border: solid 4px #222;
            border-bottom: solid 4px #cecece;

            animation: spin ease-in-out 1s infinite;
        }

        .message {
            width: 30rem;
            height: 35rem;


            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            
            word-break: break-all;
            word-wrap: break-word;

            display: flex;
            align-items: center;
            justify-content: center;

            flex-wrap: wrap;

            overflow: hidden;
            z-index: 0;

            padding: .8rem;

        }
    }
</style>
