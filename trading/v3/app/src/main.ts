import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'

import "@fortawesome/fontawesome-free/css/all.css"

import defNavbar from "@/components/defaults/defNavbar.vue"
import defContainer from "@/components/defaults/defContainer.vue"
import defButton from "@/components/defaults/defButton.vue"
import defButtonSlide from "@/components/defaults/defButtonSlide.vue"
import defModal from "@/components/defaults/defModal.vue"
import defLoader from "@/components/defaults/defLoader.vue"


const app = createApp(App)

app.component("def-navbar", defNavbar)
app.component("def-container", defContainer)
app.component("def-btn", defButton)
app.component("def-btn-slide", defButtonSlide)
app.component("def-modal", defModal)
app.component("def-loader", defLoader)

app.mount('#app')