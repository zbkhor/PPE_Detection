<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <v-app class="primary" style="height: 100vh;">
        <div style="margin-bottom: 85px; height:100%;">
            <v-app-bar
                app
                color="navigation"
                class="elevation-0 main-header pa-0 ma-0"
            >
                <v-toolbar-title class="pa-0 font-weight-regular primary--text"
                    >Visitor Detection Console</v-toolbar-title
                >
            </v-app-bar>
            <router-view></router-view>
        </div>
        <!-- Footer -->
        <v-footer
            color="blue-grey"
            class="px-8 py-0"
            style="height: 85px;"
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
            <span style="color: #fff;">
                <b>Video Analytics for PPE Detection, Beta Version</b>
            </span>
            <v-spacer></v-spacer>
            <span style="color: #fff;"><b>Sponsored by TIEFA</b></span>
        </v-footer>
    </v-app>
</template>

<script>
export default {
    name: 'App'
};
</script>

<style>
#app {
    font-family: 'Open Sans', 'Roboto', Arial, Helvetica, sans-serif !important;
}

.v-btn {
    font-weight: 600 !important;
}

.ectc-icon {
    fill: #ffffff;
}

.v-toolbar__content {
    padding: 0 !important;
}

.v-toolbar__content {
    height: 100%;
}

.v-toolbar__title {
    margin-left: 20px;
    font-family: 'Open Sans', 'Roboto', Arial, Helvetica, sans-serif !important;
}
.v-footer--absolute:not(.v-footer--inset) {
    width: auto !important;
}
</style>

<style scoped>
.tertiary {
    background-color: #ffffff !important;
}

.v-app-bar {
    border-bottom: 1px solid #ccc !important;
    padding: 0px 12px !important;
}

.v-icon.v-icon {
    width: 100%;
    height: 100%;
}
</style>
