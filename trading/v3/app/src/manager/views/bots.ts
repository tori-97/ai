import BotsView from "@/views/BotsView.vue"
import { Ref } from "vue"
import { TasksResponseType } from "../types"

function init(task: TasksResponseType, view: Ref<InstanceType<typeof BotsView>>){ 
    if(!view.value) return false
   
    if ( task.name === "bots.get.all" ){
        
        
        if ( task.done ){
            view.value.updateBots(task.data)
        }

    }else if ( task.name === "bots.create" ){

        if(task.done){
            view.value.refresh_page()
            view.value.create_bot_modal.modal.close()
            view.value.notification(task.client_msg)
        }else {
            view.value.notification(task.client_msg)
        }
    }else if ( task.name === "bots.delete" ){
        
        if(task.done){
            view.value.refresh_page()
        }
        view.value.notification(task.client_msg)
    }
}


export default init