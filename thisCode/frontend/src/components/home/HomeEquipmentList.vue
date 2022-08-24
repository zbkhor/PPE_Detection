<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <v-card class="mx-auto" max-width="100%" height="100%">
        <v-sheet
            class="v-sheet--offset d-flex mx-auto"
            elevation="6"
            max-width="calc(100% - 32px)"
            color="navigation"
        >
            <span class="d-flex align-center mr-auto white--text pl-4 py-7"
                >PPEs to Detect</span
            >
            <v-card-actions class="pr-4">
                <v-btn fab small to="/ppeselection" color="blue darken-1">
                    <v-icon color="white">mdi-file-document-edit</v-icon>
                </v-btn>
            </v-card-actions>
        </v-sheet>
        <v-list class="pl-2">
            <v-list-item v-for="(item, i) in items" :key="i">
                <v-list-item-icon>
                    <v-icon
                        class="grey--text text--darken-2"
                        large
                        v-text="item.equipmentIcon"
                    ></v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                    <v-list-item-title
                        class="equipmentList-title grey--text text--darken-2"
                        v-text="item.equipmentName"
                    ></v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list>
    </v-card>
</template>

<script>
import axios from 'axios';

export default {
    name: 'HomeEquipmentList',
    data: function () {
        return {
            item: 1,
            items: [],
        };
    },

    mounted() {
        this.getEquipmentList();
    },

    methods: {
        //Get ppe detection selection from database
        getEquipmentList() {
            axios
                .get('http://127.0.0.1:8000/api/equipments')
                .then((response) => {
                    var equipment = response.data.Success;

                    axios
                        .get(
                            'http://127.0.0.1:8000/api/ppeselections/getselection'
                        )
                        .then((response) => {
                            var selectedEquipment =
                                response.data.Success.selectionEquipment;

                            for (let i = 0; i < selectedEquipment.length; i++) {
                                equipment.forEach((item) => {
                                    if (selectedEquipment[i] == item.id) {
                                        this.items.push(item);
                                    }
                                });
                            }
                        })
                        .catch((error) => {
                            console.log(error.response.data.Error);
                        });
                });
        },
    },
};
</script>

<style>
.equipmentList-title {
    font-weight: 600;
    font-size: 0.95rem;
}
</style>
