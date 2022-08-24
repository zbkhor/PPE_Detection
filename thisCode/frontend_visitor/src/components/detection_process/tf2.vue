<template>
    <div id="tf2">
        <h3 v-if="!isVideoStreamReady && !initFailMessage">
            Initializing webcam stream ...
        </h3>
        <h3 v-if="!isModelReady && !initFailMessage">loading model ...</h3>
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
import { labelMap } from '../../../../../test/src/utilities';
const axios = require('axios').default;
const MODEL_URL =
    'https://raw.githubusercontent.com/zbkhor/ExportModel/main/model/model.json';
    


export default {
    name: 'tf2',

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
            base64:null,
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

        takepicture() {
            this.$refs.canvas.width =640
            this.$refs.canvas.height=480
            const getBase64StringFromDataURL = (data) =>
                     data.replace('data:', '').replace(/^.+,/, '');
            const context = this.$refs.canvas.getContext('2d');
            context.drawImage(this.$refs.video,0,0)

            const data =this.$refs.canvas.toDataURL('image/png');
            // this.$refs.canvas.setAttribute('src', data);
            this.base64 = getBase64StringFromDataURL(data);
            this.$refs.canvas.width =1920
            this.$refs.canvas.height=1080
            },
            
        setResultSize() {
            // get the current browser window size
            let clientWidth = window.screen.availWidth
            this.resultWidth =1920
            this.resultHeight = 1080
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
        async updateForAxios(prediction,violated) {
            console.log('updateForAxios: true');
            console.log(violated , prediction)
            let formData = new FormData();
            formData.append('image',this.base64)
            formData.append('ObjectViolated', violated)
            formData.append('condition',prediction)
           



                await axios({
                    method: 'post',
                    url: 'http://127.0.0.1:8000/api/tf2/',
                    data: formData,
                    headers: { 'Content-Type': 'multipart/form-data' }
                })
                    .then(response => {
                        console.log(JSON.stringify(response));
                        console.log('back from axios, response: ' ); // Lina added
                    })
                    .catch(error => {
                        console.log('error.response', error.response);
                        console.log(JSON.stringify(error));
                        console.log('back from axios, error: '); // Lina added
                    });
            },
        async detectObjects() {
            if (!this.isModelReady) return;

            const img = tf.browser.fromPixels(this.$refs.video);
            const resized = tf.image.resizeBilinear(img, [640, 640]);
            const casted = resized.cast('int32');
            const expanded = casted.expandDims(0);
            const obj = await this.model.executeAsync(expanded);
            
            //check the size and extract correct tensor
            for (let i = 0; i < 8; i++) {
                if (obj[i].size == 400 && obj[i].shape.length == 3) {
                    var boxes = await obj[i].array();     
                } else if (obj[i].size == 100 && obj[i].shape.length == 2) {
                    var notsure = await obj[i].array();
                    if (notsure[0][0] < 1) {
                        var scores = await obj[i].array();
                    } else if (notsure[0][0] >= 1) {
                        var classes = await obj[i].array();
                    }
                }
            }
            

            var threshold_score=0.5
            this.takepicture()
            const ctx = this.$refs.canvas.getContext('2d');
            requestAnimationFrame(() => {
                drawRect(
                    boxes[0],
                    classes[0],
                    scores[0],
                    threshold_score,
                    this.$refs.canvas.width,
                    this.$refs.canvas.height,
                    ctx
                );
            });
            let scoreslist = []
            for (let i = 0; i < scores[0].length; i++) {
                if(scores[0][i]>threshold_score){   
                    console.log(scores)                                                         
                    let index = scores[0].indexOf(scores[0][i])
                    scoreslist.push(index)

            }}
            let classeslist = []
            for (let i = 0; i < scoreslist.length; i++) {
                let classindex = classes[0][i]  
                classeslist.push(classindex)
            }
           
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
            if(classeslist.includes(2)){
                var withhelmetprediction = 'person with helmet';
                var helmetindex = classeslist.indexOf(2)
                var withhelmetscores = scores[0][helmetindex]
             
            }
            if(classeslist.includes(1)){
                var withouthelmetprediction = 'person without helmet';
                var nohelmetindex = classeslist.indexOf(1)
                console.log("nohelmetindex = " +nohelmetindex )
        
                var withouthelmetscores = scores[0][nohelmetindex]
            }
            
            if(scores[0][0]>threshold_score){
                if(withouthelmetprediction =='person without helmet' && withouthelmetscores>=threshold_score){

                    var prediction='person without helmet'; 
                    var violated = labelMap[1]['Violated']
                    this.updateForAxios(prediction,violated)
                    
                // }else if(withhelmetprediction =='person with helmet' &&  withhelmetscores>=threshold_score){
                //     var prediction = 'person with helmet';
                //     var violated = labelMap[2]['Violated']
                    
                }else if(withhelmetprediction=='person with helmet'&& withouthelmetprediction =='person without helmet' &&  withouthelmetscores >=threshold_score){
                    // var prediction = 'person without helmet';
                    // var violated = labelMap[1]['Violated']
                    var prediction = 'person without helmet';
                    var violated = labelMap[1]['Violated']
                    this.updateForAxios(prediction,violated)
                    
                }
               
               

            }
        },
        
        loadModelAndDetection() {
            this.modelPromise = this.loadCustomModel();

            // wait for both stream and model promise finished then start detecting objects
            Promise.all([this.streamPromise, this.modelPromise])
                .then(() => {
                    setInterval(this.detectObjects, 1000);
                })
                .catch(error => {
                    console.log('Failed to init stream and/or model: ');
                    this.initFailMessage = error;
                });
        },
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
  

    video {

        width: 100%    !important;
        height: 100%  !important;

    }
    canvas {
        width: 100%    !important;
        height: 100%  !important;
    }
}
</style>
