<!--
    Author: Andre Ching Wei Jie
    Date Written: 12/08/2020
-->
<template>
    <v-container fluid class="ma-0 pa-0">
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

        <v-card class="mt-4 mx-auto" max-width="100%">
            <v-card-title>
                <h4 class="mx-auto">Set up Slack Workspace/Channel</h4>
            </v-card-title>
            <v-card-subtitle class="d-flex">
                <h4 class="mx-auto">
                    To set up the Slack Workspace/Channel, you may refer to the
                    Documentation below.
                </h4>
            </v-card-subtitle>
            <div id="example-1" class="text-center pb-4">
                <v-btn
                    color="blue darken-1"
                    class="white--text"
                    :href="pdfLink"
                    target="_blank"
                >
                    <v-icon left>mdi-file</v-icon> Documentation
                </v-btn>
            </div>
        </v-card>
        <v-row class="mt-9">
            <v-col cols="5">
                <v-card class="mx-auto" max-width="100%" height="100%">
                    <v-sheet
                        class="v-sheet--offset d-flex mx-auto"
                        elevation="6"
                        max-width="calc(100% - 32px)"
                        color="navigation"
                    >
                        <span
                            class="d-flex align-center mr-auto white--text pl-4 py-7"
                            >OAuth Access Token</span
                        >
                        <v-card-actions class="pr-4">
                            <v-btn
                                :disabled="checkOAuth"
                                color="blue darken-1"
                                class="white--text saveBtn"
                                @click="postAccessToken()"
                            >
                                <v-icon class="pr-2"></v-icon>
                                Save
                            </v-btn>
                        </v-card-actions>
                    </v-sheet>
                    <v-text-field
                        label="xorb-xxxxx"
                        v-model="tokenStr"
                        single-line
                        solo
                        class="ml-4 mr-4 mt-9"
                    ></v-text-field>
                </v-card>
            </v-col>
            <v-col>
                <v-card class="mx-auto" max-width="100%" height="100%">
                    <v-sheet
                        class="v-sheet--offset d-flex mx-auto"
                        elevation="6"
                        max-width="calc(100% - 32px)"
                        color="navigation"
                    >
                        <span
                            class="d-flex align-center mr-auto white--text pl-4 py-7"
                            >Channel ID</span
                        >
                        <v-card-actions class="pr-4">
                            <v-btn
                                :disabled="checkTypedURL"
                                color="blue"
                                class="white--text saveBtn"
                                @click="postChannelId()"
                            >
                                <v-icon class="pr-2"></v-icon>
                                Assign
                            </v-btn>
                        </v-card-actions>
                    </v-sheet>
                    <v-select
                        v-model="selectedToken"
                        :items="tokens"
                        item-text="tokenStr"
                        item-value="id"
                        label="Select OAuth Token..."
                        solo
                        class="ml-4 mr-4"
                    ></v-select>
                    <v-text-field
                        label="Enter Channel ID here"
                        v-model="channelStr"
                        single-line
                        solo
                        class="ml-4 mr-4"
                    ></v-text-field>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="5">
                <div id="example-1" class="text-right pb-3">
                    <v-btn
                        :disabled="disabled"
                        color="error"
                        @click="deleteItems()"
                        >Delete Token</v-btn
                    >
                </div>

                <v-card>
                    <v-data-table
                        v-model="selected"
                        :headers="headers"
                        :items="channelLogs"
                        show-select
                        item-key="id"
                        class="elevation-1"
                        :loading="isLoading"
                    >
                    </v-data-table>
                </v-card>
            </v-col>

            <v-col>
                <div id="example-1" class="text-right pb-3">
                    <v-btn
                        :disabled="disabled2"
                        color="error"
                        @click="deleteItems2()"
                        >Unassign Channel</v-btn
                    >
                </div>
                <v-card>
                    <v-data-table
                        v-model="selected2"
                        :headers="headers2"
                        :items="channelToken"
                        show-select
                        item-key="id"
                        class="elevation-1"
                        :loading="isLoading"
                    >
                    </v-data-table>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import axios from 'axios';

export default {
    data() {
        return {
            snackbar: false,
            selectedToken: null,
            channelStr: '',
            tokenStr: '',
            token: '',
            accesstoken: '',
            message: '',
            snackbarColor: 'info',
            tokens: [],
            selected: [],
            selected2: [],
            selectedIds: [],
            selectedIds2: [],
            channelLogs: [],
            channelToken: [],
            isLoading: false,
            headers: [{ text: 'Access Tokens', value: 'tokenStr' }],
            headers2: [
                { text: 'Access Tokens', value: 'tokenStr' },
                { text: 'Channel ID', value: 'channelStr' },
            ],
            pdfLink: require('@/assets/documentation/documentation.pdf'),
        };
    },
    computed: {
        checkTypedURL: function () {
            return this.channelStr != '' ? false : true;
        },

        checkOAuth: function () {
            return this.tokenStr != '' ? false : true;
        },

        disabled() {
            let notSelected = true;

            if (this.selected != 0) {
                notSelected = false;
            }

            return notSelected;
        },

        disabled2() {
            let notSelected = true;

            if (this.selected2 != 0) {
                notSelected = false;
            }

            return notSelected;
        },
    },

    mounted() {
        this.fetchRecords();
        this.getAccessToken();
        this.getTokenList();
        this.fetchChannelTokens();
    },

    methods: {
        //Get all access tokens from the database
        fetchRecords() {
            this.isLoading = true;
            axios
                .get('http://127.0.0.1:8000/api/access_token/')
                .then((response) => {
                    this.channelLogs = response.data.Success;
                    this.isLoading = false;
                });
        },

        //Get all channel tokens from the database
        fetchChannelTokens() {
            this.isLoading = true;
            axios
                .get('http://127.0.0.1:8000/api/channels/')
                .then((response) => {
                    this.channelToken = response.data.Success;
                    this.isLoading = false;
                });
        },

        //Close snackbar
        closeButton() {
            this.snackbar = false;
        },

        //Get a access token
        getAccessToken() {
            var accessData = new FormData();

            for (var i = 0; i < this.accesstoken.length; i++) {
                accessData.append('tokenStr', this.accesstoken[i]);
            }

            axios({
                method: 'get',
                url: 'http://127.0.0.1:8000/api/access_token/',
                data: accessData,
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            })
                .then((response) => {
                    this.accesstoken = this.tokenStr;
                    //this.tokenStr = response.data.Success[0].tokenStr;
                    console.log(response);
                })
                .catch((response) => {
                    console.log(response);
                });
        },

        //Get list of access tokens
        getTokenList() {
            axios
                .get(
                    'http://127.0.0.1:8000/api/access_token/getValidAccessToken'
                )
                .then((response) => {
                    this.tokens = response.data.Success;
                    console.log(JSON.stringify(this.tokens));
                    console.log(response);
                    console.log('Success');
                    this.selectedToken = this.tokens[0].id;
                })
                .catch((response) => {
                    console.log(response);
                    console.log('Error');
                });
        },

        //Delete all selected access tokens from the database
        deleteItems() {
            // Delete selected PPE records from the database
            this.selected.forEach((row) => {
                this.selectedIds.push(row.id);
            });

            var msg =
                'Are you sure you want to disconnect this channel from the Slack workgroup?';

            if (this.selectedIds.length > 1) {
                msg = `Are you sure you want to disconnect these ${this.selectedIds.length} channels from the Slack workgroup?`;
            }

            //Convert array to form data
            var formDatas = new FormData();
            for (var i = 0; i < this.selectedIds.length; i++) {
                formDatas.append('id', this.selectedIds[i]);
            }

            if (confirm(msg)) {
                // Send data as JSON
                //axios.delete('/api/logs', data: JSON.stringify(this.selectedIds))
                // Send data as form data
                axios({
                    method: 'delete',
                    url: 'http://127.0.0.1:8000/api/access_token/',
                    data: formDatas,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                    .then((response) => {
                        //success
                        console.log(response);
                        // Refresh table
                        this.fetchRecords();
                        this.getTokenList();

                        // Remove selection
                        this.selectedIds = [];
                        this.selected = [];

                        this.message = 'Successfully deleted the record(s)';
                        this.snackbarColor = 'success';
                        this.snackbar = true;
                    })
                    .catch((response) => {
                        //error
                        console.log(response);
                        this.message =
                            'There was an error when deleting the records. Please try again.';
                        this.snackbar = true;
                        this.snackbarColor = 'error';
                    });
            }
        },

        //Save an access token
        postAccessToken() {
            let formData = new FormData();
            formData.append('tokenStr', this.tokenStr);
            formData.append('isValid', true);

            axios({
                method: 'post',
                url: 'http://127.0.0.1:8000/api/access_token/',
                data: formData,
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            })
                .then((response) => {
                    console.log(response);
                    this.fetchRecords();
                    this.getTokenList();

                    this.message = 'Successfully added the access token.';
                    this.snackbarColor = 'success';
                    this.snackbar = true;
                    this.tokenStr = '';
                })
                .catch((response) => {
                    for (const value of formData.values()) {
                        console.log(value);
                    }

                    this.message =
                        'There was an error when adding the access token. Please try again.';
                    this.snackbarColor = 'error';
                    this.snackbar = true;
                });
        },

        //Save a new channel assignment
        postChannelId() {
            console.log(JSON.stringify(this.selectedToken));
            let channelData = new FormData();

            channelData.append('tokenStr', this.selectedToken);
            channelData.append('channelStr', this.channelStr);
            channelData.append('isValid', true);

            axios({
                method: 'post',
                url: 'http://127.0.0.1:8000/api/channels/',
                data: channelData,
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            })
                .then((response) => {
                    //success
                    console.log(response);
                    this.fetchChannelTokens();

                    this.message =
                        'Successfully assigned the access token to the Channel ID';
                    this.snackbarColor = 'success';
                    this.snackbar = true;
                    this.channelStr = '';
                })
                .catch((response) => {
                    //error
                    console.log(response);

                    this.message =
                        'There was an error when assigning the access token to the Channel ID. Please try again.';
                    this.snackbarColor = 'error';
                    this.snackbar = true;
                });
        },

        // Remove all selected channel assignments from the database
        deleteItems2() {
            // Delete selected PPE records from the database
            this.selected2.forEach((row) => {
                this.selectedIds2.push(row.id);
            });

            var msg =
                'Are you sure you want to unassign this Access Token and Channel ID?';

            if (this.selectedIds2.length > 1) {
                msg = `Are you sure you want to unassign these Access Tokens and Channel IDs?`;
            }

            //Convert array to form data
            var formDatas = new FormData();
            for (var i = 0; i < this.selectedIds2.length; i++) {
                formDatas.append('id', this.selectedIds2[i]);
            }

            if (confirm(msg)) {
                // Send data as JSON
                //axios.delete('/api/logs', data: JSON.stringify(this.selectedIds))
                // Send data as form data
                axios({
                    method: 'delete',
                    url: 'http://127.0.0.1:8000/api/channels/',
                    data: formDatas,
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                })
                    .then((response) => {
                        //success
                        console.log(response);
                        // Refresh table
                        this.fetchChannelTokens();

                        this.message =
                            'Successfully unassigned the access token and the Channel ID';
                        this.snackbarColor = 'success';
                        this.snackbar = true;

                        // Remove selection
                        this.selectedIds2 = [];
                        this.selected2 = [];
                    })
                    .catch((response) => {
                        //error
                        console.log(response);

                        this.message =
                            'There was an error when unassigning the access token and Channel ID. Please try again.';
                        this.snackbarColor = 'error';
                        this.snackbar = true;
                    });
            }
        },
    },
};
</script>
<style>
.saveBtn.theme--light.v-btn.v-btn--disabled:not(.v-btn--flat):not(.v-btn--text):not(.v-btn--outlined) {
    background-color: #c5c5c5 !important;
}
</style>
