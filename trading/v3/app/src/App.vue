<template>
  <def-navbar brand="Ai Trading" :brand_on_click="app.changePage('home')">
    <ul class="app-menu">
      <li @click="app.changePage('bots')">Bots</li>
      <li @click="app.changePage('data')">Data</li>
      <li @click="app.changePage('training')">Training</li>
      <li >Settings</li>
    </ul>
  </def-navbar>
  <def-container class="container">
    <!-- 
      Views:
        Home
        Bots
        Data
        Training
        Evaluation
        Settings
     -->
    <HomeView v-if="app.current_view === 'home'" ref="bots_view"></HomeView>
    <BotsView v-if="app.current_view === 'bots'" ref="bots_view"></BotsView>
    <DataView v-if="app.current_view === 'data'" ref="data_view"></DataView>
    <TrainingView v-else-if="app.current_view === 'training'" ref="training_view"></TrainingView>
  </def-container>

  <pop-up ref="pop_up"></pop-up>
</template>

<script lang="ts" setup>

  // Views:
  import BotsView from "@/views/BotsView.vue"
  import TrainingView from "@/views/TrainingView.vue"
  import DataView from "@/views/DataView.vue"
  import HomeView from "@/views/HomeView.vue"

  import PopUp from "@/components/PopUp.vue"

  import Root from "@/manager"

  import { defineExpose, onMounted, ref, Ref } from "vue"

  const home_view     = ref<InstanceType<typeof HomeView> | null>()
  const bots_view     = ref<InstanceType<typeof BotsView> | null>()
  const data_view     = ref<InstanceType<typeof DataView> | null>()
  const training_view = ref<InstanceType<typeof TrainingView> | null>()
  const pop_up         = ref<InstanceType<typeof PopUp> | null>()

  const app = new Root({ 
      training_room: training_view as Ref<InstanceType<typeof TrainingView> | null>, 
      bots: bots_view as Ref<InstanceType<typeof BotsView> | null>, 
      home: home_view as Ref<InstanceType<typeof HomeView> | null>,
      data: data_view as Ref<InstanceType<typeof DataView> | null>,
      popup: pop_up as Ref<InstanceType<typeof PopUp> | null>
    })


  defineExpose({
    app
  })

</script>

<style lang="scss">


  * {
    margin: 0;
    padding: 0;

    font-size: 0.99rem;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;

    box-sizing: border-box;

    border: none;

    &:focus { 
      outline: none;
    }
  }

  html,body {
    overflow: hidden;
  }

  #app {
    width: 100%;
    height: 100vh;

    background-color: #bebebe;
    color: #222;

    overflow: hidden;
    .app-menu { 
      list-style: none;

      display: flex;
      align-items: center;
      gap: .2rem;

      li {
        cursor: pointer;
        padding: .6rem;
        transition-duration: 280ms;

        display: flex;
        align-items: center;
        justify-content: center;
        
        &::selection {
          background-color: transparent;
        }
        
        &:is(:hover, :focus){
          background-color: #333;
          box-shadow: 0px 0px 4px 0px #222;
          border-radius: 1rem;
        }

        &:active{
          position: relative;
          top: 1px;
        }
      }
    }

    .container {
      overflow: hidden;
    }
  }
</style>
