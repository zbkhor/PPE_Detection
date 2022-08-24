<!--
    Author: Wang Wei Liang Matthew
    Date Written: 28/08/2020
-->
<template>
    <v-card>
        <v-sheet
            class="v-sheet--offset d-flex mx-auto"
            elevation="6"
            max-width="calc(100% - 32px)"
            color="navigation"
        >
            <v-icon
                class="py-6 pl-4"
                large
                dark
                :class="videoOn ? 'blinkingGreen' : 'blue--text'"
                >mdi-camera</v-icon
            >
            <span class="pl-4 d-flex align-center white--text"
                >Live Camera Feed</span
            >

            <v-spacer></v-spacer>

            <v-card-actions class="pr-4 d-flex align-center">
                <v-select
                    v-model="selectedVideoSource"
                    :items="myVideoSources"
                    item-text="deviceName"
                    item-value="deviceId"
                    label="Select Camera"
                    dense
                    outlined
                    class="videoSourceSelect mr-6"
                    @change="changeMedia"
                    :disabled="!videoOn"
                    :class="videoOn ? 'videoEnabled' : 'videoDisabled'"
                >
                </v-select>
                <v-btn
                    class="white--text"
                    @click="toggleCamera"
                    :style="{ 'background-color': toggleColor }"
                >
                    {{ cameraBtnTxt }}
                </v-btn>
            </v-card-actions>
        </v-sheet>
        <div id="camera">
            <video id="video" ref="video" autoplay></video>
        </div>
    </v-card>
</template>

<script>
export default {
    name: 'HomeCamera',
    data: function () {
        return {
            video: null,
            track: null,
            stream: null,
            videoOn: false,
            //Default constraints video will use on startup, set to highest resolution supported
            defaultConstraints: {
                video: {
                    width: { ideal: 4096 },
                    height: { ideal: 2160 },
                    frameRate: { ideal: 30 },
                },
            },
            //List of devices for v-select items prop
            myVideoSources: [
                {
                    deviceName: 'Camera is disabled',
                    deviceId: 0,
                },
            ],
            //Selected Devices
            selectedVideoSource: 0,
        };
    },
    computed: {
        cameraBtnTxt() {
            return this.videoOn ? 'Off' : 'On';
        },
        toggleColor() {
            return this.videoOn ? '#AFB42B' : '#1E88E5';
        },
    },
    mounted() {
        this.video = this.$refs.video;
    },
    methods: {
        //Get all media devices (Video) that is connected to the user's computer
        getDevices(deviceInfos) {
            console.log('getDevices: true');
            //console.log('deviceInfos: ' + JSON.stringify(deviceInfos));
            let videoSources = [];
            //console.log(JSON.stringify(deviceInfos));
            // Get media sources (Video)
            // Handles being called several times to update labels. Preserve values.
            const values = [this.selectedVideoSource];
            // Populate media source lists with their respective media sources
            for (let i = 0; i !== deviceInfos.length; ++i) {
                const deviceInfo = deviceInfos[i];
                let device = {};
                device.deviceId = deviceInfo.deviceId;
                if (deviceInfo.kind === 'videoinput') {
                    //Video Input device
                    device.deviceName =
                        deviceInfo.label || `camera ${videoSources.length + 1}`;
                    videoSources.push(device);
                } else {
                    console.log(
                        'Some other kind of source/device: ',
                        deviceInfo
                    );
                }
                // Set lists for v-select items prop
                this.myVideoSources = videoSources;
                // Set selected value for v-select
                // Set to previous id if exists
                // else set to first one
                let sources = [videoSources];
                sources.forEach((source, index) => {
                    //If the current selected source is present in the new list of sources,
                    //the selected source will remain, i.e. not changed.
                    if (source.some((x) => x.deviceId === values[index])) {
                        switch (index) {
                            case 0:
                                this.selectedVideoSource = values[index];
                                break;
                        }
                    }
                    //else if there is at least one source in the list,
                    //the selected source is the first source in the list.
                    else if (source.length > 0) {
                        switch (index) {
                            case 0:
                                this.selectedVideoSource =
                                    videoSources[0].deviceId;
                                break;
                        }
                    }
                });
            }
        },

        //Show or stop camera live feed
        async toggleCamera() {
            this.videoOn = !this.videoOn;
            //Turn camera on
            if (this.videoOn) {
                //Get devices
                await navigator.mediaDevices
                    .enumerateDevices()
                    .then((deviceInfos) => {
                        this.getDevices(deviceInfos);
                    })
                    .catch(this.handleError);
                this.getMedia(this.defaultConstraints);
            } else {
                //Clear video
                this.stream.getVideoTracks()[0].stop();

                this.video.srcObject = null;
                //Reset
                this.myVideoSources = [
                    {
                        deviceName: 'Camera is disabled',
                        deviceId: 0,
                    },
                ];
                this.selectedVideoSource = 0;
            }
        },
        //Get user media using constraints
        getMedia(constraints) {
            console.log('getMedia: true');

            //Clear video
            if (this.stream != null) {
                this.stream.getVideoTracks()[0].stop();

                this.video.srcObject = null;
            }

            //Add media source to use to resolution constraints
            const videoSource = this.selectedVideoSource;
            console.log(JSON.stringify(videoSource));
            constraints.video.deviceId = videoSource
                ? { exact: videoSource }
                : undefined;
            //console.log(JSON.stringify(constraints));
            navigator.mediaDevices
                .getUserMedia(constraints)
                .then(this.gotStream)
                .then((deviceInfos) => {
                    this.getDevices(deviceInfos);
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
            return new Promise((resolve) => (this.video.onplaying = resolve));
        },
        //Error Handling
        handleError(error) {
            console.log(
                'navigator.MediaDevices.getUserMedia error: ',
                error.message,
                error.name
            );
        },
        changeMedia() {
            this.getMedia(this.defaultConstraints);
        },
    },
};
</script>

<style>
.videoSourceSelect .v-input__control .v-text-field__details {
    display: none !important;
}

.videoSourceSelect
    .v-input__control
    .v-input__slot
    .v-select__slot
    .v-select__selections
    div {
    overflow: visible !important;
}

.videoSourceSelect .v-input__control .v-input__slot {
    margin-bottom: 0;
}

.videoSourceSelect
    .v-input__control
    .v-input__slot
    .v-select__slot
    .v-select__selections
    input {
    display: none;
}

.videoDisabled .v-input__control .v-input__slot fieldset,
.videoDisabled .v-input__control .v-input__slot .v-select__slot label,
.videoDisabled
    .v-input__control
    .v-input__slot
    .v-select__slot
    .v-select__selections
    div,
.videoDisabled
    .v-input__control
    .v-input__slot
    .v-select__slot
    .v-input__append-inner
    div
    i {
    color: #666 !important;
}

.videoEnabled .v-input__control .v-input__slot fieldset,
.videoEnabled .v-input__control .v-input__slot .v-select__slot label,
.videoEnabled
    .v-input__control
    .v-input__slot
    .v-select__slot
    .v-select__selections
    div,
.videoEnabled
    .v-input__control
    .v-input__slot
    .v-select__slot
    .v-input__append-inner
    div
    i {
    color: #fff !important;
}

.blinkingGreen {
    animation: blinkingGreen ease-in-out 1.5s infinite;
}

@-webkit-keyframes blinkingGreen {
    0% {
        color: #333333;
    }

    50% {
        color: #afb42b;
    }

    100% {
        color: #333333;
    }
}

@keyframes blinkingGreen {
    0% {
        color: #333333;
    }

    50% {
        color: #c0ca33;
    }

    100% {
        color: #333333;
    }
}
</style>

<style scoped>
#camera,
#video {
    height: 400px;
}

#video {
    width: 100%;
    background-color: #000;
    -webkit-transform: scaleX(-1);
    transform: scaleX(-1);
}
</style>
