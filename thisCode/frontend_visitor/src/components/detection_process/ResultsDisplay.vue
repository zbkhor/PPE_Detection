<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <div id="resultsContainer" class="componentOuterBox">
        <!-- Displays the person detection result-->
        <div
            id="personPanelWrapper"
            class="align-center"
            ref="personPanelWrapper"
            :style="{ display: showPersonResultsPanel }"
        >
            <!-- style="display: flex;" -->
            <div
                id="personPanel"
                class="pl-3 pr-8 d-flex align-center justify-end"
            >
                <div id="personLoaderWrapper">
                    <component
                        :is="personLoaderComponent"
                        ref="personLoaderComponent"
                        class="loaderPos"
                    ></component>
                    <component
                        :is="tickLoaderComponent"
                        ref="tickLoaderComponent"
                        class="loaderPos"
                    >
                    </component>
                </div>
                <span
                    class="pl-4 font-weight-light"
                    :class="personDetected ? 'lime--text' : 'white--text'"
                    >{{ personDetectedText }}</span
                >
            </div>
        </div>
        <!-- Displays the equipment detection results-->
        <div
            id="equipmentPanelWrapper"
            class="align-top"
            ref="equipmentPanelWrapper"
        >
            <!-- commented out
        :style="{ display: showEquipmentResultsPanel }" -->
            <!-- my edits from here -->
            <div id="equipmentPanel">
                <!-- commented out
                    class="pl-8 pr-2 d-flex flex-column"
                -->
                <div id="headArea">
                    <!-- commented out
                        class="d-flex flex-column"
                    -->
                    <div class="equipmentWrapper">
                        <!-- added by lina -->
                        <table>
                            <thead>
                                <tr>
                                    <th>Time</th>
                                    <th>Hardhat</th>
                                    <!-- <th>Glove</th> -->
                                    <!-- <th>Face</th> -->
                                </tr>
                            </thead>

                            <tbody>
                                <tr
                                    v-for="item in personData"
                                    v-bind:key="item.timeRecorded"
                                >
                                    <td>
                                        {{ item.timeRecorded }}
                                    </td>
                                    <td>
                                        <template
                                            v-if="item.hardHatStatus != null"
                                        >
                                            <v-icon
                                                class="green--text"
                                                v-if="item.hardHatStatus"
                                            >
                                                mdi-check</v-icon
                                            >
                                            <v-icon class="red--text" v-else
                                                >mdi-close</v-icon
                                            >
                                        </template>
                                    </td>
                                    <!-- <td>
                                    <template v-if="glovesFound != null">
                                        <v-icon class="green--text" v-if="glovesFound"
                                        >mdi-check</v-icon>
                                        <v-icon class="red--text" v-else
                                        >mdi-close</v-icon>
                                    </template>
                                </td> -->
                                    <td>
                                        <template
                                            v-if="item.personImage !== ''"
                                        >
                                            <!-- edits made -->
                                            <div class="imageWrapper">
                                                <a
                                                    href="#"
                                                    style="
                                                position: relative;
                                                width: 100%;
                                                z-index: 50;
                                                "
                                                    @click="
                                                        viewImg(
                                                            item.resultsCount
                                                        )
                                                    "
                                                >
                                                    <img
                                                        :src="
                                                            'data:image/jpeg;base64,' +
                                                                item.personImage
                                                        "
                                                        width="100"
                                                        height="100"
                                                    />
                                                    <v-icon
                                                        style="
                                                    font-size: 36px;
                                                    color: white;
                                                    width: 35%;
                                                    height: auto;
                                                    background-color: rgba(0, 0, 0, 0.4);
                                                    position: absolute;
                                                    bottom: 30%;
                                                    right: 3%;
                                                    "
                                                        >mdi-magnify-plus-outline</v-icon
                                                    >
                                                </a>
                                                <v-overlay
                                                    :zIndex="zIndex"
                                                    :value="item.overlay"
                                                >
                                                    <div
                                                        :style="{
                                                            width:
                                                                item
                                                                    .personDims[0] +
                                                                'px',
                                                            height:
                                                                item
                                                                    .personDims[1] +
                                                                'px',
                                                            overflow: 'hidden'
                                                        }"
                                                    >
                                                        <img
                                                            :src="
                                                                'data:image/jpeg;base64,' +
                                                                    item.personImage
                                                            "
                                                            :style="{
                                                                marginLeft:
                                                                    -item
                                                                        .personDims[2] +
                                                                    'px',
                                                                marginTop:
                                                                    -item
                                                                        .personDims[3] +
                                                                    'px'
                                                            }"
                                                        />
                                                    </div>

                                                    <v-btn
                                                        class="white--text"
                                                        @click="
                                                            item.overlay = false
                                                        "
                                                        style="
                                                        position: absolute;
                                                        right: 0%;
                                                        bottom: -6%;
                                                    "
                                                    >
                                                        Close
                                                    </v-btn>
                                                </v-overlay>
                                            </div>
                                            <!-- end of edits -->
                                        </template>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <!-- end of my edits -->

                <!-- <v-icon
                            id="hardHatIcon"
                            :style="{ color: hardHatColor }"
                            >mdi-hard-hat</v-icon
                        >
                        <template v-if="hardHatFound != null">
                            <v-icon class="lime--text" v-if="hardHatFound"
                                >mdi-check</v-icon
                            >
                            <v-icon class="red--text" v-else>mdi-close</v-icon>
                        </template>
                    </div>
                    <div class="equipmentWrapper">
                        <v-icon
                            id="gogglesIcon"
                            :style="{ color: gogglesColor }"
                            >mdi-safety-goggles</v-icon
                        >
                        <template v-if="gogglesFound != null">
                            <v-icon
                                class="lime--text"
                                style="margin-top:-1rem;"
                                v-if="gogglesFound"
                                >mdi-check</v-icon
                            >
                            <v-icon
                                class="red--text"
                                style="margin-top:-1rem;"
                                v-else
                                >mdi-close</v-icon
                            >
                        </template>
                    </div>
                </div>
                <div id="upperBodyArea">
                    <div class="equipmentWrapper">
                        <v-icon id="shirtIcon" :style="{ fill: shirtColor }"
                            >$shirtIcon</v-icon
                        >
                        <template v-if="shirtFound != null">
                            <v-icon class="lime--text" v-if="shirtFound"
                                >mdi-check</v-icon
                            >
                            <v-icon class="red--text" v-else>mdi-close</v-icon>
                        </template>
                    </div>
                </div>
                <div id="lowerBodyArea" class="d-flex flex-column">
                    <div class="d-flex">
                        <div
                            class="equipmentWrapper"
                            style="margin-top: -6rem;"
                        >
                            <v-icon
                                id="leftHandIcon"
                                :style="{ color: glovesColor }"
                                >mdi-hand</v-icon
                            >
                            <template v-if="glovesFound != null">
                                <v-icon class="lime--text" v-if="glovesFound"
                                    >mdi-check</v-icon
                                >
                                <v-icon class="red--text" v-else
                                    >mdi-close</v-icon
                                >
                            </template>
                        </div>
                        <div class="equipmentWrapper">
                            <v-icon id="pantsIcon" :style="{ fill: pantsColor }"
                                >$pantsIcon</v-icon
                            >
                            <template v-if="pantsFound != null">
                                <v-icon class="lime--text" v-if="pantsFound"
                                    >mdi-check</v-icon
                                >
                                <v-icon class="red--text" v-else
                                    >mdi-close</v-icon
                                >
                            </template>
                        </div>
                        <div
                            class="equipmentWrapper"
                            style="margin-top: -6rem;"
                        >
                            <v-icon
                                id="rightHandIcon"
                                :style="{ color: glovesColor }"
                                >mdi-hand</v-icon
                            >
                            <template v-if="glovesFound != null">
                                <v-icon class="lime--text" v-if="glovesFound"
                                    >mdi-check</v-icon
                                >
                                <v-icon class="red--text" v-else
                                    >mdi-close</v-icon
                                >
                            </template>
                        </div>
                    </div>
                    <div class="equipmentWrapper">
                        <v-icon id="bootsIcon" :style="{ fill: bootsColor }"
                            >$bootsIcon</v-icon
                        >
                        <template v-if="bootsFound != null">
                            <v-icon class="lime--text" v-if="bootsFound"
                                >mdi-check</v-icon
                            >
                            <v-icon class="red--text" v-else>mdi-close</v-icon>
                        </template>
                    </div>
                </div>
            </div> -->
            </div>
            <!--Displays the progress bar and the outcome of the detection-->
            <!-- <div
            id="progressBarWrapper"
            class="justify-center"
            ref="progressBarWrapper"
            :style="{ display: showProgressBarPanel }"
        >
            <div id="progressBarPanel">
                <div class="pt-3 pb-2 text-center">
                    <span
                        class="font-weight-light align-start"
                        :class="textColor"
                        >{{ progressText }}</span
                    >
                </div>
                <div style="width: 50%; float: left;">
                    <progress-bar
                        :bg-color="progressColor"
                        bar-color="#333333"
                        :val="progressValue"
                        size="small"
                    ></progress-bar>
                </div>
                <div style="width: 50%; float: left; transform:scaleX(-1)">
                    <progress-bar
                        :bg-color="progressColor"
                        bar-color="#333333"
                        :val="progressValue"
                        size="small"
                    ></progress-bar>
                </div>
            </div>
        </div> -->
            <!-- Displays the equipment detection results in text form to make the app more accessible for the color blind-->
            <!-- <div
            id="colorBlindAssistPanelWrapper"
            ref="colorBlindAssistPanelWrapper"
            class="align-center"
            :style="{ display: showColorBlindAssistPanel }"
        >
            <div
                id="colorBlindAssistPanel"
                class="pl-10 pr-10 d-flex flex-column justify-end"
            >
                <v-simple-table class="py-2">
                    <template v-slot:default>
                        <thead>
                            <tr>
                                <th class="text-left white--text cbaHeader">
                                    Equipment
                                </th>
                                <th class="text-left white--text cbaHeader">
                                    Status
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, i) in itemStatusList" :key="i">
                                <td
                                    class="text-left cbaContent py-3 pr-10"
                                    :class="item.color"
                                >
                                    {{ item.name }}
                                </td>
                                <td>
                                    <v-icon
                                        v-if="item.status"
                                        class="lime--text"
                                        large
                                        >mdi-check</v-icon
                                    >
                                    <v-icon v-else class="red--text" large
                                        >mdi-close</v-icon
                                    >
                                </td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </div>-->
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import PersonDetectionLoader from '@/components/detection_process/loaders/PersonDetectionLoader';
import TickIconLoader from '@/components/detection_process/loaders/TickIconLoader';
import ProgressBar from 'vue-simple-progress';

import { EventBus } from '../../main.js'; // line added by Lina

export default {
    name: 'ResultsDisplay',

    components: {
        PersonDetectionLoader,
        TickIconLoader,
        ProgressBar
    },

    data() {
        return {
            items: [],
            itemsPopulated: false,

            personLoaderComponent: PersonDetectionLoader,
            tickLoaderComponent: null,

            showPersonResultsPanel: 'none',
            personDetectedText: 'No Person Found',

            showEquipmentResultsPanel: 'none',

            showProgressBarPanel: 'none',
            textColor: 'white--text',

            showColorBlindAssistPanel: 'none',
            itemStatusList: null,

            //Used to change color of icons
            hardHatColor: '',
            gogglesColor: '',
            shirtColor: '',
            glovesColor: '',
            pantsColor: '',
            bootsColor: '',

            //Used to set tick or cross
            hardHatFound: null,
            gogglesFound: null,
            shirtFound: null,
            glovesFound: null,
            pantsFound: null,
            bootsFound: null,

            //  Lina added

            personData: [], //added
            resultsCount: 0, //added - for use in HTML to provide unique ID for each result
            // personIndex: 0, //commented out
            timeRecorded: '', //for storing the time that the result is recorded
            personImage: '',
            hardHatStatus: null,
            gloveStatus: null,
            imagePersonDetected: ''

            // End of Lina added
        };
    },

    props: [
        'togglePersonResultsPanel',
        'toggleEquipmentResultsPanel',
        'toggleProgressBarPanel',
        'toggleColorBlindAssistPanel',
        'personDetected',
        'multipleDetected',
        'itemList',
        'progressValue',
        'progressText',
        'progressColor',
        'detectedItems'
    ],

    watch: {
        togglePersonResultsPanel: function() {
            console.log('toggle person results emitted');
            if (this.togglePersonResultsPanel) {
                this.showPersonResultsPanel = 'flex';
                this.$refs.personPanelWrapper.classList.add('slideInFromLeft');

                //Reset colors for icons in equipment panel to white
                console.log(
                    '-----------------------itemList: ' +
                        JSON.stringify(this.itemList)
                );
                for (let i = 0; i < this.itemList.length; i++) {
                    switch (this.itemList[i].name) {
                        case 'Hard hat':
                            this.hardHatColor = '#BDBDBD';
                            break;
                        case 'Gloves':
                            this.glovesColor = '#BDBDBD';
                            break;
                    }
                }
            } else {
                this.$refs.personPanelWrapper.classList.remove(
                    'slideInFromLeft'
                );
                this.showPersonResultsPanel = 'none';
            }
        },
        personDetected: function() {
            if (this.personDetected) {
                this.tickLoaderComponent = TickIconLoader;
                this.personDetectedText = 'Person Found';
                setTimeout(() => {
                    this.$refs.personPanelWrapper.classList.remove(
                        'slideInFromLeft'
                    );
                }, 2000);
            } else {
                this.tickLoaderComponent = null;
                this.personDetectedText = 'No Person Found';
            }
        },
        multipleDetected: function() {
            if (!this.personDetected)
                this.personDetectedText = this.multipleDetected
                    ? 'Too Many People'
                    : 'No Person Found';
        },
        toggleEquipmentResultsPanel: function() {
            if (this.toggleEquipmentResultsPanel) {
                //Reset
                this.hardHatFound = null;
                this.gogglesFound = null;
                this.shirtFound = null;
                this.glovesFound = null;
                this.pantsFound = null;
                this.bootsFound = null;

                this.showEquipmentResultsPanel = 'flex';

                //commented out
                // this.$refs.equipmentPanelWrapper.classList.add(
                //     'slideInFromRight'
                // );
                //end of commented out
            }
            //commented out
            // else {
            //     //commented out
            //     // this.$refs.equipmentPanelWrapper.classList.remove(
            //     //     'slideInFromRight'
            //     // );
            //     //end of commented out
            //     // setTimeout(() => {
            //     //     this.showEquipmentResultsPanel = 'none';
            //     // }, 1000);
            //     this.showEquipmentResultsPanel = 'flex';
            // }
            //end of commented out
        },
        // toggleProgressBarPanel: function() {
        //     if (this.toggleProgressBarPanel) {
        //         this.showProgressBarPanel = 'flex';
        //         this.$refs.progressBarWrapper.classList.add('slideInFromTop');
        //     } else {
        //         this.$refs.progressBarWrapper.classList.remove(
        //             'slideInFromTop'
        //         );
        //         setTimeout(() => {
        //             this.textColor = 'white--text';
        //             this.showProgressBarPanel = 'none';
        //         }, 1000);
        //     }
        // },
        // toggleColorBlindAssistPanel: function() {
        //     if (this.toggleColorBlindAssistPanel) {
        //         this.showColorBlindAssistPanel = 'flex';
        //         this.$refs.colorBlindAssistPanelWrapper.classList.add(
        //             'slideInFromLeft'
        //         );
        //     } else {
        //         this.$refs.colorBlindAssistPanelWrapper.classList.remove(
        //             'slideInFromLeft'
        //         );
        //         setTimeout(() => {
        //             this.itemStatusList = null;
        //             this.showColorBlindAssistPanel = 'none';
        //         }, 1000);
        //     }
        // },
        detectedItems: function() {
            if (this.detectedItems != null) {
                console.log(
                    '------------------detectedItems: ' +
                        JSON.stringify(this.detectedItems)
                );

                var newItemList = [...this.itemList];

                if (newItemList.length > this.detectedItems.length) {
                    this.textColor = 'red--text';
                } else {
                    this.textColor = 'lime--text';
                }

                //For each item in itemList
                for (let i = 0; i < newItemList.length; i++) {
                    //If detectedItems is not empty
                    if (this.detectedItems.length > 0) {
                        //Item was detected
                        if (
                            this.findIndexByAttr(
                                this.detectedItems,
                                'equipment',
                                newItemList[i].id.toString()
                            ) != -1
                        ) {
                            this.showResult(newItemList[i].name, true);
                            newItemList[i].status = true;
                            newItemList[i].color = 'lime--text';
                        } else {
                            //Item was not detected
                            this.showResult(newItemList[i].name, false);
                            newItemList[i].status = false;
                            newItemList[i].color = 'red--text';
                        }
                    } else {
                        //No items were detected, all items are missing
                        this.showResult(newItemList[i].name, false);
                        newItemList[i].status = false;
                        newItemList[i].color = 'red--text';
                    }
                }

                this.itemStatusList = newItemList;

                this.hardHatStatus = null;
                this.glovesStatus = null;
            }
        },
        progressColor: function() {
            if (this.progressColor === '#F44336') {
                this.textColor = 'red--text';
            }
        },
        progressText: function() {
            if (this.progressText.includes('relax')) {
                this.textColor = 'white--text';
            }
        }
    },

    methods: {
        showResult(equipment_name, is_detected) {
            console.log('changeItemColor: true');

            switch (equipment_name) {
                case 'Hard hat':
                    this.hardHatFound = is_detected;
                    break;
                case 'Gloves':
                    this.glovesFound = is_detected;
                    break;
            }
        },

        //Find index of object in array based on the object's attribute value
        findIndexByAttr(array, attr, value) {
            for (var i = 0; i < array.length; i++) {
                if (array[i][attr] === value) {
                    return i;
                }
            }
            return -1;
        },

        //added
        viewImg(resultsCount) {
            //loop through all results in this.personData, find the result number
            for (var i = 0; i < this.personData.length; i++) {
                if (this.personData[i].resultsCount == resultsCount) {
                    //once result number is found,
                    this.personData[i].overlay = true; //show overlay for image of the result
                }
            }
            this.zIndex = 51; //this is to allow the overlay be at the top most layer of the HTML
        },

        checkNonCompliance(results) {
            //change colour of detection dot
            var tempResults = 0; //temporary variable to check if all results are compliant
            for (var i = 0; i < results.length; i++) {
                //check if there is any non-compliance
                if (results[i].hardHatStatus == false) {
                    //if there is non-compliance
                    this.$parent.nonComplianceDetected(true); //change the colour of the detection dot to red (emits function in SimpleDetection.vue)
                } else {
                    tempResults += 1; //if current result is compliant, add 1 to temp var
                }
            }
            if (tempResults == 7) {
                //if all results are compliant, change detection dot colour back to green
                this.$parent.nonComplianceDetected(false); //
            }
        }
        //end of added
    }, // end methods

    created() {
        console.log('arrived at CREATED results display');
        EventBus.$on('person-image', getTempData => {
            console.log('in CREATED results display!');
            // 3 items in getTempData [0]: base64imagestr, [1]: true/fasle, [2]: 13/14, [3]: personcoords
            // console.log(getTempData);

            for (let count = 0; count < getTempData.length; count++) {
                // Get hardhat detection results
                var hardHatDetection;
                if (getTempData[count][1] && getTempData[count][2] == 14) {
                    console.log(
                        'detection result',
                        getTempData[count][1],
                        '+',
                        getTempData[count][2] == 14
                    );
                    hardHatDetection = true;
                } else {
                    hardHatDetection = false;
                }

                //dimensions to crop person image by
                //width, height, x coord to start from (left), y coord to start from (top)
                var personDimensions = [
                    getTempData[count][3][2] - getTempData[count][3][0],
                    getTempData[count][3][3] - getTempData[count][3][1],
                    getTempData[count][3][0],
                    getTempData[count][3][1]
                ];

                // Get base64imageStr of person
                this.imagePersonDetected = getTempData[count][0];
                this.resultsCount += 1; //added, used to count results

                var my_object = {
                    // personIndex : count + 1,
                    timeRecorded: new Date().toLocaleTimeString(), //get current time
                    hardHatStatus: hardHatDetection,
                    // gloveStatus : this.glovesFound,
                    personImage: this.imagePersonDetected,
                    personDims: personDimensions,
                    resultsCount: this.resultsCount,
                    overlay: false
                };

                //added
                if (this.personData.length >= 7) {
                    this.personData.splice(this.personData.length - 1, 1); //start at index 0, remove 1 element (removes oldest element)
                }

                this.personData.unshift(my_object); //unshift() adds to beginning of array
            } // end for

            this.checkNonCompliance(this.personData); //added
        }); // end EventBus
    }
};
</script>

<style>
#personPanelWrapper {
    height: 100%;
    position: absolute;
    left: 0;
    display: none;
    animation: slideOutToLeft ease-in-out 1s;
    animation-fill-mode: forwards;
}

#personPanelWrapper.slideInFromLeft {
    animation: slideInFromLeft ease-in-out 1s;
    animation-fill-mode: forwards;
}

#personPanel {
    background: rgba(0, 0, 0, 0.7);
}

#personPanel span {
    font-size: 2rem;
}

#personLoaderWrapper {
    width: 100px;
    height: 100px;
    position: relative;
}

.loaderPos {
    position: absolute;
    left: 0;
    top: 0;
}

#equipmentPanelWrapper {
    height: 100%;
    width: 23%;
    position: absolute;
    right: 0;
    /* display: show; */
    /* commented out */
    /* animation: slideOutToRight ease-in-out 1s;
    animation-fill-mode: forwards; */
    /* end of commented out */
}

#equipmentPanelWrapper.slideInFromRight {
    animation: slideInFromRight ease-in-out 1s;
    animation-fill-mode: forwards;
}

#equipmentPanel {
    /* background: rgba(0, 0, 0, 0.7); */
    height: 80%;
    width: 100%;
    position: absolute;
    top: 1%;
    right: 2%;
}

#equipmentPanel span {
    font-size: 1.5rem;
}

#equipmentPanel .v-icon {
    fill: rgba(150, 150, 150, 0.1);
    color: rgba(150, 150, 150, 0.1);
}

#progressBarWrapper {
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    display: none;
    animation: slideOutToTop ease-in-out 1s;
    animation-fill-mode: forwards;
}

#progressBarWrapper.slideInFromTop {
    animation: slideInFromTop ease-in-out 1s;
    animation-fill-mode: forwards;
}

#progressBarPanel {
    background: rgba(0, 0, 0, 0.7);
    width: 30%;
    position: absolute;
}

#progressBarPanel span {
    font-size: 2rem;
}
/*
#colorBlindAssistPanelWrapper {
    height: 100%;
    position: absolute;
    left: 0;
    display: none;
    animation: slideOutToLeft ease-in-out 1s;
    animation-fill-mode: forwards;
}

#colorBlindAssistPanelWrapper.slideInFromLeft {
    animation: slideInFromLeft ease-in-out 1s;
    animation-fill-mode: forwards;
}

#colorBlindAssistPanel {
    background: rgba(0, 0, 0, 0.7);
}

#colorBlindAssistPanel .v-data-table {
    background: none;
}

.cbaHeader {
    font-size: 1.1rem !important;
}

.cbaContent {
    font-size: 1.5rem !important;
}

#colorBlindAssistPanel
    .v-data-table
    > .v-data-table__wrapper
    > table
    > tbody
    > tr:not(:last-child)
    > td:not(.v-data-table__mobile-row),
#colorBlindAssistPanel
    .v-data-table
    > .v-data-table__wrapper
    > table
    > thead
    > tr:last-child
    > th {
    border-bottom-color: rgba(0, 0, 0, 0) !important;
}  */

/* Icon size styles */
#hardHatIcon {
    font-size: 8rem;
}

#gogglesIcon {
    font-size: 6rem;
    margin-top: -2rem;
}

#shirtIcon {
    font-size: 13rem;
    width: 1em;
    height: 1em;
}

#leftHandIcon {
    transform: scaleY(-1);
    font-size: 6rem;
}

#pantsIcon {
    font-size: 13rem;
    width: 1em;
    height: 1em;
}

#rightHandIcon {
    transform: scale(-1, -1);
    font-size: 6rem;
}

#bootsIcon {
    font-size: 10rem;
    width: 1em;
    height: 1em;
    margin-top: -2rem;
}

#headArea,
#upperBodyArea,
#lowerBodyArea {
    justify-content: center;
    align-items: center;
    height: 100%;
}

.equipmentWrapper {
    display: inline-block;
    width: 100%;
    height: 100%;
    overflow: hidden;
    /* position: relative; */
}

.equipmentWrapper
    .v-icon:not(#hardHatIcon):not(#gogglesIcon):not(#shirtIcon):not(#leftHandIcon):not(#rightHandIcon):not(#pantsIcon):not(#bootsIcon) {
    font-size: 7rem;
    position: relative; /* original value = absolute */
    width: 80%; /* original value = 100% */
    height: 80%; /* original value = 100% */
}

.imageWrapper {
    position: relative;
}

/* Slide in and out from left */
@-webkit-keyframes slideInFromLeft {
    0% {
        left: -500px;
    }

    100% {
        left: 0;
    }
}

@keyframes slideInFromLeft {
    0% {
        left: -500px;
    }

    100% {
        left: 0;
    }
}

@-webkit-keyframes slideOutToLeft {
    0% {
        left: 0;
    }

    100% {
        left: -500px;
    }
}

@keyframes slideOutToLeft {
    0% {
        left: 0;
    }

    100% {
        left: -500px;
    }
}

/* Slide in and out from right */
@-webkit-keyframes slideInFromRight {
    0% {
        right: -500px;
    }

    100% {
        right: 0;
    }
}

@keyframes slideInFromRight {
    0% {
        right: -500px;
    }

    100% {
        right: 0;
    }
}

@-webkit-keyframes slideOutToRight {
    0% {
        right: 0;
    }

    100% {
        right: -500px;
    }
}

@keyframes slideOutToRight {
    0% {
        right: 0;
    }

    100% {
        right: -500px;
    }
}

/* Slide in and out from top */
@-webkit-keyframes slideInFromTop {
    0% {
        top: -250px;
    }

    100% {
        top: 0;
    }
}

@keyframes slideInFromTop {
    0% {
        top: -250px;
    }

    100% {
        top: 0;
    }
}

@-webkit-keyframes slideOutToTop {
    0% {
        top: 0;
    }

    100% {
        top: -250px;
    }
}

@keyframes slideOutToTop {
    0% {
        top: 0;
    }

    100% {
        top: -250px;
    }
}

/* My edits from here */

table {
    /* position: absolute;
    top: 0;
    right: 0; */
    font-family: 'Open Sans', sans-serif;
    width: 100%;
    border-collapse: collapse;
    border: 10px solid #44475c;
    table-layout: fixed;
    position: relative;
}

table th {
    text-transform: uppercase;
    text-align: center;
    background: #44475c;
    color: #fff;
    padding: 15px;
    /* min-width: 30px; */
}

table tr {
    text-align: center;
    padding: 10px;
    /* border-right: 5px solid #7D82A8; */
    font-weight: bold;
    /* font-size: large; */
    color: #000;
    background: #adabab;
}
/* table td:last-child {
    border-right: none;
} */
table tbody tr:nth-child(2n) td {
    /* styling for even rows */
    background: #3c3c3c;
    color: #fff;
}
</style>
