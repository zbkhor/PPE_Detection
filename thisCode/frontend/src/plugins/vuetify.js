import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import light from './vuetify/lightTheme';
import VueTableDynamic from 'vue-table-dynamic';
import ectclogo from '../components/logos/EctcLogo.vue';
import dsaclogo from '../components/logos/DsacLogo.vue';

Vue.use(Vuetify);
Vue.use(VueTableDynamic);

export default new Vuetify({
    theme: {
        themes: { light },
    },
    icons: {
        values: {
            ectclogo: {
                component: ectclogo,
            },
            dsaclogo: {
                component: dsaclogo,
            },
        },
    },
});
