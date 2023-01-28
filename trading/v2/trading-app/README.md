# trading-app

## TODO:
  repair errors on popups then its possible to continue develope


```js
// Access to component values

<template>
  <div>
    <modal-component ref="modal"></modal-component>
  </div>
</template>

<script lang="ts" setup>

  import ModalComponent from "@/components/ModalComponent.vue"
  import { ref, onMounted } from "vue";

  const modal = ref<InstanceType<typeof ModalComponent> | null>(null)

  onMounted(() => {
    modal.value?.close()
  })


</script>

<style lang="scss">
#app {

}
</style>


// Modal file:

<template>
    <div class="modal"></div>
</template>
<script lang='ts' setup>

    import { defineExpose, getCurrentInstance, onMounted } from 'vue';

    const cinstance = getCurrentInstance()

    const open = () => {
        console.log("Modal is open")
    }

    const close = () => {
        console.log("Modal is closed")
    }

    onMounted(() => {
        console.log("Modal is mounted...")
    })

    defineExpose({
        open,
        close
    })

</script>
<style lang='scss' scoped>

    .modal { 
        width: 10rem;
        height: 10rem;

        background-color: #222;
    }

</style>

```
