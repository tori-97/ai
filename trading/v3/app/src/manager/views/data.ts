function init(task: any, view: any){ 
    if(!view.value) return false

   if ( task.name === 'data.manager.symbols.downloadable' ){


        if ( task.done ){
            view.value.symbols = task.data
            view.value.loading = false
        }else {
            view.value.loading = true
            view.value.loading_msg = task.client_msg
        }

    }else if ( task.name === 'data.manager.symbols.available' ){
 
         if ( task.done ){
             view.value.symbols_available = Object.keys(task.data)
         }
    }else if ( task.name === 'data.manager.symbols.update' ){

        const symbols = view.value.listSymbols()
        const symbol = symbols[`symbol_${task.data.name}`][0]
        symbol.load(task.data.load)

        if(task.done){
            symbol.loading = false
            symbol._available = true
        }
    }
    
} 



export default init