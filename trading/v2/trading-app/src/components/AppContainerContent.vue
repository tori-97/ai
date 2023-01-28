<template>
    <div class="content">
        <slot />
    </div>
</template>
<script lang="ts" setup></script>
<style lang="scss" scoped>
    .content {
        width: 100%;
        height: 100%;

        display: flex;
        flex-direction: column;
        align-items: center;

        overflow: hidden;
    }
</style>
