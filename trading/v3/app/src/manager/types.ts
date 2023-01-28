import { Ref } from "vue"

import BotsView from "@/views/BotsView.vue"
import TrainingView from "@/views/TrainingView.vue"
import DataView from "@/views/DataView.vue"
import HomeView from "@/views/HomeView.vue"

import PopUp from "@/components/PopUp.vue"

interface ViewsType{
    home: Ref<InstanceType<typeof HomeView> | null>
    bots: Ref<InstanceType<typeof BotsView> | null>
    training_room: Ref<InstanceType<typeof TrainingView> | null>
    data: Ref<InstanceType<typeof DataView> | null>
    popup: Ref<InstanceType<typeof PopUp> | null>
}

interface TasksResponseType{
    name: string
    view: string
    done: boolean
    data: any
    client_msg: string
    inner_task: TasksResponseType
}

export {
    ViewsType,
    TasksResponseType
}