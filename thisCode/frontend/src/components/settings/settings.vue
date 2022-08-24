<!--
    Author: Andre Ching Wei Jie
    Date Written: 12/08/2020
-->
<template>
    <v-container fluid class="ma-0 pa-0">
        <v-snackbar
            v-model="snackbar"
            :color="snackbarColor"
            :timeout="4000"
            top
            right
        >
            <span class="pr-4">{{ message }}</span>
            <v-btn @click="closeButton" text> Close </v-btn>
        </v-snackbar>
        <v-row class="mt-9">
            <v-col cols="6">
                <v-card class="mx-auto" max-width="100%" height="100%">
                    <v-sheet
                        class="v-sheet--offset d-flex mx-auto"
                        elevation="6"
                        max-width="calc(100% - 32px)"
                        color="navigation"
                    >
                        <span
                            class="d-flex align-center mr-auto white--text pl-4 py-7"
                            >Database Management</span
                        >
                        <v-spacer></v-spacer>
                        <v-card-actions class="pr-4 flex-wrap justify-end">
                            <download-csv
                                :data="channelLogs"
                                name="yourRecords.csv"
                            >
                                <v-btn
                                    color="blue darken-1"
                                    class="white--text exportImportBtns"
                                    @click="getRecords()"
                                    :disabled="disabled"
                                >
                                    <v-icon class="pr-2">mdi-upload</v-icon>
                                    Export as CSV
                                </v-btn>
                            </download-csv>
                            <v-btn
                                color="blue"
                                class="white--text exportImportBtns ml-4"
                                @click="submitFile()"
                                :disabled="disabled2"
                            >
                                <v-icon class="pr-2"></v-icon>
                                Import
                            </v-btn>
                        </v-card-actions>
                    </v-sheet>
                    <div class="mr-4 ml-2" id="file-input">
                        <v-file-input
                            id="file"
                            ref="file"
                            v-model="file"
                            accept=".csv"
                        />
                    </div>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';
import Vue from 'vue';
import JsonCsv from 'vue-json-csv';

Vue.component('downloadCsv', JsonCsv);

export default {
    data() {
        return {
            snackbar: false,
            message: '',
            snackbarColor: 'info',
            channelLogs: [],
            file: null,
        };
    },
    computed: {
        disabled() {
            let noRecords = true;

            if (this.channelLogs != 0) {
                noRecords = false;
            }

            return noRecords;
        },
        disabled2() {
            let noFiles = true;

            if (this.file != null) {
                noFiles = false;
            }

            return noFiles;
        },
    },
    mounted() {
        this.getRecords();
        this.sendMessage();
    },
    methods: {
        //Display message informing that the logs are being retrieved in the snackbar
        sendMessage() {
            this.message = 'Retrieving your logs. Please wait.';
            this.snackbar = true;
        },

        //Get all detection logs stored in the database
        getRecords() {
            axios.get('http://127.0.0.1:8000/api/tf2/').then((response) => {
                this.channelLogs = response.data.Success;
                console.log(response.data.Success);
                if (response.data.Success < 1) {
                    this.message = 'Logs are empty.';
                    this.snackbar = true;
                } else if (response.data.Success != 0) {
                    this.message = 'Logs are ready for export.';
                    this.snackbar = true;
                    this.snackbarColor = 'success';
                }
            });
        },

        //Import csv file
        submitFile() {
            let formData = new FormData();
            /* Add the form data we need to submit */
            formData.append('file', this.file);

            axios({
                method: 'POST',
                url: 'http://127.0.0.1:8000/api/dbsettings/db_import/',
                data: formData,
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            })
                .then((response) => {
                    console.log(response);
                    this.message = 'Import is successful.';
                    this.snackbar = true;
                    this.snackbarColor = 'success';
                })
                .catch((error) => {
                    console.log(error.response.data);
                    this.message = error.response.data;
                    this.snackbar = true;
                    this.snackbarColor = 'error';
                });
        },

        //Close snackbar
        closeButton() {
            this.snackbar = false;
        },
    },
};
</script>
<style>
.exportImportBtns.theme--light.v-btn.v-btn--disabled:not(.v-btn--flat):not(.v-btn--text):not(.v-btn--outlined) {
    background-color: #c5c5c5 !important;
}

#file-input .primary--text:first-child {
    color: #cfd8dc !important;
}
</style>
