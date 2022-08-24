<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <div class="px-8 py-5 text-left">
        <div class="mb-4">
            <span id="mediaText" class="font-weight-medium"
                >Media Settings</span
            >
        </div>
        <div>
            <div id="mediaInnerContainer">
                <v-select
                    v-model="selectedVideoSource"
                    :items="myVideoSources"
                    item-text="deviceName"
                    item-value="deviceId"
                    label="Video Source"
                    ref="videoSource"
                    outlined
                    dense
                    @change="changeMedia"
                >
                </v-select>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MediaSelection',
    data() {
        return {
            //List of devices for v-select items prop
            myVideoSources: [],
            //Selected Devices
            selectedVideoSource: null
        };
    },
    props: ['devices'],
    watch: {
        //Update video constraints
        devices: function() {
            console.log('watch:devices: true');
            this.gotDevices(this.devices);
        }
    },
    methods: {
        gotDevices(deviceInfos) {
            console.log('gotDevices: true');
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
                    if (source.some(x => x.deviceId === values[index])) {
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
        }, //end gotDevices()
        changeMedia() {
            let media = [this.selectedVideoSource];
            this.$emit('mediaReceived', media);
        } //end changeMedia()
    }
};
</script>
