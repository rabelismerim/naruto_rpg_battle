import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Tres from '@tresjs/core'
import App from './App.vue'

const app = createApp(App)

app.use(createPinia())
app.use(Tres)
app.mount('#app')