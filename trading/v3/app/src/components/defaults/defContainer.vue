<template>
  <div class="container">
    <slot />
  </div>
</template>
<script lang="ts" setup></script>
<style lang="scss" scoped>
.container {
  width: 100%;
  height: 100%;

//   background-color: #222;
//   color: #bebebe;
//   box-shadow: 0px 0px 4px 0px #222;

  display: flex;

  overflow: hidden;


}
</style>
