<template>
  <div class="view">
    <def-navbar class="top-bar" justify="space-between" width="100%">
      <div class="btn-group">
        <def-btn @click="new_training_modal?.modalComp?.open">New Training</def-btn>
        <def-btn ref="pause_btn" @click="pause_training" v-if="training_active">{{ !training_paused ? "Pause Training" : "Resume Training" }}</def-btn>
        <def-btn @click="stop_training" v-if="training_active">Stop Training</def-btn>
        <input v-if="training_active" type="range" min="32" max="500" ref="train_speed" value="100" @change="train_speed_update">
      </div>
      <div class="status-light">
        Status:
        <div ref="status_light" class="value"></div>
      </div>
    </def-navbar>
    <def-container class="container">
      <InfoSidebar ref="info_sidebar"></InfoSidebar>
      <def-container class="container-content">
        <StockGraph ref="graph"></StockGraph>
      </def-container>
    </def-container>
  </div>
  <NewTrainingModal ref="new_training_modal"></NewTrainingModal>
</template>
<script lang="ts" setup>

import NewTrainingModal from "@/components/views/training/newTrainingModal.vue" 
import StockGraph from "@/components/views/training/StockGraph.vue";
import InfoSidebar from "@/components/views/training/InfoSidebar.vue"

import { ref, getCurrentInstance, defineExpose, onBeforeUnmount, watch, onMounted } from "vue";

import App from "@/manager"

const graph = ref<InstanceType<typeof StockGraph> | null>();
const new_training_modal = ref<InstanceType<typeof NewTrainingModal> | null>();
const info_sidebar = ref<InstanceType<typeof InfoSidebar> | null>();
const pause_btn = ref<HTMLDivElement>()
const train_speed = ref<HTMLInputElement>()

const training_active = ref(false);
const training_paused = ref(false);
const status_light = ref<HTMLDivElement>()
const instance = getCurrentInstance()
const root = instance?.root.exposed?.app as App

// onBeforeUnmount(() => {

//   if ( training_active.value ){
//     const conf = confirm("If you leave the training will be automatically stopped !!")

//     if( conf ){
//       // stop_training()
//       pause_training()
//     }
//   }
// })


watch(training_active, (val, oldVal) => {
 
  if ( val === true ){
    info_sidebar.value?.setWidth('22rem')
    graph.value?.show(true)
  }else {
    info_sidebar.value?.setWidth('0')
    graph.value?.show(false)
  }
})


const pause_training = () => {
  
  if ( training_paused.value === false ){
    root.comunicate('training', 'trainings.pause', null)
    // pause_btn.textContent = "Resume Training"
    training_paused.value = true
  } else {
    root.comunicate('training', 'trainings.resume', null)
    // pause_btn.textContent = "Pause Training"
    training_paused.value = false

  }
}

const stop_training = () => {
  root.comunicate('training', 'trainings.stop', null)
  training_active.value = false
}

const changeStatusMode = (mode: "active" | "paused" | "stopped" | "errors") => {
  if(!status_light.value) return false

  if(mode === 'active'){
    status_light.value.style.backgroundColor = "green"
  }else if ( mode === 'paused' ){
    status_light.value.style.backgroundColor = "orange"
  }else if ( mode === 'stopped' ){
    status_light.value.style.backgroundColor = "red"
  }else if ( mode === 'errors' ){
    status_light.value.style.backgroundColor = "yellow"
  }
}

const train_speed_update = () => {
  if(!train_speed.value) return false

  const speed = parseInt(train_speed.value.value) / 100
  
  root.comunicate('training', 'trainings.set.speed', {
    speed: speed
  })
}

defineExpose({
    graph,
    new_training_modal,
    training_active,
    changeStatusMode,
    info_sidebar,
    train_speed
})

</script>
<style lang="scss" scoped>
.view {
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  align-items: center;

    overflow: hidden;
  .top-bar {
    background-color: #777;

    .btn-group {
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    .status-light {
      display: flex;
      align-items: center;
      gap: 0.6rem;

      .value {
        width: 1.5rem;
        height: 1.5rem;

        background-color: #cacaca;

        border-radius: 50%;
      }
    }
  }

  .container {
    display: flex;
    align-items: center;
     
    overflow: hidden;

    flex: 1 1 auto;

    .container-content{
      width: 100%;

      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}
</style>
