<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
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
        <div class="d-flex align-center">
            <v-spacer></v-spacer>
            <v-btn
                :disabled="disabled"
                color="blue"
                class="white--text"
                @click="saveSelection()"
            >
                <v-icon class="pr-2"></v-icon>
                <span>SAVE</span>
            </v-btn>
        </div>
        <v-card class="mt-4 mx-auto" max-width="100%">
            <v-card-title>
                <span class="mx-auto">Select the PPEs to detect</span>
            </v-card-title>
            <v-card-subtitle class="d-flex">
                <span class="mx-auto">
                    You can select/deselect a PPE by clicking their respective
                    buttons.
                </span>
            </v-card-subtitle>
            <v-list class="d-flex mx-auto ppe-btn-list justify-center">
                <v-list-item v-for="(button, i) in buttons" :key="i">
                    <v-btn
                        class="mx-auto"
                        :class="{ selected: button.selected }"
                        @click="select(button)"
                    >
                        <v-icon class="equipmentIcon" large>
                            {{ button.equipmentIcon }}
                        </v-icon>
                        <div class="btn-text">
                            {{ button.equipmentName }}
                        </div>
                    </v-btn>
                </v-list-item>
            </v-list>
        </v-card>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    name: 'EquipmentSelection',
    data: function () {
        return {
            message: '',
            originalSelection: [],
            currentSelection: [],
            buttons: [],
            snackbar: false,
            snackbarColor: 'info',
        };
    },
    methods: {
        //When the user clicks on the close button in the snackbar
        closeButton() {
            this.snackbar = false;
        },

        // When a ppe button is clicked
        select(button) {
            this.errorMsg = '';
            if (button.selected) {
                let onlyOneSelected = true;
                // Check if button is the only one selected
                this.buttons.forEach((oneBtn) => {
                    // Check all buttons except the current button
                    if (!(button.id === oneBtn.id)) {
                        if (oneBtn.selected) {
                            onlyOneSelected = false;
                        }
                    }
                });

                if (!onlyOneSelected) {
                    button.selected = false;

                    //Remove item from currentSelection
                    let index = this.currentSelection.indexOf(button.id);
                    this.currentSelection.splice(index, 1);
                } else {
                    // Display error message if user is trying to deselect the only button that is selected
                    this.snackbarColor = 'error';
                    this.message = 'At least one PPE must be selected!';
                    this.snackbar = true;
                }
            } else {
                button.selected = true;

                //Add item id from currentSelection
                this.currentSelection.push(button.id);
            }

            console.log(this.currentSelection);
        },
        saveSelection() {
            //Convert array to form data
            var formData = new FormData();
            for (var i = 0; i < this.currentSelection.length; i++) {
                formData.append('selectionEquipment', this.currentSelection[i]);
            }

            // Pass selection to API to save in database
            axios({
                method: 'post',
                url: '/api/ppeselections/',
                data: formData,
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            })
                .then((response) => {
                    //success
                    this.originalSelection = this.currentSelection.slice();
                    console.log(response);
                    this.message = 'Success! Your option(s) have been saved.';
                    this.snackbar = true;
                    this.snackbarColor = 'success';
                })
                .catch((error) => {
                    //error
                    console.log(error.response.data.Error);
                    this.message = 'Failed to save your selection.';
                    this.snackbar = true;
                    this.snackbarColor = 'error';
                });
        },
    },
    computed: {
        // Enables save button when there are changes from the original selection.
        disabled() {
            let noChanges = true;

            // Check that both arrays are the same length
            if (this.originalSelection.length != this.currentSelection.length) {
                // If the lengths are not the same, then a change occured
                noChanges = false;
            } else {
                // For each item in the current selection, check if it exists in the original selection
                let exists = false;

                this.currentSelection.forEach((currentItem) => {
                    this.originalSelection.forEach((originalItem) => {
                        // If first item id matches any item id in the original selection then item
                        // existed in the original selection i.e. no change occured
                        if (currentItem === originalItem) {
                            exists = true;
                        }
                    });

                    // If the current item does not exist in the original selection then a change occured.
                    if (!exists) {
                        noChanges = false;
                    }

                    //Reset exists
                    exists = false;
                });
            }

            return noChanges;
        },
    },
    mounted: function () {
        // Execute only when DOM is mounted

        // Get list of equipment (PPEs)
        //var icons = ['mdi-hand', 'mdi-hard-hat', 'mdi-safety-goggles', 'mdi-shoe-formal', 'mdi-tshirt-crew'];

        axios.get('/api/equipments').then((response) => {
            // For hardcoded icon strings
            /*for (var i = 0; i < response.data.Success.length; i++) {
                        response.data.Success[i].selected = false;
                        response.data.Success[i].icon = icons[i];
                        //console.log(response.data.Success[i]);
                    }*/

            // If icons are retrieved from the database
            response.data.Success.forEach((equipment) => {
                equipment.selected = false;
                //console.log(equipment);
            });

            this.buttons = response.data.Success;

            // Get currently selected PPE
            axios.get('/api/ppeselections/getselection').then((response) => {
                this.originalSelection =
                    response.data.Success.selectionEquipment;

                // Make a copy of the selection retrieved.
                this.currentSelection = this.originalSelection.slice();
                //console.log("Original Selection: " + this.originalSelection);
                //console.log("Current Selection: " + this.currentSelection);

                // Set buttons to show they are selected
                this.originalSelection.forEach((item) => {
                    this.buttons.forEach((button) => {
                        if (item === button.id) {
                            button.selected = true;
                        }
                    });
                });
            }); //END axios.get('/api/ppeselections/getselection')
        }); //END axios.get('/api/equipments')
    },
};
</script>

<style>
.ppe-btn-list .v-btn__content {
    flex-flow: column;
    width: 100%;
}

.ppe-btn-list .v-btn__content {
    white-space: normal;
}

.v-btn .equipmentIcon,
.v-btn .btn-text {
    color: #bdbdbd;
}

.v-btn.selected {
    background-color: #0094ff !important;
}

.v-btn.selected .equipmentIcon,
.v-btn.selected .btn-text {
    color: #fff !important;
}
</style>

<style scoped>
.ppe-btn-list .v-list-item .v-btn {
    width: 150px;
    height: 150px;
}

.ppe-btn-list .v-list-item .v-btn:hover::before {
    opacity: 0.1 !important;
}

.ppe-btn-list {
    flex-wrap: wrap;
}

.ppe-btn-list .v-list-item {
    flex: 0 1 20% !important;
    margin: 20px 0;
}
</style>
