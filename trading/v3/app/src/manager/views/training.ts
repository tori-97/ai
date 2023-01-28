import TrainingView from "@/views/TrainingView.vue"
import { Ref } from "vue"

import { TasksResponseType } from "../types"

function init(task: TasksResponseType, view: Ref<InstanceType<typeof TrainingView> | null>){ 
    if(!view.value) return false

    if ( task.name === "data.manager.symbols"){ 
        // TODO
    }else if ( task.name === 'bots.get.all' ){
        
        view.value.new_training_modal.updateAvailableBots(task.data) 

    }else if (task.name === 'data.manager.symbols.all' ){

        view.value.new_training_modal.updateAvailableSymbols(task.data) 

    }else if (task.name === 'bots.get' ){

        view.value.new_training_modal.update_configuration(JSON.parse(task.data)) 

    }else if ( task.name === 'trainings.start' ){ 

        const inner_task = task.inner_task 
        
        if ( view.value ) {           
            view.value.training_active = true
        }

        if(inner_task){
      
            if (inner_task.name === 'load-data' ){
                // view.value.graph.create(task.data)
                view.value.graph.create(inner_task.data.symbol,inner_task.data.days,inner_task.data.closes)
     
            } else if (inner_task.name === 'load-bots' ){
                view.value.graph.registerBots(inner_task.data)
                view.value.info_sidebar.configureThreads(inner_task.data)

            } else if ( inner_task.name === 'update' ){
                view.value.graph.moveBot(inner_task.data.id, inner_task.data.day)
                // view.value.info_sidebar.max_episodes = 20
                view.value.info_sidebar.configuration.max_episodes = inner_task.data.episode
                view.value.info_sidebar.configuration.threads_alive = view.value.graph.listActiveBots().length
                view.value.info_sidebar.updateThread(inner_task.data)

            } else if ( inner_task.name === 'status' ){
                view.value.changeStatusMode(inner_task.data)

                const status_mode = inner_task.data
                if ( status_mode  === 'stopped' ){
                    if ( view.value ) {
                        view.value.training_active = false
                    }
                }
            } else if ( inner_task.name === 'game-over' ){
                view.value.graph.deleteBot(inner_task.data)
                view.value.info_sidebar.deleteThread(inner_task.data)

            }

        }
    }else if ( task.name === 'trainings.set.speed' ){
        console.log(task)
    }else if ( task.name === 'data.manager.symbols.periods' ){
        view.value.new_training_modal.updateAvailablePeriods(task.data)
    }
} 



export default init