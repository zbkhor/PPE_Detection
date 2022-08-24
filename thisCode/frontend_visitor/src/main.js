import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import '@mdi/font/css/materialdesignicons.css';
import '@fortawesome/fontawesome-free/css/all.css';
import './assets/sass/styles.scss';

import VueParticles from 'vue-particles';

Vue.config.productionTip = false;

export const EventBus = new Vue(); // line added by Lina

Vue.use(VueParticles);

new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
}).$mount('#app');
