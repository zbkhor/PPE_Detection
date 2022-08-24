import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import light from './vuetify/lightTheme';
import ectclogo from '../components/logos/EctcLogo.vue';
import dsaclogo from '../components/logos/DsacLogo.vue';
import shirticon from '../components/detection_process/icons/shirtIcon.vue';
import pantsicon from '../components/detection_process/icons/pantsIcon.vue';
import bootsicon from '../components/detection_process/icons/bootsIcon.vue';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: { light }
    },
    icons: {
        values: {
            ectclogo: {
                component: ectclogo
            },
            dsaclogo: {
                component: dsaclogo
            },
            shirtIcon: {
                component: shirticon
            },
            pantsIcon: {
                component: pantsicon
            },
            bootsIcon: {
                component: bootsicon
            }
        }
    }
});
