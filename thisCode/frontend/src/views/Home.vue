<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
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
        <v-row>
            <v-col cols="6">
                <home-line-chart
                    :seriesLine="seriesLine"
                    :datesLine="datesLine"
                    :tickAmt="tickAmt"
                ></home-line-chart>
            </v-col>
            <v-col cols="6">
                <home-bar-chart
                    :seriesBar="seriesBar"
                    :datesBar="datesBar"
                ></home-bar-chart>
            </v-col>
        </v-row>
        <v-row class="mt-6">
            <v-col cols="4">
                <home-equipment-list></home-equipment-list>
            </v-col>
            <v-col>
                <home-camera></home-camera>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

import HomeLineChart from '@/components/home/HomeLineChart';
import HomeBarChart from '@/components/home/HomeBarChart';
import HomeEquipmentList from '@/components/home/HomeEquipmentList';
import HomeCamera from '@/components/home/HomeCamera';

export default {
    name: 'Home',

    components: {
        HomeLineChart,
        HomeBarChart,
        HomeEquipmentList,
        HomeCamera,
    },

    data: function () {
        return {
            seriesLine: [],
            seriesBar: [],
            datesBar: [],
            datesLine: [],
            myDates: [],
            tickAmt: 0,
            snackbarColor: 'info',
            message: '',
            snackbar: '',
        };
    },

    mounted() {
        this.getChartData();
    },

    methods: {
        //Get data for charts from database
        getChartData() {
            this.message = 'Getting chart data...';
            this.snackbar = true;

            axios
                .get('http://127.0.0.1:8000/api/details/total_violation/')
                .then((response) => {
                    this.seriesLine = [
                        {
                            name: 'PPE Violations',
                            data: response.data.series1.data,
                        },
                    ];
                    this.seriesBar = response.data.series2;
                    console.log('responsedata' + this.seriesBar);
                    //Format dates
                    let dates = response.data.dates;
                    let date = '';
                    for (var i = 0; i < dates.length; i++) {
                        date = moment(dates[i], 'DD-MM-YYYY').format(
                            'DD MMM YY'
                        );
                        dates[i] = date;
                        //console.log(dates[i])
                    }

                    this.datesLine = dates;
                    this.datesBar = dates;

                    //Determine tick amount
                    let tickAmount = 0,
                        minVal = 0,
                        maxVal = 0;
                    let dataArr = response.data.series1.data;
                    minVal = Math.min(...dataArr);
                    maxVal = Math.max(...dataArr);

                    let diffVal = maxVal - minVal;
                    if (diffVal < 6) {
                        tickAmount = diffVal;
                    } else {
                        //default
                        tickAmount = 6;
                    }
                    this.tickAmt = tickAmount;
                    //console.log(tickAmt);
                    this.message =
                        'The chart data has been retrieved successfully.';
                    this.snackbar = true;
                    this.snackbarColor = 'success';
                });
        },

        //Close snackbar if its open
        closeButton() {
            if (this.snackbar) this.snackbar = false;
        },
    },
};
</script>

<style>
.v-sheet--offset {
    top: -24px;
    position: relative;
}
</style>
