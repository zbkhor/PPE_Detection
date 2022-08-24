import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'Dashboard',
        meta: { title: 'Dashboard' },
        component: Home,
    },
    {
        path: '/ppeselection',
        name: 'PPESelection',
        meta: { title: 'PPE Selection' },
        component: () => import('../views/PPESelection.vue'),
    },
    {
        path: '/managelogs',
        name: 'ManageLogs',
        meta: { title: 'Manage Logs' },
        component: () => import('../views/ManageLogs.vue'),
    },
    {
        path: '/slacknotifications',
        name: 'SlackNotifications',
        meta: { title: 'Slack Notifications' },
        component: () => import('../views/SlackNotifications.vue'),
    },
    {
        path: '/settings',
        name: 'Settings',
        meta: { title: 'Settings' },
        component: () => import('../views/Settings.vue'),
    },
    {
        path: '*',
        name: '404',
        component: () => import('../views/Error404.vue'),
    },
];

const router = new VueRouter({
    mode: 'history',
    routes,
});

export default router;
