import { ViewsType } from "./types"
import Socket from "./socket"

import { ref, Ref } from "vue"

export default class {
    views: ViewsType
    private _socket: Socket
    #current_view: Ref<string> = ref('home')

    constructor(views: ViewsType){
        this.views = views
        this._socket = new Socket(this.views)
    }

    comunicate(view: string, query: string , params: any){
        this._socket.send(view, query, params)
    }

    changePage(page: string){
        this.#current_view.value = page
    }

    get current_view(){
        return this.#current_view.value
    }

    ref2Object(data: any){
        const tmp = {}
        Object.assign(tmp, data)
        return tmp
    }
    notification(message: string){
        this.views.popup.value.showMessage(message)
    }
}