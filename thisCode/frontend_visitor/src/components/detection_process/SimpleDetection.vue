<!-- 
    Author: Wang Wei Liang Matthew 
    Date Written: 10/08/2020
-->
<template>
    <div id="videoContainer" ref="videoContainer">
        <!-- Camera feed -->
        <video
            ref="video"
            id="video"
            :class="{ flipX: isFlipX, flipY: isFlipY, flipXY: isFlipXY }"
            autoplay
        ></video>
        <!-- Dynamically load the different screens used in the detection process -->
        <!-- <component
            :is="startComponent"
            ref="startComponent"
            @startScreenTapped="launchGuide"
        ></component> -->
        <!-- Used to provide information for the user through text-to-speech messages and subtitles -->
        <component
            :is="guideComponent"
            ref="guideComponent"
            @detectPerson="checkForPerson"
            @detectEquipment="checkEquipment"
            @endDetection="returnToStart"
            :guideTrigger="guideTrigger"
        ></component>
        <span id="dot" ref="detectionDot"></span>
        <!--Canvas for boundary boxes (Detected areas) -->
        <canvas
            id="boundaryBoxCanvas"
            ref="boundaryBoxCanvas"
            class="drawingArea"
        ></canvas>
        <canvas
            id="canvas"
            ref="canvas"
            class="drawingArea"
            style="display:none;"
        ></canvas>
        <!--Display used to show ppe detection results-->
        <!-- lina edit -->
        <component
            :is="resultsComponent"
            ref="resultsComponent"
            :detectedItems="detectedItems"
            :itemList="itemList"
            :toggleEquipmentResultsPanel="toggleEquipmentResultsPanel"
        ></component>
        <!--    :personDetected="personDetected"
                :togglePersonResultsPanel="togglePersonResultsPanel"
        commented out -->

        <!-- end of lina edit -->
        <!-- <component
            :is="resultsComponent"
            ref="resultsComponent"
            :detectedItems="detectedItems"
            :itemList="itemList"
            :personDetected="personDetected"
            :multipleDetected="multipleDetected"
            :progressValue="progressValue"
            :progressColor="progressColor"
            :progressText="progressText"
            :togglePersonResultsPanel="togglePersonResultsPanel"
            :toggleEquipmentResultsPanel="toggleEquipmentResultsPanel"
            :toggleProgressBarPanel="toggleProgressBarPanel"
            :toggleColorBlindAssistPanel="toggleColorBlindAssistPanel"
        ></component> -->
        <!-- Display detection loader -->
        <!-- <component :is="loaderComponent" ref="loaderComponent"></component> -->
        <!-- Used to return to the start screen-->
        <!-- <div id="cancelBtnWrapper" :style="{ display: cancelBtnDisplay }">
            <v-btn
                id="cancelBtn"
                class="white--text blue"
                @click="returnToStart"
                x-large
            >
                <v-icon class="mr-4">mdi-home</v-icon>
                <span>Return To Start</span>
            </v-btn>
        </div> -->
    </div>
</template>

<script>
import adapter from 'webrtc-adapter';
import axios from 'axios';
import StartScreen from '@/components/detection_process/StartScreen';
import DetectionGuide from '@/components/detection_process/DetectionGuide';
import ResultsDisplay from '@/components/detection_process/ResultsDisplay';
import Loader from '@/components/detection_process/Loader';

import { EventBus } from '../../main.js';

export default {
    name: 'SimpleDetection',
    components: {
        StartScreen,
        DetectionGuide,
        ResultsDisplay,
        Loader
    },
    data() {
        return {
            canvas: null,
            video: null,
            track: null,
            stream: null,
            //Default constraints video will use on startup, set to highest resolution supported
            defaultConstraints: {
                video: {
                    width: { ideal: 4096 },
                    height: { ideal: 2160 },
                    frameRate: { ideal: 30 }
                }
            },
            currentAudioInput: null,
            currentVideoSource: null,
            checkForObjects: false,
            guideTrigger: null,
            // startComponent: null, //commented out
            guideComponent: null,
            resultsComponent: null,
            loaderComponent: null,
            xPos: null,
            yPos: null,
            rectWidth: null,
            rectHeight: null,
            isFlipX: false,
            isFlipY: false,
            isFlipXY: false,
            togglePersonResultsPanel: false,
            personDetected: false,
            multipleDetected: false,
            checkingEquipment: false,
            toggleEquipmentResultsPanel: true,
            detectedItems: null,
            toggleProgressBarPanel: false,
            progressValue: 0,
            progressText: 'Detecting...',
            progressColor: '#CDDC39',
            toggleColorBlindAssistPanel: false,
            itemList: null,
            errorCount: 0,
            cancelBtnDisplay: 'none',
            returningToStart: false,

            //testing
            resultsforDisplay: [],
            currentNoOfResults: 0,

            //  My edits from here
            numPersonDetected: 0,
            imageStr: '',
            personCoordinates: [],

            //commented out
            // left: [],
            // top: [],
            // right: [],
            // bottom: [],
            //end of commented out
            allCoord: null
        };
    },
    //Data form parent components (from Home.vue)
    props: [
        'constraints',
        'media',
        'flipHorizontally',
        'flipVertically',
        'fullscreenTrigger'
    ],
    //Watch for changes in props data
    watch: {
        constraints: function() {
            console.log(':watch:constraints: true');
            this.getMedia(this.constraints);
        },
        media: function() {
            console.log('watch:media: true');
            this.currentVideoSource = this.media[0];
            this.getMedia(this.defaultConstraints);
        },
        flipHorizontally: function() {
            this.isFlipXY = false;
            this.isFlipX = !this.isFlipX;
            if (this.isFlipX && this.isFlipY) {
                this.isFlipXY = true;
            }
        },
        flipVertically: function() {
            this.isFlipXY = false;
            this.isFlipY = !this.isFlipY;
            if (this.isFlipX && this.isFlipY) {
                this.isFlipXY = true;
            }
        },
        fullscreenTrigger: function() {
            console.log('watch:fullscreenTrigger: true');
            if (this.fullscreenTrigger) {
                this.$refs.videoContainer.style.setProperty(
                    'width',
                    '100%',
                    'important'
                );
                //Load components used in detection process
                // this.startComponent = StartScreen; //commented out
                this.guideComponent = DetectionGuide;
                this.resultsComponent = ResultsDisplay;
                //Box coordinates calculation
                // this.xPos = Math.round(
                //     this.video.videoWidth / 2 - this.video.videoWidth / 6
                // );
                // this.yPos = 20;
                // this.rectWidth = Math.round((this.video.videoWidth / 6) * 2);
                // this.rectHeight = Math.round(
                //     this.video.videoHeight - this.yPos * 2
                // );

                // Lina edit

                // Remove box coordinates
                this.xPos = 1;
                this.yPos = 1;
                this.rectWidth = this.video.videoWidth - 1;
                this.rectHeight = this.video.videoHeight - 1;
                // end of Lina edit

                this.launchGuide(); //added by xy
                this.checkForPerson(); //added by xy
                setTimeout(() => {
                    this.checkEquipment();
                }, 500);
                // this.checkEquipment(); //added by xy
            } else {
                this.$refs.videoContainer.style.setProperty(
                    'width',
                    'inherit',
                    'important'
                );
                /* Reset everything */
                //Clear all utterances
                this.clearAllSpeeches();
                //Unload components used in detection process
                // this.startComponent = null; //commented out
                this.guideComponent = null;
                this.resultsComponent = ResultsDisplay;
                this.loaderComponent = null;
                //Clear canvas drawings
                var bCanvas = this.$refs.boundaryBoxCanvas;
                const ctx = bCanvas.getContext('2d');
                ctx.clearRect(0, 0, bCanvas.width, bCanvas.height);
                //Hide canvas
                this.canvas.style.display = 'none';
                //Reset detection process variables
                this.guideTrigger = null;
                this.checkForObjects = false;
                this.errorCount = 0;
                this.togglePersonResultsPanel = false;
                this.personDetected = false;
                this.multipleDetected = false;
                this.checkingEquipment = false;
                this.detectedItems = null;
                this.toggleEquipmentResultsPanel = true;
                // this.toggleEquipmentResultsPanel = false;
                this.toggleProgressBarPanel = false;
                this.progressValue = 0;
                this.progressColor = '#CDDC39';
                this.progressText = 'Logging result'; // original value 'Detecting...'
                this.toggleColorBlindAssistPanel = false;
                this.cancelBtnDisplay = 'none';
                this.returningToStart = false;
                //Update item list for detection
                this.setItemListForDetection();
            }
        }
    },
    async mounted() {
        this.canvas = this.$refs.canvas;
        this.video = this.$refs.video;
        //Load item list for detection
        this.setItemListForDetection();
        await navigator.mediaDevices
            .enumerateDevices()
            .then(deviceInfos => {
                this.$emit('getDevices', deviceInfos);
            })
            .catch(this.handleError);
        this.getMedia(this.defaultConstraints);
        // setTimeout(() => {
        //     this.resultsforDisplay = [];
        // }, 120000);
    },
    methods: {
        //Get the list of items the system should detect
        setItemListForDetection() {
            console.log('setItemListForDetection: true');
            this.itemList = null;
            axios.get('/api/equipments').then(response => {
                var equipment = response.data.Success;
                axios
                    .get('/api/ppeselections/getselection')
                    .then(response => {
                        var myList = [];
                        var selectedEquipment =
                            response.data.Success.selectionEquipment;
                        for (let i = 0; i < selectedEquipment.length; i++) {
                            equipment.forEach(item => {
                                if (selectedEquipment[i] == item.id) {
                                    let myItem = {};
                                    myItem.id = item.id;
                                    myItem.name = item.equipmentName;
                                    myList.push(myItem);
                                }
                            });
                        }
                        return myList;
                    })
                    .then(data => {
                        this.itemList = data;
                    })
                    .catch(error => {
                        console.log(error);
                    });
            });
        },
        getMedia(constraints) {
            console.log('getMedia: true');

            //Clear video
            if (this.stream != null) {
                this.stream.getVideoTracks()[0].stop();

                this.video.srcObject = null;
            }

            //Add media source to use to resolution constraints
            const videoSource = this.currentVideoSource;

            constraints.video.deviceId = videoSource
                ? { exact: videoSource }
                : undefined;

            navigator.mediaDevices
                .getUserMedia(constraints)
                .then(this.gotStream)
                .then(deviceInfos => {
                    this.$emit('getDevices', deviceInfos);
                })
                .then(this.resolveVideo)
                .catch(this.handleError);
        },

        //Assign the stream to the video element
        gotStream(mediaStream) {
            console.log('gotStream: true');
            this.stream = window.stream = mediaStream;
            this.video.srcObject = mediaStream;
            this.track = mediaStream.getVideoTracks()[0];
            return navigator.mediaDevices.enumerateDevices();
        },

        //Ensure that the video is playing
        resolveVideo() {
            console.log('resolveVideo: true');
            return new Promise(resolve => (this.video.onplaying = resolve));
        },

        //Error Handling
        handleError(error) {
            console.log(
                'navigator.MediaDevices.getUserMedia error: ',
                error.message,
                error.name
            );
            this.$emit(
                'constraintError',
                'This resolution is not supported by your device.'
            );
        },

        //added
        //changing detection dot colour
        nonComplianceDetected(nonCompliance) {
            if (nonCompliance == true) {
                this.$refs.detectionDot.style.setProperty(
                    //if there is 1 non-compliant result, set detection dot to red
                    'background-color',
                    'red'
                );
            } else {
                this.$refs.detectionDot.style.setProperty(
                    //if all detections are compliant, set detection dot to green
                    'background-color',
                    'green'
                );
            }
        },
        //end of added

        // Detection Process Methods
        launchGuide() {
            console.log('launchGuide: true');
            this.returningToStart = false;
            //Show person detection results panel
            // this.togglePersonResultsPanel = true; //commented out
            //Show equipment results panel
            // this.toggleEquipmentResultsPanel = true; //commented out
            //Show return to start button
            this.cancelBtnDisplay = 'block';

            // setTimeout(() => {
            //     // this.togglePersonResultsPanel = true;
            //     this.toggleEquipmentResultsPanel = true;
            // }, 100)

            //Draw rectangle on screen to indicate the area where user should be standing within
            var bCanvas = this.$refs.boundaryBoxCanvas;
            bCanvas.width = this.video.videoWidth;
            bCanvas.height = this.video.videoHeight;
            const ctx = bCanvas.getContext('2d');
            ctx.strokeStyle = 'rgba(255, 255, 0, 0.8)';
            ctx.lineWidth = 4;
            ctx.strokeRect(
                this.xPos,
                this.yPos,
                this.rectWidth,
                this.rectHeight
            );
            // this.startComponent = null; //commented out
            // this.guideTrigger = 1; //commented out
        },

        //Check if a person is standing within the yellow box
        checkForPerson() {
            console.log('checkForPerson: true');
            //Reset
            this.guideTrigger = null;
            this.checkingEquipment = false;
            this.checkForObjects = false;
            //Get form data to send to api
            var formData = this.prepareData(null, this.itemList);
            console.log('going to api - advObjDet');
            if (this.fullscreenTrigger) {
                axios({
                    method: 'post',
                    url: '/api/detection/advanceObjectDetection/',
                    data: formData,
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                    .then(response => {
                        //console.log(response.data);
                        //A person was detected within the box
                        if (response.data.humanDetections) {
                            // Lina added
                            // console.log('humanDetections from api: ' + response.data.humanDetections);
                            // console.log('detections from api: ');
                            // console.log(response.data.detections);  // [object Object]
                            // var answer = response.data.detections;

                            // console.log("answer[0].personcoords");
                            // console.log(answer[0].personcoords); // array with all personcoords
                            // console.log("num of people detected");
                            // console.log(answer[0].numofpersons);
                            // end of Lina added

                            console.log('A person was detected.');
                            //Hide person detection results panel
                            this.personDetected = true;
                            //this.multipleDetected = false;
                            //Plays second set of messages (Person detected -> Checking Equipment)
                            // sends to DetectionGuide.vue
                            // this.guideTrigger = 2;  // guideTrigger=2 : 'person found' ; commented out
                        } else {
                            //Check if multiple people were detected
                            // this.multipleDetected = response.data.errorMessage.includes(
                            //     'too many'
                            // )
                            //     ? true
                            //     : false;
                            //No person detected within the box
                            //Check again
                            if (!this.returningToStart) {
                                this.checkForPerson();
                            }
                        }
                    })
                    .catch(error => {
                        //log error and try again
                        console.log(JSON.stringify(error));
                        this.checkForPerson();
                    });
            }
        },

        // Lina added

        // crop image
        cropImage(formData, personcoordhh) {
            console.log('arrive at cropImage');
            formData.delete('top');
            formData.delete('left');
            formData.delete('width');
            formData.delete('height');
            var width = personcoordhh[2] - personcoordhh[0];
            var height = personcoordhh[3] - personcoordhh[1];

            formData.append('top', personcoordhh[1]);
            formData.append('left', personcoordhh[0]);
            formData.append('width', width);
            formData.append('height', height);

            // Display the key/value pairs
            // for (var pair of formData.entries()) {
            //     console.log(pair[0]+ ', ' + pair[1]);
            // }
            return formData;
        }, // end cropImage

        // draw boxes if no hardhat found
        drawBox(answerhh, numofpax) {
            console.log('drawBox true');

            //create arrays to store each person's coordinates
            var left = [];
            var top = [];
            var right = [];
            var bottom = [];

            for (let count = 0; count < numofpax; count++) {
                //loop through all person detections

                //get coordinates of current person and push into coordinates array
                left.push(answerhh[count].personcoords[0]);
                top.push(answerhh[count].personcoords[1]);
                right.push(answerhh[count].personcoords[2]);
                bottom.push(answerhh[count].personcoords[3]);

                // Draw boxes around person if no hardhat found
                var tempCanvas = this.$refs.boundaryBoxCanvas;
                tempCanvas.width = this.video.videoWidth;
                tempCanvas.height = this.video.videoHeight;
                const tempctx = tempCanvas.getContext('2d');
                tempctx.lineWidth = 4;

                // if(answerhh[count].detection){
                //     tempctx.strokeStyle = 'rgba(0, 255, 0, 0.8)'; // green colour;
                // } else {
                //     tempctx.strokeStyle = 'rgba(255, 0, 0, 0.8)'; // red colour;
                // }

                //draws the boundary box
                for (let count = 0; count < numofpax; count++) {
                    if (answerhh[count].detection) {
                        tempctx.strokeStyle = 'rgba(0, 255, 0, 0.8)'; // green colour;
                    } else {
                        tempctx.strokeStyle = 'rgba(255, 0, 0, 0.8)'; // red colour;
                    }
                    tempctx.strokeRect(
                        left[count],
                        top[count],
                        right[count] - left[count],
                        bottom[count] - top[count]
                    );
                }
            } //end for
        }, // end drawBox

        // draw boxes around each human found
        drawHumanBox(answerhh, numofpax) {
            console.log('drawHumanBox true');

            for (let count = 0; count < numofpax; count++) {
                // Get all the coordinates of person detected
                this.left.push(answerhh[count].personcoords[0]);
                this.top.push(answerhh[count].personcoords[1]);
                this.right.push(answerhh[count].personcoords[2]);
                this.bottom.push(answerhh[count].personcoords[3]);
                console.log('this.left is ' + this.left);

                // Draw boxes around person if no hardhat found
                var tempCanvas = this.$refs.boundaryBoxCanvas;
                tempCanvas.width = this.video.videoWidth;
                tempCanvas.height = this.video.videoHeight;
                const tempctx = tempCanvas.getContext('2d');
                tempctx.lineWidth = 4;
                tempctx.strokeStyle = 'rgba(0,0,0,0.8)'; // black colour

                for (let count = 0; count < numofpax; count++) {
                    console.log('am I drawing a box??');
                    tempctx.strokeRect(
                        this.left[count],
                        this.top[count],
                        this.right[count] - this.left[count],
                        this.bottom[count] - this.top[count]
                    );
                }
            } //end for
        }, // end drawHumanBox

        async updateForAxios(formData, answerhh, numofpax, successList) {
            console.log('updateForAxios: true');

            for (let count = 0; count < numofpax; count++) {
                let formData2 = new FormData();
                var personcoordhh = answerhh[count].personcoords;
                console.log('count = ' + count);
                // console.log(personcoordhh);
                formData2 = this.cropImage(formData, personcoordhh);
                formData2 = this.logResult(successList, formData2, count);
                // console.log('return from logResult');

                await axios({
                    method: 'post',
                    url: '/api/logs/',
                    data: formData2,
                    headers: { 'Content-Type': 'multipart/form-data' }
                })
                    .then(response => {
                        console.log(JSON.stringify(response));
                        console.log('back from axios, response: ' + count); // Lina added
                    })
                    .catch(error => {
                        console.log('error.response', error.response);
                        console.log(JSON.stringify(error));
                        console.log('back from axios, error: ' + count); // Lina added
                    });
            }
        }, // end async updateForAxios

        getCropBase64(imgStr) {
            // var indivResults = [];
            // // var startX = answerhh[count].personcoords[0];
            // // var startY = answerhh[count].personcoords[1];
            // // var endX = answerhh[count].personcoords[2];
            // // var endY = answerhh[count].personcoords[3];
            // // var width = endX - startX;
            // // var height = endY - startY;
            // // // console.log('printing coordinates');
            // // // console.log(startX, startY, endX, endY, width, height);
            // // //Get current frame from camera feed
            // // this.canvas.width = width;
            // // this.canvas.height = height;
            // // //Ensures that the image drawn on the canvas is the same as the video
            // // // var scaleH = this.isFlipX ? -1 : 1;
            // // // var scaleV = this.isFlipY ? -1 : 1;
            // // var posX = this.isFlipX ? (this.video.videoWidth - endX) : startX;
            // // var posY = this.isFlipY ? (this.video.videoHeight - endY) : startY;
            // // //Draw image
            // // var canvasContext = this.canvas.getContext('2d');
            // // // canvasContext.scale(scaleH, scaleV);
            // // canvasContext.drawImage(this.video, posX, posY, width, height, 0, 0, width, height);
            // //Get base64 image string and format it for the API
            // // let base64ImgStr = this.canvas.toDataURL('image/jpeg', 1);
            // // base64ImgStr = base64ImgStr.replace(/^data:image.+;base64,/, '');
            // let eqptDetection = answerhh[count].detection;
            // let eqptType = answerhh[count].equipment;
            // indivResults = [imgStr, eqptDetection, eqptType];
            // // return base64ImgStr;
            // return indivResults;
        },

        // end of Lina added

        //Prepare the data to send to the API
        prepareData(frame, itemsToDetectList) {
            console.log('prepareData: true');
            var base64ImgStr = '';
            if (frame != null) {
                base64ImgStr = frame;
            } else {
                //Get current frame
                base64ImgStr = this.drawFrame();
            }
            //Prepare form data to send to API
            let formData = new FormData();

            let valDict = {
                image: base64ImgStr,
                checkForObjects: this.checkForObjects,
                left: this.xPos,
                top: this.yPos,
                width: this.rectWidth,
                height: this.rectHeight
            };
            for (const [key, value] of Object.entries(valDict)) {
                formData.append(key, value);
            }
            for (let i = 0; i < itemsToDetectList.length; i++) {
                formData.append('itemDetectionList', itemsToDetectList[i].id);
            }

            return formData;
        },
        //Draws the current frame
        drawFrame() {
            console.log('drawFrame: true');
            //Get current frame from camera feed
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
            //Ensures that the image drawn on the canvas is the same as the video
            var scaleH = this.isFlipX ? -1 : 1;
            var scaleV = this.isFlipY ? -1 : 1;
            var posX = this.isFlipX ? this.canvas.width * -1 : 0;
            var posY = this.isFlipY ? this.canvas.height * -1 : 0;
            //Draw image
            var canvasContext = this.canvas.getContext('2d');
            canvasContext.scale(scaleH, scaleV);
            canvasContext.drawImage(
                this.video,
                posX,
                posY,
                this.canvas.width,
                this.canvas.height
            );
            //Get base64 image string and format it for the API
            let base64ImgStr = this.canvas.toDataURL('image/jpeg', 1);
            base64ImgStr = base64ImgStr.replace(/^data:image.+;base64,/, '');
            return base64ImgStr;
        },
        //Check the person's Personal Protective Equipment
        checkEquipment() {
            console.log('checkEquipment: true');
            //Reset
            this.guideTrigger = null;
            this.togglePersonResultsPanel = false;
            this.personDetected = false;
            this.detectedItems = null;
            this.progressValue = 0;
            this.progressColor = '#CDDC39';
            //this.progressText = 'Detecting';  //lina commented out
            //Get 3 frames to detect

            //added
            // var frames = [];
            // let myObj = {};
            // myObj.base64Str = this.drawFrame();
            // frames.push(myObj)

            //experimental added
            let frame = {};
            frame.base64Str = this.drawFrame();

            // commented out
            // var frames = [];
            // for (let i = 0; i < 3; i++) {
            //     let myObj = {};
            //     myObj.base64Str = this.drawFrame();  // draw the whole screen
            //     frames.push(myObj);
            // }

            //Set
            this.checkingEquipment = true;
            this.loaderComponent = Loader;
            // this.toggleProgressBarPanel = true;
            this.checkForObjects = true;

            //Get voices
            const allVoicesObtained = new Promise((resolve, reject) => {
                let voices = window.speechSynthesis.getVoices();
                if (voices.length !== 0) {
                    resolve(voices);
                } else {
                    window.speechSynthesis.addEventListener(
                        'voiceschanged',
                        function() {
                            voices = window.speechSynthesis.getVoices();
                            resolve(voices);
                        }
                    );
                }
            });

            allVoicesObtained.then(voices => {
                //Check if browser is Edge or Edge Chromium
                var isIE = /*@cc_on!@*/ false || !!document.documentMode;
                var isEdge = !isIE && !!window.StyleMedia;
                var isChrome =
                    !!window.chrome &&
                    (!!window.chrome.webstore || !!window.chrome.runtime);
                var isEdgeChromium =
                    isChrome && navigator.userAgent.indexOf('Edg') != -1;
                var index = 0;
                if (isEdge || isEdgeChromium) {
                    console.log('isEdgeChromium');
                    index = 1;
                }

                //Utter message
                var synth = window.speechSynthesis;
                var beginMsg = '';
                // var beginMsg = 'Detecting';
                var utterThis = new SpeechSynthesisUtterance(beginMsg);

                utterThis.voice = voices[index];
                synth.speak(utterThis);

                var toDetectList = [...this.itemList];
                var successList = [];
                //console.log(toDetectList);
                //Wait for text-to-speech to finish
                utterThis.onend = async e => {
                    // var framecount = -1;
                    //Detect each frame
                    // for (let i = 0; i < frames.length; i++) {
                    //Get form data to send to API
                    var formData = this.prepareData(
                        frame.base64Str,
                        toDetectList
                    );

                    // framecount = framecount + 1;  // Lina added

                    var endDetection = false;
                    if (this.fullscreenTrigger) {
                        await axios({
                            method: 'post',
                            url: '/api/detection/advanceObjectDetection/',
                            data: formData,
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        })
                            .then(response => {
                                //If true, then end detection
                                if (!this.returningToStart) {
                                    //console.log(response.data);
                                    //Person detected succeeded - Person inside the box + No Problems
                                    if (response.data.humanDetections) {
                                        //  Lina added
                                        console.log(
                                            'checkEqpt mtd - humanDetections = True.'
                                        );
                                        console.log(response.data.detections);

                                        // Get coord of hardhat.  If empty list, draw a box around person based on personcoords.
                                        var answerhh = response.data.detections;
                                        var numofpax = answerhh.length;

                                        // console.log('framecount is  ' + framecount);

                                        // Draw box around all human detected
                                        // this.drawHumanBox(answerhh, numofpax);
                                        // this.drawBox(answerhh, numofpax);

                                        //  end of Lina edit

                                        var detections =
                                            response.data.detections;

                                        var partNotDetected = {};
                                        var checkingEnded = false; // var for ending detection if body part is found but eqpt not found
                                        //Check through each equipment's detection result
                                        for (
                                            let j = 0;
                                            j < detections.length;
                                            j++
                                        ) {
                                            //console.log(JSON.stringify(detections[j]));
                                            //If the body part that the equipment was worn on was detected
                                            if (detections[j].partDetection) {
                                                //If the equipment was detected
                                                if (detections[j].detection) {
                                                    //Add the equipment name to detection object
                                                    let index = this.findIndexByAttr(
                                                        toDetectList,
                                                        'id',
                                                        parseInt(
                                                            detections[j]
                                                                .equipment
                                                        )
                                                    );
                                                    detections[j].Name =
                                                        toDetectList[
                                                            index
                                                        ].name;
                                                    //Remove item from the list of equipment to detect
                                                    toDetectList.splice(
                                                        index,
                                                        1
                                                    );
                                                    //Store result
                                                    successList.push(
                                                        detections[j]
                                                    );
                                                }

                                                // end if (detections[j].detection).  if eqpt detected.
                                                checkingEnded = true;

                                                console.log(
                                                    '------toDetectList: ' +
                                                        JSON.stringify(
                                                            toDetectList
                                                        )
                                                );
                                            } // else >> if (detections[j].partDetection)
                                            // didn't find body parts
                                            else {
                                                //If the body part that the equipment was worn on was not detected
                                                //Store the detection object

                                                partNotDetected = detections[j];
                                                endDetection = true;

                                                break;
                                            }
                                        } //end of for(let j = 0;.....

                                        if (!endDetection) {
                                            //If there are no more items to detect or its on the last iteration

                                            if (
                                                toDetectList.length == 0 ||
                                                checkingEnded == true
                                                // || i >= 2
                                            ) {
                                                //Hide loader
                                                this.loaderComponent = null;

                                                // This has been commented out so that the red box stays till the end
                                                //Clear canvas
                                                // const ctx = this.$refs.boundaryBoxCanvas.getContext(
                                                //     '2d'
                                                // );
                                                // ctx.clearRect(
                                                //     0,
                                                //     0,
                                                //     ctx.canvas.width,
                                                //     ctx.canvas.height
                                                // );
                                                // const imgCtx = this.canvas.getContext(
                                                //     '2d'
                                                // );
                                                // imgCtx.clearRect(
                                                //     0,
                                                //     0,
                                                //     imgCtx.canvas.width,
                                                //     imgCtx.canvas.height
                                                // );

                                                //Display results
                                                this.detectedItems = [
                                                    ...successList
                                                ];
                                                this.progressValue = 100;
                                                let numOfMissingItems =
                                                    this.itemList.length -
                                                    successList.length;
                                                //If an item is missing
                                                if (numOfMissingItems > 0) {
                                                    let msg =
                                                        'Missing ' +
                                                        numOfMissingItems;
                                                    msg +=
                                                        numOfMissingItems > 1
                                                            ? ' items'
                                                            : ' item';
                                                    this.progressText = msg;
                                                } else {
                                                    this.progressText =
                                                        'All Items Found';
                                                }

                                                this.toggleColorBlindAssistPanel = true;
                                                //Play message and show timer
                                                if (
                                                    response.data.detections[0]
                                                        .detection == false
                                                ) {
                                                    this.guideTrigger = 10; // equipment not found
                                                } else {
                                                    this.guideTrigger = 4; // The detection has ended
                                                }
                                                console.log(
                                                    'Detection has ended'
                                                );
                                                //Reset error count
                                                this.errorCount = 0;

                                                //Create log
                                                // this.logResult(successList, formData);

                                                // lina added

                                                // commented out
                                                // if(framecount == (frames.length - 1)){
                                                //     console.log('drawing box');
                                                //     this.drawBox(answerhh, numofpax);

                                                // }
                                                console.log('drawing box');
                                                this.drawBox(
                                                    answerhh,
                                                    numofpax
                                                );

                                                // Crop image. post in Axios for each crop image.
                                                this.updateForAxios(
                                                    formData,
                                                    answerhh,
                                                    numofpax,
                                                    successList
                                                );

                                                var resultsforDisplay = []; //commented out

                                                // send to ResultsDisplay.vue
                                                for (
                                                    let count = 0;
                                                    count < numofpax;
                                                    count++
                                                ) {
                                                    var tempdata = [
                                                        frame.base64Str,
                                                        answerhh[count]
                                                            .detection,
                                                        answerhh[count]
                                                            .equipment,
                                                        answerhh[count]
                                                            .personcoords
                                                    ];
                                                    resultsforDisplay.push(
                                                        tempdata
                                                    );
                                                }

                                                EventBus.$emit(
                                                    'person-image',
                                                    resultsforDisplay
                                                ); // send captured image to ResultsDisplay.vue
                                                console.log('emit completed');

                                                // end of lina added
                                            }

                                            //commented out
                                            // else {
                                            //     //There are missing items - Check next frame
                                            //     this.progressValue += 33;
                                            // }
                                            //end of commented out
                                        } else {
                                            //A body part was not detected

                                            //added
                                            console.log(
                                                'body part not detected'
                                            );
                                            this.checkEquipment();
                                            //end of added

                                            //commented out
                                            // console.log(
                                            //     '------------------A body part was not detected'
                                            // );
                                            // //Reset
                                            // this.loaderComponent = null;
                                            // this.progressValue = 0;
                                            // //Check for which equipment it was for
                                            // let index = this.findIndexByAttr(
                                            //     toDetectList,
                                            //     'id',
                                            //     parseInt(
                                            //         partNotDetected.equipment
                                            //     )
                                            // );
                                            // partNotDetected.Name =
                                            //     toDetectList[index].name;
                                            // this.progressColor = '#F44336';
                                            // switch (partNotDetected.Name) {
                                            //     case 'Hard hat':
                                            //         this.progressText =
                                            //             'Face Not Detected';
                                            //         this.guideTrigger = 8;  // We could not detect your face
                                            //         break;
                                            //     case 'Gloves':
                                            //         this.progressText =
                                            //             'Hands Not Detected';
                                            //         this.guideTrigger = 9;  // We could not detect your hands
                                            //         break;
                                            // }
                                            //end of commented out
                                        }

                                        //added
                                    } else {
                                        console.log('no person found');
                                        this.checkEquipment();
                                    }
                                    //end of added

                                    //commented out
                                    // } else {
                                    //     //Failure due to noncompliance of detection rules
                                    //     //A person was not found inside the box, or multiple people were detected
                                    //     //Reset
                                    //     this.loaderComponent = null;
                                    //     this.progressValue = 0;
                                    //     //Delay the closing of the progress bar panel
                                    //     setTimeout(() => {
                                    //         this.toggleProgressBarPanel = false;
                                    //     }, 1500);
                                    //     //Show person detection results panel
                                    //     this.togglePersonResultsPanel = true;
                                    //     endDetection = true;
                                    //     //Indicate Person missing in progress bar
                                    //     this.progressColor = '#F44336';
                                    //     //If multiple people detected inside the box
                                    //     if (
                                    //         response.data.errorMessage.includes(
                                    //             'too many'
                                    //         )
                                    //     ) {
                                    //         this.multipleDetected = true;
                                    //         console.log(
                                    //             '----------errorMessages success'
                                    //         );
                                    //         this.progressText =
                                    //             'Multiple People Detected';
                                    //         this.guideTrigger = 7;
                                    //     } else {
                                    //         console.log(
                                    //             '----------No person found'
                                    //         );
                                    //         //A person was not found inside the box
                                    //         this.progressText =
                                    //             'No Person Found';
                                    //         // this.guideTrigger = 3;  // We could not find you inside the yellow box ; commented out

                                    //         //Clear canvas
                                    //         const ctx = this.$refs.boundaryBoxCanvas.getContext('2d');
                                    //         ctx.clearRect(
                                    //                 0,
                                    //                 0,
                                    //                 ctx.canvas.width,
                                    //                 ctx.canvas.height
                                    //             );
                                    //         const imgCtx = this.canvas.getContext('2d');
                                    //         imgCtx.clearRect(
                                    //                 0,
                                    //                 0,
                                    //                 imgCtx.canvas.width,
                                    //                 imgCtx.canvas.height
                                    //             );

                                    //     }
                                    // }
                                    //end of commented out
                                } else {
                                    endDetection = true;
                                    // this.returnToStart();
                                }
                            })
                            .catch(error => {
                                console.log(error);

                                this.checkEquipment(); //added

                                //commented out
                                // //log error and try again
                                // console.log(JSON.stringify(error));
                                // //Indicate error occurred in progress bar
                                // this.progressColor = '#F44336';
                                // this.progressText = 'Error Occurred';
                                // this.errorCount += 1;
                                // //Remove detection loader
                                // this.loaderComponent = null;
                                // console.log('errorCount: ' + this.errorCount);
                                // endDetection = true;
                                // //3 retries max
                                // if (this.errorCount <= 3) {
                                //     this.guideTrigger = 5;
                                // } else {
                                //     //Max retry count
                                //     endDetection = true;
                                //     this.guideTrigger = 6;
                                // }
                                //end of commented out
                            });
                    }
                    //commented out
                    // else {
                    //     break;
                    // }
                    // //Exit loop
                    // if (endDetection) {
                    //     break;
                    // }
                    // }  // end of for loop - loop for each frame
                    //end of commented out
                };
            });
        },
        //Creates a log of the detection's result in the database
        logResult(detectedItems, formData, count) {
            console.log('logResult: true');
            console.log('printing count.. ' + count);

            var itemListCopy = [...this.itemList];
            //Delete unnecessary values from formData
            formData.delete('checkForObjects');
            formData.delete('itemDetectionList');

            // Lina added
            if (count > 0) {
                formData.delete('objectsViolated');
            }
            // end of Lina added

            //Add data
            //For each item in itemListCopy
            for (let i = 0; i < itemListCopy.length; i++) {
                //If detectedItems is not empty
                if (detectedItems.length > 0) {
                    //Item was detected
                    if (
                        this.findIndexByAttr(
                            detectedItems,
                            'equipment',
                            itemListCopy[i].id.toString()
                        ) != -1
                    ) {
                        formData.append('objectsDetected', itemListCopy[i].id);
                    } else {
                        //Item was not detected
                        formData.append('objectsViolated', itemListCopy[i].id);
                    }
                } else {
                    //No items were detected, all items are missing
                    formData.append('objectsViolated', itemListCopy[i].id);
                }
            }

            formData.append('countcheck', count); // Lina added

            //Send to API to create log

            // axios({
            //     method: 'post',
            //     url: '/api/logs/',
            //     data: formData,
            //     headers: {
            //         'Content-Type': 'multipart/form-data'
            //     }
            // })
            //     .then(response => {
            //         console.log(JSON.stringify(response));
            //         console.log('back from axios, response: ' + count);  // Lina added
            //     })
            //     .catch(error => {
            //         console.log(JSON.stringify(error));
            //         console.log('back from axios, error: ' + count);  // Lina added
            //     });
            // console.log('just after axios from logResult');

            return formData;
        }, // end of logResult

        //Find index of object in array based on the object's attribute value
        findIndexByAttr(array, attr, value) {
            for (var i = 0; i < array.length; i++) {
                if (array[i][attr] === value) {
                    return i;
                }
            }
            return -1;
        },
        //Clear all speechsynthesis instances from queue.
        //Accounts for instances created after onend event by canceling again every 0.1 seconds for 5 extra times.
        clearAllSpeeches() {
            var synth = window.speechSynthesis;
            var i = 0;
            synth.cancel();
            var timer = setInterval(() => {
                if (synth.speaking) {
                    synth.cancel();
                }
                if (i > 4) {
                    clearInterval(timer);
                }
                i++;
            }, 100);
        },
        //Return to the start of the detection process
        returnToStart() {
            //Used to cancel detection midway
            this.returningToStart = true;
            //Clear canvas
            const ctx = this.$refs.boundaryBoxCanvas.getContext('2d');
            ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
            const imgCtx = this.canvas.getContext('2d');
            imgCtx.clearRect(0, 0, imgCtx.canvas.width, imgCtx.canvas.height);
            //Clear all utterances
            this.clearAllSpeeches();
            //Reset all variables and components used in the detection process
            this.guideTrigger = null;
            this.errorCount = 0;
            this.togglePersonResultsPanel = false;
            this.multipleDetected = false;
            this.personDetected = false;
            this.checkingEquipment = false;
            this.toggleEquipmentResultsPanel = true;
            // this.toggleEquipmentResultsPanel = false;
            this.detectedItems = null;
            this.toggleProgressBarPanel = false;
            this.toggleColorBlindAssistPanel = false;
            this.loaderComponent = null;
            this.canvas.style.display = 'none';
            this.cancelBtnDisplay = 'none';
            //Check for any changes in the items list
            this.setItemListForDetection();
            //Reload components
            this.guideComponent = null;
            // this.resultsComponent = null;
            //Show start screen
            setTimeout(() => {
                this.guideComponent = DetectionGuide;
                this.resultsComponent = ResultsDisplay;
                this.launchGuide();
                this.checkForPerson();
                this.checkEquipment();
                // this.startComponent = StartScreen; //commented out
            }, 500); // original value = 500
        }
    }
};
</script>

<style>
.drawingArea {
    position: absolute;
    top: 0;
    max-width: 100%;
    height: 100%;
}

#canvas {
    object-fit: cover;
    opacity: 1;
}

#canvasContainer {
    z-index: 1;
}

#boundaryBoxCanvas {
    z-index: 11;
}

#dot {
    height: 45px;
    width: 45px;
    background-color: green;
    border-radius: 50%;
    left: 1%;
    top: 2%;
    position: absolute;
}

.flipX {
    transform: scaleX(-1);
}

.flipY {
    transform: scaleY(-1);
}

.flipXY {
    transform: scaleX(-1) scaleY(-1) !important;
}

#cancelBtnWrapper {
    position: absolute;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    z-index: 150;
}

#cancelBtn {
    position: absolute;
    left: 25px;
    bottom: 25px;
}
</style>
