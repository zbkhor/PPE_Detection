<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <v-container id="outerContainer" class="d-flex" style="height:100%;">
        <v-snackbar
            v-model="snackbar"
            :timeout="4000"
            :color="snackbarColor"
            top
            right
        >
            <span class="pr-4">{{ snackbarMessage }}</span>
            <v-btn class="ma-0" @click="closeSnackbar" text>Close</v-btn>
        </v-snackbar>
        <v-row>
            <!--START - Resolution and Media Settings-->
            <v-col cols="4" id="settings">
                <!-- Resolution Selection -->
                <resolution-selection
                    ref="resolutionSelection"
                    @constraintsReceived="changeVideoRes"
                ></resolution-selection>
                <v-divider class="grey"></v-divider>
                <!-- Media Source Selection -->
                <media-selection
                    ref="mediaSelection"
                    @mediaReceived="changeMediaSource"
                    :devices="devices"
                ></media-selection>
            </v-col>
            <!--END - Resolution and Media Settings-->
            <!--START - Camera Display and Controls-->
            <v-col class="px-5">
                <!--START - Camera Display-->
                <v-row class="py-5">
                    <v-col >
                        <div id="cameraDisplay">
                            <fullscreen
                                ref="fullscreen"
                                @change="fullscreenChange"
                                class="d-flex"
                            >
                                <!--Detection component-->
                                <div v-if="fullscreen"><tf2 class='d-flex'
                                    ref="tf2"
                                    @getDevices="findDevices"
                                    @constraintError="displayError"
                                    :constraints="videoConstraints"
                                    :media="mediaSources"
                                    :fullscreenTrigger="fullscreen"
                                    :flipHorizontally="flipHorizontally"
                                    :flipVertically="flipVertically"
                                ></tf2></div>
                                <div v-else><preset class='d-flex'
                                    ref="preset"
                                    @getDevices="findDevices"
                                    @constraintError="displayError"
                                    :constraints="videoConstraints"
                                    :media="mediaSources"
                                    :fullscreenTrigger="fullscreen"
                                    :flipHorizontally="flipHorizontally"
                                    :flipVertically="flipVertically"
                                ></preset></div>
                            </fullscreen>
                        </div>
                    </v-col>
                </v-row>
                <!--END - Camera Display-->
                <!--START - Camera Controls-->
                <v-row class="pb-6">
                    <v-col>
                        <div class="d-flex justify-center" id="cameraControls">
                            <v-btn
                                @click="toggle"
                                color="blue darken-3 white--text"
                            >
                                <v-icon>mdi-fullscreen</v-icon>
                                Fullscreen
                            </v-btn>
                            <!-- <v-btn
                                @click="toggleHorizontalFlip"
                                color="lime darken-4 white--text"
                            >
                                <v-icon>mdi-flip-horizontal</v-icon>
                                Flip Horizontally
                            </v-btn>
                            <v-btn
                                @click="toggleVerticalFlip"
                                color="lime darken-4 white--text"
                            >
                                <v-icon>mdi-flip-vertical</v-icon>
                                Flip Vertically
                            </v-btn> -->
                        </div>
                    </v-col>
                </v-row>
                <!--END - Camera Controls-->
            </v-col>
            <!--END - Camera Display and Controls-->
        </v-row>
    </v-container>
</template>

<script>
//import packages and components
//npm packages
// import Fullscreen from 'vue-fullscreen/src/component.vue';
import fullscreen from 'vue-fullscreen';
import axios from 'axios';

//vue components
import ResolutionSelection from '@/components/console/ResolutionSelection';
import MediaSelection from '@/components/console/MediaSelection';
import Vue from 'vue'
import SimpleDetection from '@/components/detection_process/SimpleDetection';
import tf2 from '@/components/detection_process/tf2'
import preset from '@/components/detection_process/preset'
Vue.use(fullscreen)
export default {
    name: 'Home',

    components: {
        ResolutionSelection,
        MediaSelection,
        tf2,
        preset
    },

    data() {
        return {
            captures: [],

            fullscreen: false,

            videoConstraints: null,
            mediaSources: null,
            devices: null,

            flipHorizontally: false,
            flipVertically: false,

            snackbar: false,
            snackbarColor: 'info',
            snackbarMessage: ''
        };
    },

    methods: {
        //Change video resolution
        changeVideoRes(constraints) {
            this.videoConstraints = constraints;
        },

        //Change media sources
        changeMediaSource(media) {
            this.mediaSources = media;
        },

        //Refresh media sources
        findDevices(deviceInfos) {
            this.devices = deviceInfos;
        },

        //Change fullscreen
        fullscreenChange(fullscreen) {
            this.fullscreen = fullscreen;
        },

        //Toggle fullscreen
       toggle () {
        this.$refs['fullscreen'].toggle()

         // recommended
        // this.fullscreen = !this.fullscreen // deprecated
      },
      fullscreenChange (fullscreen) {
        this.fullscreen = fullscreen
      },
  


        //Flip camera horizontally
        toggleHorizontalFlip() {
            this.flipHorizontally = !this.flipHorizontally;
        },

        //Flip camera vertically
        toggleVerticalFlip() {
            this.flipVertically = !this.flipVertically;
        },

        //Display error in snackbar
        displayError(errorMessage) {
            this.snackbarColor = 'error';
            this.snackbarMessage = errorMessage;
            this.snackbar = true;
        },

        //Close snackbar
        closeSnackbar() {
            this.snackbar = false;
        }
    }
};
</script>

<style>
.row,
.col {
    margin: 0 !important;
    padding: 0 !important;
}

#cameraControls .v-btn {
    flex: 1 1 20%;
    margin: 8px 16px 0 16px;
}

#cameraControls .v-btn:first-child {
    margin-right: 10%;
    flex-basis: 30%;
}

#outerContainer {
    max-width: 100% !important;
    padding: 0px !important;
}

#settings {
    display: flex;
    flex-direction: column;
    box-shadow: 3px 0px 3px -2px #ccc;
}

#resolutionText,
#mediaText {
    font-size: 1.2rem !important;
    line-height: normal;
    text-align: left;
}

#resolutionListItems {
    padding: 0 !important;
}

div.select {
    display: inline-block;
    margin: 0 0 1em 0;
}

label {
    width: 12em;
    display: inline-block;
}

html {
    overflow-y: unset !important;
    box-sizing: unset !important;
}

.fullscreen {
    margin: 0 auto;
    display: inline;
    position: relative;
    /* bottom:500px;
    left:500px; */
    justify-content: center;
    align-items: center;
}
div.model{
    display: block !important;
    position:relative;
    /* bottom: 500px;
    left: 100px; */
    /* max-height:100%; */
    /* max-width: 100%;  */
    margin: 0 auto;
    overflow: auto;
  
}
.v-application--wrap {
    min-height: unset !important;
}

#app {
    text-align: center;
    color: #2c3e50;
    margin-top: 64px;
}

#video {
    background-color: #000000;
    display: block !important;
    object-fit: cover;
    height: 100%;
    max-width: 100%;
    margin: 0 auto;
}



#videoContainer {
    margin: 0 auto;
    display: inline-block;
    position: relative;
    height: 100%;

    justify-content: center;
}

li {
    display: inline;
    padding: 5px;
}

div#buttons {
    margin: 0 0 1em 0;
}

.v-list-item {
    flex: unset !important;
    flex-wrap: wrap;
}

.v-list-item button {
    margin: 10px;
    flex: 1 0 auto;
}

#cameraDisplay > div {
    height: 80vh;

}


.v-text-field.v-text-field--enclosed:not(.v-text-field--rounded)
    > .v-input__control
    > .v-input__slot,
.v-text-field.v-text-field--enclosed .v-text-field__details {
    padding: 0 !important;
}

.v-label {
    padding: 0 0 0 16px;
}

.v-select__selection {
    padding: 0 0 0 12px;
}

/* Detection interface styles */
#snap {
    position: absolute;
    margin-left: auto;
    margin-right: auto;
    left: 0;
    right: 0;
    bottom: 25px;
    text-align: center;
    background: royalblue;
    padding: 10px 20px;
    color: #ffffff !important;
    z-index: 2;
}

.componentOuterBox {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
}

#detectionMethodBtn {
    flex-basis: 15% !important;
}



</style>
