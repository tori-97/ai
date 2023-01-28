<template>
    <div class="container">
        <slot></slot>
    </div>
</template>
<script lang="ts" setup></script>
<style lang="scss" scoped>
    .container {
        width: 100%;
        height: 100%;

        display: flex;
        overflow: hidden;
    }
</style>
