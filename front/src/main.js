import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // 📌 Importamos Vue Router

// 📌 Importamos Vuetify y sus estilos
import { createVuetify } from "vuetify";
import "vuetify/styles"; 
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

// ✅ Configuración correcta de Vuetify
const vuetify = createVuetify({
    components,
    directives
});

const app = createApp(App);

app.use(router); // 📌 Agregamos Vue Router
app.use(vuetify); // 📌 Agregamos Vuetify

app.mount("#app");
