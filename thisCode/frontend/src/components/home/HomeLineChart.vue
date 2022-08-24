<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <v-card class="mx-auto" max-width="100%">
        <v-card-title>
            <span>Total PPE Violations</span>
        </v-card-title>
        <v-card-subtitle>
            <span class="font-weight-light grey--text text--darken-2"
                >Shows the total number of PPE violations for each day.</span
            >
        </v-card-subtitle>
        <apexchart
            ref="lineChart"
            type="line"
            height="250"
            :options="chartOptionsLine"
            :series="lineSeriesData"
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
    name: 'HomeLineChart',

    components: {
        apexchart: VueApexCharts,
    },

    props: ['seriesLine', 'datesLine', 'tickAmt'],

    //Retrieve data from parent component and set accordingly
    watch: {
        seriesLine: function () {
            console.log(this.seriesLine);
            this.lineSeriesData = this.seriesLine;
        },
        datesLine: function () {
            this.$refs.lineChart.updateOptions({
                xaxis: {
                    categories: this.datesLine,
                },
            });
        },
        tickAmtLine: function () {
            this.$refs.lineChart.updateOptions({
                yaxis: {
                    tickAmount: this.tickAmtLine,
                    labels: {
                        formatter: function (value) {
                            return parseInt(value, 10);
                        },
                    },
                },
            });
        },
    },

    data: function () {
        return {
            lineSeriesData: [],
            chartOptionsLine: {
                chart: {
                    toolbar: {
                        show: false,
                    },
                    width: '100%',
                    height: 250,
                    type: 'line',
                    zoom: {
                        enabled: false,
                    },
                },
                dataLabels: {
                    enabled: false,
                },
                stroke: {
                    curve: 'straight',
                },
                title: {
                    text: undefined,
                },
                grid: {
                    row: {
                        colors: ['#f3f3f3', 'transparent'],
                        opacity: 0.5,
                    },
                },
                xaxis: {
                    categories: [],
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
                    // Hardcoded data for chart - testing purposes
                this.seriesLine = [{
                        name: "Total PPE Violations",
                        data: [3, 0, 9, 20, 4]
                    }]
                }*/
};
</script>

<style scoped></style>
