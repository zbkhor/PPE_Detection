<!--
    Author: Wang Wei Liang Matthew, Andre Ching Wei Jie
    Date Written: 10/08/2020
-->
<template>
    <v-app class="primary" style="height: 100%;">
        <v-app-bar
            app
            color="tertiary"
            class="elevation-0 main-header pa-0 ma-0"
        >
            <v-app-bar-nav-icon
                @click.stop="toggleMini = !toggleMini"
            ></v-app-bar-nav-icon>
            <v-toolbar-title class="pa-0 primaryTxt--text">
                {{ currentRouteName }}
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <!--<v-btn @click="toggleTheme" class="mr-6">
                {{ buttonText }}
            </v-btn>-->
            <div>
                <v-menu offset-y>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            class="ma-2"
                            text
                            icon
                            v-bind="attrs"
                            v-on="on"
                            @click="clearNotif"
                        >
                            <v-badge
                                :content="newMessages"
                                :value="newMessages"
                                color="red"
                                overlap
                            >
                                <v-icon :color="bellColor">mdi-bell</v-icon>
                            </v-badge>
                        </v-btn>
                    </template>
                    <v-list>
                        <v-list-item
                            id="valueOptions"
                            to="/managelogs"
                            @click="clearDropdown"
                        >
                            <v-list-item-title>
                                <v-icon
                                    id="valueOptionsIcon"
                                    :color="iconColor"
                                    >{{ icon }}</v-icon
                                >
                                <span
                                    id="valueOptionsText"
                                    class="d-flex align-center"
                                    >{{ violationMsg }}</span
                                >
                            </v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-menu>
            </div>
        </v-app-bar>
        <div style="height: 100%;">
            <v-navigation-drawer
                v-model="sidebarMenu"
                app
                :permanent="sidebarMenu"
                :mini-variant.sync="mini"
                mini-variant-width="80"
                color="navigation"
                class="main-sidebar d-flex flex-column"
                id="appNavigation"
            >
                <v-list dense class="pa-0 mx-auto sidebar-icon" width="100%">
                    <v-list-item>
                        <v-list-item-content class="pa-0" style="height: 85%;">
                            <v-icon style="fill: white; height: 100%;"
                                >$ectclogo</v-icon
                            >
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
                <v-list nav class="px-3 pt-0" id="navigationList">
                    <v-divider class="grey darken-1 mb-3"></v-divider>
                    <v-list-item
                        v-for="item in items"
                        :key="item.title"
                        link
                        :to="item.href"
                        v-ripple="{ class: `white--text`, center: true }"
                    >
                        <v-list-item-icon class="px-0">
                            <v-icon color="navigationTxt">
                                {{ item.icon }}
                            </v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title
                                class="nav-text navigationTxt--text"
                            >
                                {{ item.title }}
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
                <v-spacer></v-spacer>
                <v-list nav class="px-3 pt-0 mb-2">
                    <v-list-item
                        link
                        href="http://127.0.0.1:8082/visitor"
                        target="_blank"
                        v-ripple="{ class: `white--text`, center: true }"
                        id="openVisitorAppBtn"
                        class="orange darken-2"
                    >
                        <v-list-item-icon class="px-0">
                            <v-icon color="navigationTxt"
                                >mdi-open-in-app</v-icon
                            >
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title
                                class="nav-text navigationTxt--text"
                            >
                                Visitor Console
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-navigation-drawer>
            <v-main class="primary" style="height: 100%;">
                <v-container fluid class="py-2" style="margin-bottom: 85px;">
                    <v-row>
                        <v-col class="px-5 py-0">
                            <transition name="fade">
                                <router-view></router-view>
                            </transition>
                        </v-col>
                    </v-row>
                </v-container>
                <!-- Footer -->
                <v-footer
                    color="blue-grey"
                    class="px-8"
                    style="height: 85px !important;"
                    absolute
                >
                    <v-icon
                        style="
                            width: 190px;
                            height: 100%;
                            fill: #fff !important;
                        "
                        class="mr-4"
                        >$ectclogo</v-icon
                    >
                    <v-icon
                        style="
                            width: 170px;
                            height: 100%;
                            fill: #fff !important;
                        "
                        >$dsaclogo</v-icon
                    >

                    <v-spacer></v-spacer>
                    <span style="color: #fff;"
                        ><b
                            >Video Analytics for PPE Detection, Beta Version</b
                        ></span
                    >
                    <v-spacer></v-spacer>
                    <span style="color: #fff;"><b>Sponsored by TIEFA</b></span>
                </v-footer>
            </v-main>
        </div>
    </v-app>
</template>

<script>
import axios from 'axios';

export default {
    name: 'App',
    computed: {
        //Shrink navigation menu to only show icons
        mini() {
            return this.$vuetify.breakpoint.smAndDown || this.toggleMini;
        },
        buttonText() {
            return !this.$vuetify.theme.dark ? 'Dark Mode' : 'Light Mode';
        },
        currentRouteName() {
            return this.$route.meta.title;
        },
    },
    data: () => ({
        sidebarMenu: true,
        toggleMini: false,
        items: [
            { title: 'Dashboard', href: '/', icon: 'home' },
            {
                title: 'PPE Selection',
                href: '/ppeselection',
                icon: 'mdi-hard-hat',
            },
            {
                title: 'Manage Logs',
                href: '/managelogs',
                icon: 'mdi-file-document-outline',
            },
            {
                title: 'Slack Notifications',
                href: '/slacknotifications',
                icon: 'mdi-bell-outline',
            },
            { title: 'Settings', href: '/settings', icon: 'mdi-cog-outline' },
        ],

        violationValue: 0,
        violationMsg: '',
        icon: '',

        newMessages: 0,
        oldLogCount: 0,
        show: true,

        bellColor: 'grey',
        iconColor: 'green',
    }),

    async mounted() {
        let result = await this.getTotalLogCount();
        if (result) {
            setInterval(() => {
                this.getViolationNumber();
            }, 5000);
        }
        this.violationMsg;
        this.clearDropdown();
    },

    methods: {
        //Get total log count from database.
        //Check against old log count to see there are new logs.
        //If there are new logs, notify the safety manager using the notification bell
        getViolationNumber() {
            console.log('getViolationNumber: true');
            axios
                .get('http://127.0.0.1:8000/api/details/total_logs/')
                .then((response) => {
                    let newLogCount = response.data.total;
                    console.log('New log count: ' + newLogCount);

                    if (newLogCount > this.oldLogCount) {
                        this.newMessages += newLogCount - this.oldLogCount;
                        this.oldLogCount = newLogCount;

                        if (this.newMessages > 0) {
                            var date = new Date().toLocaleDateString();
                            var time = new Date().toLocaleTimeString();
                            this.violationMsg =
                                'As of ' +
                                date +
                                ' at ' +
                                time +
                                ', ' +
                                this.newMessages +
                                ' new violation(s) have been detected. Click here to check the logs.';
                            this.icon = 'mdi-alert-circle';
                            this.iconColor = 'red';
                            this.bellColor = '#FFD700';
                            console.log(this.violationMsg);
                        }
                        console.log(this.newMessages);
                    }
                });
        },

        //Get current total log count from database
        getTotalLogCount() {
            console.log('getTotalLogCount: true');
            return new Promise((resolve) => {
                axios
                    .get('http://127.0.0.1:8000/api/details/total_logs/')
                    .then((response) => {
                        this.oldLogCount = response.data.total;
                        console.log('Current Log Count: ' + this.oldLogCount);
                    });
                resolve(true);
            });
        },

        //Clear notifications from bell
        clearNotif() {
            if (this.newMessages == 0) {
                this.violationMsg = 'No new violations.';
                this.iconColor = 'green';
                this.icon = 'mdi-check';
            }
            this.newMessages = 0;
            this.bellColor = 'grey';
        },
        //Clear message from bell dropdown
        clearDropdown() {
            this.violationMsg = 'No new violations.';
            this.icon = 'mdi-check';
        },
    },
};
</script>

<style>
#app {
    font-family: 'Open Sans', 'Roboto', Arial, Helvetica, sans-serif !important;
}

#app.theme--light {
    background-color: #f8f9fa;
}

.v-btn__content {
    font-size: 0.8rem;
    font-weight: 600;
}

.nav-text {
    font-size: 0.9rem !important;
}

.v-toolbar__title {
    font-size: 1.1rem !important;
}

.v-toolbar__content {
    padding: 0 20px !important;
    margin: 0 !important;
    height: 54px !important;
}

.sidebar-icon,
.sidebar-icon .v-list-item {
    height: 54px !important;
}

.sidebar-icon .v-icon--is-component {
    width: 52px;
    height: 52px;
}

#appNavigation .v-navigation-drawer__content {
    display: flex;
    flex-direction: column;
}

#valueOptions {
    background-color: unset !important;
}

#valueOptions::before {
    background: unset !important;
}

#valueOptions .v-list-item__title {
    display: flex;
}

#valueOptionsIcon {
    margin-right: 10px;
}

#valueOptionsText {
    font-size: 0.9rem;
}

#openVisitorAppBtn {
    font-weight: normal;
}

.v-card__title {
    font-weight: normal !important;
}

.v-snack__content {
    padding-right: 8px !important;
}
</style>

<style scoped>
.v-list--dense {
    border-radius: 0 !important;
}

.tertiary {
    background-color: #ffffff !important;
}

.v-application .title {
    font-size: 1.1rem !important;
}

.v-app-bar {
    border-bottom: 1px solid #ccc !important;
    padding: 0px 12px !important;
}

.v-list-item {
    font-weight: 300;
    border-radius: 4px !important;
}

.v-list--nav .v-list-item {
    padding: 0 16px !important;
}

.v-list--nav .v-list-item:hover:not(.v-list-item--active) {
    background-color: rgba(255, 255, 255, 0.1);
}

#navigationList .v-list-item--active {
    color: #1e88e5 !important;
    background-color: #1e88e5;
    font-weight: normal !important;
}

.v-list--nav .v-list-item__icon {
    margin: 14px 0;
}

.main-header,
.v-app-bar {
    height: 54px !important;
}

.v-content {
    padding-top: 54px !important;
}
</style>
