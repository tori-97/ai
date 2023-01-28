<template>
  <div class="graph-container">
    <div class="stock-graph">
      <canvas id="graph"></canvas>
    </div>
  </div>

</template>
<script lang='ts' setup>
    import { Chart, registerables } from "chart.js"
    import annotation from "chartjs-plugin-annotation"

    import { defineExpose, getCurrentInstance } from "vue";
    import manager from "@/manager";

    const inst = getCurrentInstance()
    const app = inst?.root?.exposed?.app as manager

    function randcolor(){ return '#'+(0x1000000+Math.random()*0xffffff).toString(16).substr(1,6) }

    Chart.register(...registerables, annotation)

    interface BotType{
      type: 'point',
      xValue: Array<string>,
      yValue: Array<number>,
      backgroundColor: string
    }

    interface ActiveBotsType{
      [key: string]: BotType
    }

    let chart: Chart;
    const active_bots = {} as ActiveBotsType
    
    const create  = (label: string, x: Array<string>, y: Array<number>) => {
      const graph = document.querySelector("#graph") as HTMLCanvasElement

      if (!graph) return false

      if (chart) {
        chart.destroy()
      }
      
      chart = new Chart(graph, {
        type: 'line',
        data: {
          labels: x,
          datasets: [
            {
              label: label,
              data: y
            }
          ]
        },
        options: {
          plugins: {
            annotation: {
              annotations: active_bots as any
            },
          },
          layout: {
            padding: 10
          },
          responsive: true,
          // animation: true,
          spanGaps: false,
          maintainAspectRatio:  false,
          animations: {
            tension: {
              duration: 500
            }
          }
        }
      })

      if(!graph.parentElement) return false
      
      let dyn_width = x.length * 2
      if ( dyn_width > 25000 ){
        dyn_width = 25000
      } else if ( dyn_width < 5000 ){
        dyn_width = 5000
      }

      graph.parentElement.style.width = `${dyn_width}px`
      graph.parentElement.style.minWidth = `${dyn_width}px`
      
      return true
    }

    const update = (label: string, x: Array<string>, y: Array<number>) => {
      if(!chart) return false
      chart.data.labels = x
      chart.data.datasets[0].label = label
      chart.data.datasets[0].data = y
      chart.update()
      // chart.resize(x.length * 500, 100)
      return true
    }

    const clear = () => {
      if(!chart) return false
      chart.clear()
      return true
    }

    const registerBots = (bots: Array<string>) => {
      if(!chart) return false
      bots.forEach((bot: string) => {
          let cbot = active_bots[bot]    
          const dlabel = chart.data.labels

            if(dlabel){
                if(cbot === undefined){
                  active_bots[bot] = {
                    type: 'point',
                    xValue: dlabel[0] as Array<string>,
                    yValue: chart.data.datasets[0].data[1] as Array<number>,
                    backgroundColor: randcolor()
                  }
                }
            }

      })
      chart.update()
      return true
    }

    const listActiveBots = () => {
      return Object.keys(active_bots)
    }

    const moveBot = (bot_id: string, day: number) => {
      const bot = active_bots[bot_id] as BotType
      if(!bot) return false
      if(!chart.data.labels) return false

      bot.xValue = chart.data.labels[day] as Array<string>
      bot.yValue = chart.data.datasets[0].data[day] as Array<number>

      chart.update()

      // const stock_graph = document.querySelector(".graph-container")

      // if(!stock_graph) return false

      // const train_speed = app.views.training_room.value.train_speed.value;

      // if ( day % 10 === 0){
        
      //   let left = day * 5
  
      //   if ( train_speed > 100 ){
      //     left = day * 2  
      //   }else if ( train_speed < 100 ){
      //     left = day * 23 
      //   }
      
      //   stock_graph.scrollTo({
      //     left: left
      //   })
      // }

        
      return true
    }

    const deleteBot = (bot_id: string) => {
      delete active_bots[bot_id]
      chart.update()
      return true
    }

    const show = (_show: boolean) => {
      const cont = document.querySelector(".graph-container") as HTMLDivElement
      if(!cont) return false

      if ( _show ){
        cont.style.top = "50%"
      }else {
        cont.style.top = "250%"
      }
    }

    defineExpose({
        create,
        update,
        clear,
        registerBots,
        listActiveBots,
        moveBot,
        deleteBot,
        show
    })
</script>
<style lang='scss' scoped>
  .graph-container {
    width: 80%;
    height: 80%;

    background-color: #222;
    box-shadow: 0px 0px 4px 0px #222;
    
    border-radius: .6rem;

    overflow: hidden;
    overflow-x: auto;

    padding: .8rem;

    display: flex;
    align-items: center;
    justify-content: flex-start;

    transition-duration: 280ms;

    position: absolute;
    top: 250%;
    transform: translateY(-44%);

    .stock-graph {
      min-width: 5000px;
      max-width: 5000px;

      width: 5000px;
      height: 100%;

      overflow: hidden;

      border-radius: .6rem;

      transition-duration: 280ms;

      
      canvas {
        width: 100%;
        height: 100px;

        overflow: hidden;

        background-color: #111;

        padding: .8rem;

      }
    }
  }

</style>