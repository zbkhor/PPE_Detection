<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <div class="px-8 py-5 text-left">
        <span id="resolutionText" class="font-weight-medium pt-5"
            >Resolution Settings</span
        >
        <v-list class="d-flex mx-auto ppe-btn-list">
            <v-list-item id="resolutionListItems">
                <v-btn
                    id="qvga"
                    @click="sendConstraints(qvgaConstraints)"
                    class="white--text"
                    :class="qvgaBtnColor"
                    >QVGA</v-btn
                >
                <v-btn
                    id="vga"
                    @click="sendConstraints(vgaConstraints)"
                    class="white--text"
                    :class="vgaBtnColor"
                    >VGA</v-btn
                >
                <v-btn
                    id="hd"
                    @click="sendConstraints(hdConstraints)"
                    class="white--text"
                    :class="hdBtnColor"
                    >HD</v-btn
                >
                <v-btn
                    id="full-hd"
                    @click="sendConstraints(fullHdConstraints)"
                    class="white--text"
                    :class="fullHdBtnColor"
                    >Full HD</v-btn
                >
            </v-list-item>
        </v-list>
    </div>
</template>

<script>
export default {
    name: 'ResolutionSelection',
    data() {
        return {
            //Video Constraints - Resolutions
            //Quarter Video Graphics Array Resolution (320 x 240 pixels)
            qvgaConstraints: {
                video: { width: { exact: 320 }, height: { exact: 240 } }
            },
            //Video Graphics Array Resolution (640 x 480 pixels)
            vgaConstraints: {
                video: { width: { exact: 640 }, height: { exact: 480 } }
            },
            //High Definition Resolution (1280 x 720 pixels)
            hdConstraints: {
                video: { width: { exact: 1280 }, height: { exact: 720 } }
            },
            //Full HD Resolution (1920 x 1080 pixels)
            fullHdConstraints: {
                video: { width: { exact: 1920 }, height: { exact: 1080 } }
            },
            qvgaBtnColor: 'cyan',
            vgaBtnColor: 'cyan',
            hdBtnColor: 'cyan',
            fullHdBtnColor: 'cyan'
        };
    },
    methods: {
        sendConstraints(constraints) {
            console.log('sendConstraints: true');
            this.qvgaBtnColor = 'cyan';
            this.vgaBtnColor = 'cyan';
            this.hdBtnColor = 'cyan';
            this.fullHdBtnColor = 'cyan';

            switch (constraints.video.height.exact) {
                case 240:
                    this.qvgaBtnColor = 'blue darken-2';
                    break;
                case 480:
                    this.vgaBtnColor = 'blue darken-2';
                    break;
                case 720:
                    this.hdBtnColor = 'blue darken-2';
                    break;
                case 1080:
                    this.fullHdBtnColor = 'blue darken-2';
                    break;
            }
            this.$emit('constraintsReceived', constraints);
        }
    }
};
</script>
