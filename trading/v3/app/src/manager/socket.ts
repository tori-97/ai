import { ViewsType } from "./types"

import { bots, training, data } from "./views"


class Socket{
    private _socket: WebSocket
    max_retries = 10
    retry_counter = 0
    is_open = false
    has_error = false
    views: ViewsType

    constructor(views: ViewsType){
        this.views = views

        this._socket = new WebSocket("ws://localhost:9000/")

        this._socket.addEventListener("open", () => {
            console.log("[+] Connection open...")
            this.is_open = true
        })

        this._socket.addEventListener("close", () => {
            console.log("[+] Connection closed...")
            this.is_open = false
        })

        this._socket.addEventListener("error", () => {
            console.log("[+] Connection error...")
            this.is_open = false
            this.has_error = true
        })

        this._socket.addEventListener("message", (ev) => {this.redirector(this.views, ev)})
    }

    redirector(views: ViewsType, ev: MessageEvent){
        const task = JSON.parse(ev.data)

        if ( task.view === 'bots' ){
            bots(task, views.bots)
        }else if ( task.view === 'training' ){
            training(task, views.training_room)
        }else if ( task.view === 'data' ){
            data(task, views.data)
        }

        // console.log(task)
    }


    async send(view: string, query: string , params: any){

        if(!this.is_open && !this.has_error){
            this.retry_counter += 1

            if(this.retry_counter > this.max_retries){
                console.log("[+] Max retries reached, connection cannot be established !! \nPlease Refresh your page")
                return false
            }

            setTimeout(() => {
                console.log(`[+] Connection tried ${this.retry_counter} times send you request !!`)
                this.send(view, query, params)
            }, 1000)

        }else if (this.is_open && !this.has_error) { 
            try {
                this._socket.send(JSON.stringify({
                    query: query,
                    view: view,
                    params: params
                }))
            }catch(e){console.log("[+] Connection not available anymore !!")}

            this.retry_counter = 0
            return true
        }

    }
}

export default Socket