<!--
    Author: Andre Ching Wei Jie
    Date Written: 12/08/2020
-->
<template>
    <v-container fluid>
        <v-snackbar
            v-model="snackbar"
            :timeout="4000"
            :color="snackbarColor"
            top
            right
        >
            <span class="pr-4">{{ message }}</span>
            <v-btn class="ma-0" @click="closeButton" text>Close</v-btn>
        </v-snackbar>
        <div style="text-align: right;">
            <div id="example-2" style="display: inline-block;">
                <v-dialog v-model="dialog" scrollable max-width="450px">
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            color="blue"
                            class="white--text"
                            v-bind="attrs"
                            v-on="on"
                            :disabled="disabledFilter"
                        >
                            <v-icon class="mr-2">
                                mdi-sort
                            </v-icon>
                            Filter
                        </v-btn>
                    </template>

                    <v-card>
                        <v-card-title>Filter By...</v-card-title>

                        <v-card-text style="width: 450px;">
                            <span>Date and Time</span>
                            <v-datetime-picker
                                label="Start Date/Time"
                                v-model="startDateTime"
                                class="pt-2"
                            >
                            </v-datetime-picker>
                            <v-datetime-picker
                                label="End Date/Time"
                                v-model="endDateTime"
                            >
                            </v-datetime-picker>

                            <v-divider></v-divider>

                            <span class="mt-2">Expected PPE</span>
                            <div style="display: flex;">
                                <v-checkbox
                                    v-model="expectedPPESelection"
                                    label="Hard Hat"
                                    id="hardHatExpected"
                                    value="ObjectViolated"
                                    color="blue"
                                ></v-checkbox>
                                <div class="ml-2">
                                    <v-checkbox
                                        v-model="expectedPPESelection"
                                        label="Gloves"
                                        value="Gloves"
                                        color="blue"
                                    ></v-checkbox>
                                </div>
                            </div>

                            <span>Missing PPE</span>
                            <div style="display: flex;">
                                <v-checkbox
                                    v-model="missingPPESelection"
                                    label="Hard Hat"
                                    value="ObjectViolated"
                                    color="blue"
                                ></v-checkbox>
                                <div class="ml-2">
                                    <v-checkbox
                                        v-model="missingPPESelection"
                                        label="Gloves"
                                        value="Gloves"
                                        color="blue"
                                    ></v-checkbox>
                                </div>
                            </div>
                            <!-- <span>Is Compliant?</span> -->

                            <!-- <div style="display: flex;">
                                <v-radio-group v-model="isCompliant">
                                    <v-radio
                                        label="Both"
                                        value="0"
                                        color="blue"
                                    ></v-radio>
                                    <v-radio
                                        label="Yes"
                                        value="1"
                                        color="blue"
                                    ></v-radio>
                                    <v-radio
                                        label="No"
                                        value="2"
                                        color="blue"
                                    ></v-radio>
                                </v-radio-group>
                            </div> -->
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions style="margin-left: 65%;">
                            <v-btn
                                color="blue darken-1"
                                text
                                @click="dialog = false"
                                >Close</v-btn
                            >
                            <v-btn
                                color="blue darken-1"
                                text
                                @click="closeAndFilterDialog(filterLogs)"
                            >
                                Filter
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </div>
            <div
                id="example-1"
                class="text-right pb-2 pl-2"
                style="display: inline-block;"
            >
                <v-btn
                    :disabled="disabled"
                    color="error"
                    @click="deleteItems()"
                >
                    <v-icon class="mr-2">
                        mdi-delete
                    </v-icon>
                    Delete Row
                </v-btn>
            </div>
        </div>

        <!-- Id Retrieval Test -->
        <!-- <h5>{{ selectedRows }}</h5> -->
        <v-card>
            <v-data-table
                v-model="selected"
                :headers="headers"
                :items="filterLogs"
                show-select
                item-key="id"
                class="elevation-1"
                :headers-length="headersLength"
                sort-by="id"
                :sort-desc="true"
                :loading="isLoading"
                loading-text="Retrieving your logs..."
            >
                <template v-slot:item.id="{ item }">
                    <span>
                        {{
                            filterLogs
                                .map(function (x) {
                                    return x.id;
                                })
                                .indexOf(item.id) + 1
                        }}
                    </span>
                </template>

                <template v-slot:item.image="{ item }">
                    <expandable-image
                        class="expandable-image"
                        :src="'data:image/png;base64,' + item.image"
                    />
                </template>
                <template v-slot:item.compliant="{ item }">
                    <div v-if="item.compliant">
                        <v-icon class="green--text">mdi-check</v-icon>
                    </div>
                    <div v-else>
                        <v-icon class="red--text">mdi-close</v-icon>
                    </div>
                </template>
            </v-data-table>
        </v-card>
    </v-container>
</template>

<script>
import axios from 'axios';
import Vue from 'vue';
import DateTimePicker from 'vuetify-datetime-picker';
import VueExpandableImage from 'vue-expandable-image';
import moment from 'moment';

Vue.use(DateTimePicker);
Vue.use(VueExpandableImage);

export default {
    name: 'ManageLogs',
    data() {
        return {
            selected: [],
            selectedIds: [],

            logs: [],
            filterLogs: [],
            selectedFilterList: [],

            dialog: false,

            startDateTime: null,
            endDateTime: null,

            snackbar: false,
            snackbarColor: 'info',
            message: '',

            count: 0,

            headers: [
                { text: 'No.', value: 'id' },
                { text: 'Time', value: 'time' },
                { text: 'PPE', value: 'condition' },
                { text: 'PPE Violated', value: 'ObjectViolated' },
                { text: 'Image', value: 'image', align: 'center' },
            ],
            isLoading: true,

            //For filters
            expectedPPESelection: [],
            missingPPESelection: [],
            isCompliant: '0',
        };
    },

    mounted() {
        this.fetchRecords();
    },

    methods: {
        //Fetch detection logs from database to populate table
        fetchRecords() {
            // Fetch PPE records from the database
            axios
                .get('http://127.0.0.1:8000/api/tf2/')
                .then((response) => {
                    this.logs = response.data.Success;
                    this.logs.sort((a, b) => a.id - b.id); //added, sorts the logs by ID in ascending order
                    //console.log(this.filterLogs);
                    this.filterLogs = [...this.logs];
                    this.isLoading = false;
                })
                //added
                .catch((response) => {
                    console.log(response.response);
                });
            //end of added
        },

        //Delete rows selected by the user
        deleteItems() {
            //Reset
            this.selectedIds = [];

            // Delete selected PPE records from the database
            this.selected.forEach((row) => {
                this.selectedIds.push(row.id);
            });

            var msg = 'Are you sure you want to delete this log?';

            if (this.selectedIds.length > 1) {
                msg = `Are you sure you want to delete these ${this.selectedIds.length} logs?`;
            }

            //Convert array to form data
            var formData = new FormData();
            for (var i = 0; i < this.selectedIds.length; i++) {
                formData.append('id', this.selectedIds[i]);
            }

            if (confirm(msg)) {
                // Send data as JSON
                //axios.delete('/api/logs', data: JSON.stringify(this.selectedIds))
                // Send data as form data
                axios({
                    method: 'delete',
                    url: 'http://127.0.0.1:8000/api/tf2/',
                    data: formData,
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                })
                    .then((response) => {
                        //success
                        console.log(response);
                        // Refresh table
                        this.fetchRecords();

                        // Remove selection
                        this.selectedIds = [];
                        this.selected = [];

                        this.message =
                            'Your log(s) have been deleted successfully.';
                        this.snackbarColor = 'success';
                        this.snackbar = true;
                    })
                    .catch((response) => {
                        //error
                        console.log(response);

                        this.message =
                            'Failed to delete the log(s). Please try again.';
                        this.snackbarColor = 'error';
                        this.snackbar = true;
                    });
            }
        },

        //Filter the logs based on the options selected by the user in the filter options box
        closeAndFilterDialog() {
            console.log('closeAndFilterDialog: true');
            this.filterLogs = [];
            //Create a copy of the original logs
            var newList = [...this.logs];
            var violatedlist = [...this.logs];
            console.log(newList);
            console.log(this.expectedPPESelection.length + 'PPESELECTION');
            console.log(this.expectedPPESelection);

            //Remove logs in list based on filters that are true
            //If there is a filter selected for the expected ppe group
            if (this.expectedPPESelection.length > 0) {
                console.log('-----ExpectedPPESelection: true');
                if (this.expectedPPESelection.length >= 2) {
                    console.log(
                        '--------ExpectedPPESelection: Gloves and Hard hat'
                    );
                    //Hard hat & Gloves selected
                    newList = newList.filter((item) => {
                        return (
                            item.objectsDetected.includes('Hard hat') &&
                            item.objectsDetected.includes('Gloves')
                        );
                    });
                } else if (this.expectedPPESelection == 'ObjectViolated') {
                    console.log('--------ExpectedPPESelection: Hard hat only');
                    //Hard hat selected
                    let regex = /^No Object Violated$/;
                    newList = newList.filter((item) => {
                        return regex.test(item.ObjectViolated);
                    });
                } else {
                    console.log('--------ExpectedPPESelection: Gloves only');
                    //Gloves selected
                    let regex = /^Gloves$/;
                    newList = newList.filter((item) => {
                        return regex.test(item.ObjectViolated);
                    });
                }
            }

            if (this.missingPPESelection.length > 0) {
                console.log('----------MissingPPESelection: true');
                console.log(this.missingPPESelection.length);
                console.log(this.missingPPESelection);
                if (this.missingPPESelection.length >= 2) {
                    newList = newList.filter((item) => {
                        return (
                            item.objectViolated.includes('Hard hat') &&
                            item.objectViolated.includes('Gloves')
                        );
                    });
                } else if (this.missingPPESelection == 'ObjectViolated') {
                    let regex = /^Hard hat$/;
                    violatedlist = violatedlist.filter((item) => {
                        return regex.test(item.ObjectViolated);
                    });
                } else {
                    let regex = /^Hard hat$/;
                    newList = newList.filter((item) => {
                        return regex.test(item.objectViolated);
                    });
                }
            }

            // if (parseInt(this.isCompliant) != 0) {
            //     newList = newList.filter((item) => {
            //         return parseInt(this.isCompliant) === 1
            //             ? item.compliant
            //             : !item.compliant;
            //     });
            // }

            //If start and end datetime are specified
            if (this.startDateTime != null && this.endDateTime != null) {
                let startUnix = moment(
                    this.startDateTime,
                    'YYYY-MM-DD, HH:mm'
                ).unix();
                let endUnix = moment(
                    this.endDateTime,
                    'YYYY-MM-DD, HH:mm'
                ).unix();

                newList = newList.filter((item) => {
                    return (
                        moment(item.time, 'DD-MM-YY , HH:mm').isSameOrAfter(
                            this.startDateTime,
                            'YYYY-MM-DD, HH:mm'
                        ) &&
                        moment(item.time, 'DD-MM-YY , HH:mm').isSameOrBefore(
                            this.endDateTime,
                            'YYYY-MM-DD, HH:mm'
                        )
                    );
                });
            } else if (this.startDateTime != null) {
                //If only start datetime is specified
                newList = newList.filter((item) => {
                    console.log(
                        '-----------Condition: ' +
                            moment(item.time, 'DD-MM-YY , HH:mm').isSameOrAfter(
                                this.startDateTime,
                                'YYYY-MM-DD, HH:mm'
                            )
                    );
                    return moment(item.time, 'DD-MM-YY , HH:mm').isSameOrAfter(
                        this.startDateTime,
                        'YYYY-MM-DD, HH:mm'
                    );
                });
            } else if (this.endDateTime != null) {
                //If only end datetime is specified
                newList = newList.filter((item) => {
                    return moment(item.time, 'DD-MM-YY , HH:mm').isSameOrBefore(
                        this.endDateTime,
                        'YYYY-MM-DD, HH:mm'
                    );
                });
            }

            console.log('-------startDateTime: ' + this.startDateTime);
            console.log('-------endDateTime: ' + this.endDateTime);

            if (
                this.expectedPPESelection.length == 1 &&
                this.missingPPESelection.length == 1
            ) {
                this.filterLogs = newList;
                this.filterLogs.push.apply(newList, violatedlist);
            } else if (this.expectedPPESelection.length == 1) {
                this.filterLogs = newList;
            } else if (this.missingPPESelection.length == 1) {
                this.filterLogs = violatedlist;
            }
            this.dialog = false;
        },

        //Close the snackbar if its open
        closeButton() {
            if (this.snackbar) this.snackbar = false;
        },
    },
    computed: {
        disabled() {
            let notSelected = true;

            if (this.selected != 0) {
                notSelected = false;
            }

            return notSelected;
        },
        disabledFilter() {
            let notEmpty = true;

            if (this.logs != 0) {
                notEmpty = false;
            }

            return notEmpty;
        },
        headersLength() {
            return this.headers.length + 1;
        },
    },
};
</script>
<style>
.v-progress-linear {
    background: #4169e1;
}

img {
    max-width: 200px;
    height: auto;
    max-height: 100%;
}

.align-left {
    margin-left: 2em;
}

.v-date-picker-title__year,
.v-date-picker-title__date,
.v-picker__title__btn,
.v-picker-title {
    color: rgba(0, 0, 0, 0.87);
}
</style>
