<template>
    <div id="preset">
        <!-- <h3 v-if="!isVideoStreamReady && !initFailMessage">
            Initializing webcam stream ...
        </h3>
        <h3 v-if="!isModelReady && !initFailMessage">loading model ...</h3> -->
        <h3 v-if="initFailMessage">
            Failed to init stream and/or model - {{ initFailMessage }}
        </h3>

        <div class="resultFrame">
            <video ref="video" autoplay playsinline></video>
            <canvas
                ref="canvas"
                :width="resultWidth"
                :height="resultHeight"
            ></canvas>
        </div>
    </div>
</template>

<script>
var boxes;
import * as tf from '@tensorflow/tfjs';
import { loadGraphModel } from '@tensorflow/tfjs-converter';
import { drawRect } from '../../../../../test/src/utilities';
const MODEL_URL =
    'https://raw.githubusercontent.com/zbkhor/ExportModel/main/model/model.json';

export default {
    name: 'preset',

    data() {
        return {
            // store the promises of initialization
            streamPromise: null,
            modelPromise: null,

            // control the UI visibilities
            isVideoStreamReady: false,
            isModelReady: false,
            initFailMessage: '',

            // tfjs model related
            model: null,

            videoRatio: 1,
            resultWidth: 0,
            resultHeight: 0
        };
    },

    methods: {
        initWebcamStream() {
            // if the browser supports mediaDevices.getUserMedia API
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                return navigator.mediaDevices
                    .getUserMedia({
                        audio: false, // don't capture audio
                        video: { facingMode: 'environment' } // use the rear camera if there is
                    })
                    .then(stream => {
                        // set <video> source as the webcam input
                        let video = this.$refs.video;
                        try {
                            video.srcObject = stream;
                        } catch (error) {
                            // support older browsers
                            video.src = URL.createObjectURL(stream);
                        }

                        return new Promise((resolve, reject) => {
                            // when video is loaded
                            video.onloadedmetadata = () => {
                                // calculate the video ratio
                                this.videoRatio =
                                    video.offsetHeight / video.offsetWidth;
                                // add event listener on resize to reset the <video> and <canvas> sizes
                                window.addEventListener(
                                    'resize',
                                    this.setResultSize
                                );
                                // set the initial size
                                this.setResultSize();

                                this.isVideoStreamReady = true;
                                console.log('webcam stream initialized');
                                resolve();
                            };
                        });
                    })
                    .catch(error => {
                        console.log(
                            'failed to initialize webcam stream',
                            error
                        );
                        throw error;
                    });
            } else {
                return Promise.reject(
                    new Error(
                        'Your browser does not support mediaDevices.getUserMedia API'
                    )
                );
            }
        },

        setResultSize() {
            // get the current browser window size
            let clientWidth = document.documentElement.clientWidth;

            // set max width as 600
            // set the height according to the video ratio
            this.resultWidth = 1000;

            this.resultHeight = this.resultWidth * this.videoRatio;
            // set <video> width and height
            /*
        Doesn't use vue binding :width and :height,
          because the initial value of resultWidth and resultHeight
          will affect the ratio got from the initWebcamStream()
      */
            let video = this.$refs.video;
            video.width = this.resultWidth;
            video.height = this.resultHeight;
        },

        loadCustomModel() {
            this.isModelReady = false;

            // load the model with loadGraphModel
            return loadGraphModel(MODEL_URL)
                .then(model => {
                    this.model = model;
                    this.isModelReady = true;
                    console.log('model loaded: ', model);
                })
                .catch(error => {
                    console.log('failed to load the model', error);
                    throw error;
                });
        },

        async detectObjects() {
            if (!this.isModelReady) return;

            const img = tf.browser.fromPixels(this.$refs.video);
            const resized = tf.image.resizeBilinear(img, [640, 640]);
            const casted = resized.cast('int32');
            const expanded = casted.expandDims(0);
            const obj = await this.model.executeAsync(expanded);
            console.log(obj[1].array());
            console.log(obj[4].array());
            //check the size and assign to correct tensor
            for (let i = 0; i < 8; i++) {
                if (obj[i].size == 400 && obj[i].shape.length == 3) {
                    var boxes = await obj[i].array();
                    console.log(boxes);
                } else if (obj[i].size == 100 && obj[i].shape.length == 2) {
                    var notsure = await obj[i].array();
                    console.log();

                    if (notsure[0][0] < 1) {
                        var scores = await obj[i].array();
                    } else if (notsure[0][0] >= 1) {
                        var classes = await obj[i].array();
                    }
                }
            }


     
            const ctx = this.$refs.canvas.getContext('2d');
            requestAnimationFrame(() => {
                drawRect(
                    boxes[0],
                    classes[0],
                    scores[0],
                    0.4,
                    this.$refs.video.width,
                    this.$refs.video.height,
                    ctx
                );
            });

            tf.dispose(img);
            tf.dispose(resized);
            tf.dispose(casted);
            tf.dispose(expanded);
            tf.dispose(obj);
            ctx.clearRect(
                0,
                0,
                this.$refs.canvas.width,
                this.$refs.canvas.height
            );
            console.log('cleared');
        },

        loadModelAndDetection() {
            this.modelPromise = this.loadCustomModel();

            // wait for both stream and model promise finished then start detecting objects
            Promise.all([this.streamPromise, this.modelPromise])
                .then(() => {
                    setInterval(this.detectObjects, 500);
                })
                .catch(error => {
                    console.log('Failed to init stream and/or model: ');
                    this.initFailMessage = error;
                });
        }
    },

    mounted() {
        this.streamPromise = this.initWebcamStream();
        this.loadModelAndDetection();
    }
};
</script>

<style lang="scss">
body {
    margin: 0;
}

.resultFrame {
    display: grid;

    video {
        grid-area: 1 / 8;
        margin-left : 23px
    }
    canvas {
        grid-area: 1 / 8;
        margin-left : 23px
    }
}
</style>
