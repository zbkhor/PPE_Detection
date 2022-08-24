<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <v-card class="mx-auto" max-width="100%">
        <v-card-title>
            <span>Type of PPE Violations</span>
        </v-card-title>
        <v-card-subtitle>
            <span class="font-weight-light grey--text text--darken-2"
                >Shows the kind of PPE that visitors were missing.</span
            >
        </v-card-subtitle>
        <apexchart
            ref="barChart"
            type="bar"
            height="250"
            :options="chartOptionsBar"
            :series="barSeriesData"
        ></apexchart>
        <!--<v-card-text class="pt-0">
            <v-divider class="my-2"></v-divider>
            <v-icon class="mr-2"
                    small>
                mdi-clock
            </v-icon>
            <span class="caption grey--text font-weight-light">last updated 1 hour ago</span>
        </v-card-text>-->
    </v-card>
</template>

<script>
import VueApexCharts from 'vue-apexcharts';

export default {
    name: 'HomeBarChart',

    components: {
        apexchart: VueApexCharts,
    },

    props: ['seriesBar', 'datesBar'],

    //Retrieve data from parent component and set accordingly
    watch: {
        seriesBar: function () {
            console.log(this.seriesLine);
            this.barSeriesData = this.seriesBar;
        },
        datesBar: function () {
            this.$refs.barChart.updateOptions({
                xaxis: {
                    categories: this.datesBar,
                },
            });
        },
    },

    data: function () {
        return {
            barSeriesData: [],
            chartOptionsBar: {
                chart: {
                    type: 'bar',
                    height: 250,
                    stacked: true,
                    toolbar: {
                        show: false,
                    },
                },
                plotOptions: {
                    bar: {
                        horizontal: false,
                    },
                },
                xaxis: {
                    type: 'string',
                    categories: this.datesBar,
                },
                legend: {
                    position: 'right',
                    offsetY: 40,
                },
                fill: {
                    opacity: 1,
                },
                yaxis: {
                    tickAmount: 1,
                    labels: {
                        formatter: function (value) {
                            return parseInt(value, 10);
                        },
                    },
                },
            },
        };
    },

    /*mounted() {
                    //Hardcoded data for chart - testing purposes
                this.barSeriesData = [{
                        name: 'Hard Hat',
                        data: [44, 55, 41, 67, 22]
                    }, {
                        name: 'Goggles',
                        data: [13, 23, 20, 8, 13]
                    }, {
                        name: 'Safety Clothes',
                        data: [11, 17, 15, 15, 21]
                    }, {
                        name: 'Covered Shoes',
                        data: [21, 7, 25, 13, 22]
                    }]
                }*/
};
</script>

<style scoped></style>
