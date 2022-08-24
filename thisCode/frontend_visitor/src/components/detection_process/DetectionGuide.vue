<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <div class="componentOuterBox" id="detectionGuideBox">
        <div
            id="guideTextBox"
            class="white--text d-flex justify-center align-center"
        >
            <!-- <span id="subtitle" ref="subtitle">{{ subtitle }}</span> -->
        </div>
        <div
            class="loaderBox"
            ref="loaderBox"
            :style="{ display: displayLoader }"
        >
            <div class="loader">
                <timer-loader class="timerLoader"></timer-loader>
            </div>
            <span
                id="timerDisplay"
                class="d-flex justify-center align-center"
                ref="timerDisplay"
                >{{ seconds }}</span
            >
        </div>
    </div>
</template>

<script>
import TimerLoader from '@/components/detection_process/loaders/TimerLoader';

export default {
    name: 'DetectionGuide',

    data() {
        return {
            subtitle: null,
            msgCount: 0,
            seconds: null,
            trigger: null,

            displayLoader: 'none'
        };
    },

    components: {
        TimerLoader
    },

    props: ['guideTrigger'],

    watch: {
        guideTrigger: async function() {
            var utterances = [];
            this.trigger = this.guideTrigger;
            switch (this.trigger) {
                case 1: {
                    //Case 1: User taps on the Start screen to start the detection process
                    console.log('trigger = 1');

                    //Messages to display and utter
                    utterances.push('Welcome to the PPE Detection System');
                    // utterances.push(
                    //     'Stand inside the yellow box and wait for the system to detect you'
                    // );

                    this.playMessages(utterances);
                    break;
                }
                case 2: {
                    //Case 2: A person was detected inside the yellow box
                    console.log('trigger = 2');
                    // console.log('Person Found');
                    utterances.push('Person Found');
                    // utterances.push(
                    //     'We will now begin checking for your equipment'
                    // );
                    // utterances.push(
                    //     'Ensure that your equipment is visible before detection begins'
                    // // );
                    // utterances.push('Detection starting in');

                    this.playMessages(utterances);
                    break;
                }
                case 3: {
                    //Case 3: During the equipment check, a user was not detected inside the yellow box
                    console.log('trigger = 3');
                    utterances.push(
                        // 'We could not find you inside the yellow box'
                        'No persons detected'
                    );
                    // utterances.push(
                    //     'Please stay inside the yellow box until we begin checking for your equipment'
                    // );

                    this.playMessages(utterances);
                    break;
                }
                //commented out
                case 4: {
                    //Case 4: The detection process ended successfully
                    console.log('trigger = 4');
                    utterances.push('');
                    this.playMessages(utterances);
                    //commented out
                    //     utterances.push('The detection has ended.');
                    //     // utterances.push(
                    //     //     'The result has been displayed on the screen.'
                    //     // );
                    //     // utterances.push('Session ending in');

                    //     this.playMessages(utterances);
                    //end of commented out
                    break;
                }
                //end of commented out
                case 5: {
                    //Case 5: As system error occurred during detection
                    console.log('trigger = 5');
                    utterances.push('An error has occurred during detection');
                    // utterances.push('Retrying...');

                    this.playMessages(utterances);
                    break;
                }
                case 6: {
                    //Case 6: Maximum number of retries due to system errors reached. Return user to start screen
                    console.log('trigger = 6');
                    // utterances.push(
                    //     'The system is unable to process your request at this time'
                    // );
                    utterances.push(
                        'Please try again later or contact an administrator about this issue'
                    );
                    utterances.push('Session ending in');

                    this.playMessages(utterances);
                    break;
                }
                case 7: {
                    //Case 7: During the equipment check, multiple people were detected inside the box.
                    console.log('trigger = 7');
                    utterances.push(
                        'Multiple people were detected inside the yellow box'
                    );
                    // utterances.push(
                    //     'Please ensure that only one person is inside the box at all times'
                    // );

                    this.playMessages(utterances);
                    break;
                }
                case 8: {
                    //Case 8: During the equipment check for a hard hat, the face was not detected
                    console.log('trigger = 8');
                    utterances.push('We could not detect your face');
                    // utterances.push('Please ensure that your face is visible');
                    // utterances.push('Retrying in');

                    this.playMessages(utterances);
                    break;
                }
                case 9: {
                    //Case 9: During the equipment check for gloves, the hands were not detected
                    console.log('trigger = 9');
                    utterances.push('We could not detect your hands');
                    // utterances.push(
                    //     'Please ensure that your hands are spaced apart from your body'
                    // );
                    // utterances.push('Retrying in');

                    this.playMessages(utterances);
                    break;
                }
                case 10: {
                    //Case 10: PPE non-compliance
                    console.log('trigger = 10');
                    utterances.push('PPE non-compliance detected');
                    this.playMessages(utterances);
                    break;
                }
            }
        }
    },

    methods: {
        async playMessages(utterances) {
            console.log('playMessages: true');
            var utteranceObjArr = [];

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
                var synth = window.speechSynthesis;

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
                    index = 2;
                }

                console.log('Voices ' + voices.length);
                utterances.forEach(utterance => {
                    var utterThis = new SpeechSynthesisUtterance(utterance);
                    utterThis.rate = 5.0; //original value = 0.7
                    utterThis.voice = voices[index];
                    utteranceObjArr.push(utterThis);
                });

                this.msgCount = 0;

                var guideTextObj = this.$refs.subtitle;

                if (guideTextObj) {
                    guideTextObj.classList.add('px-4', 'py-2');
                }
                this.subtitle = utterances[0];
                console.log('GuideText ' + this.subtitle);

                for (let i = 0; i < utteranceObjArr.length; i++) {
                    console.log(i);

                    synth.speak(utteranceObjArr[i]);
                    if (i != utteranceObjArr.length - 1) {
                        //For all except last element in array
                        utteranceObjArr[i].addEventListener('end', e => {
                            this.subtitle = utterances[i + 1];
                        });
                    } else {
                        //For last element in array
                        utteranceObjArr[i].addEventListener('end', e => {
                            console.log('all messages spoken');
                            this.subtitle = '';
                            if (guideTextObj) {
                                guideTextObj.classList.remove('px-4', 'py-2');
                            }

                            switch (this.trigger) {
                                case 1:
                                case 3:
                                case 7: {
                                    this.$emit('detectPerson');
                                    break;
                                }
                                case 2:
                                case 8:
                                case 9: {
                                    // this.showTimer(3, index);
                                    this.$emit('detectEquipment');
                                    break;
                                }
                                case 4: {
                                    // this.showTimerWithoutSpeech(2);
                                    setTimeout(() => {
                                        this.$emit('endDetection');
                                    }, 1000);
                                    break;
                                }
                                case 5: {
                                    this.$emit('detectEquipment');
                                    break;
                                }
                                case 6: {
                                    // this.showTimerWithoutSpeech(2);
                                    setTimeout(() => {
                                        this.$emit('endDetection');
                                    }, 1000);
                                    break;
                                }
                                case 10: {
                                    setTimeout(() => {
                                        this.$emit('endDetection');
                                    }, 1000);
                                    break;
                                }
                            }

                            this.trigger = null;
                        });
                    }
                }
            });
        },

        showTimer(seconds, index) {
            console.log('showTimer: true');
            this.seconds = seconds;

            var synth = window.speechSynthesis;
            var voices = synth.getVoices();

            this.displayLoader = 'block';

            var utteranceObjArr = [];
            for (let i = this.seconds; i > 0; i--) {
                var msg = new SpeechSynthesisUtterance(i);
                msg.rate = 3.0; // original value = 1.8
                msg.voice = voices[index];
                utteranceObjArr.push(msg);
            }

            for (let i = 0; i < utteranceObjArr.length; i++) {
                synth.speak(utteranceObjArr[i]);
                if (i != utteranceObjArr.length - 1) {
                    //For all except last element in array
                    utteranceObjArr[i].addEventListener('end', e => {
                        console.log('spoken: ' + this.seconds);
                        this.seconds--;
                    });
                } else {
                    //For last element in array
                    utteranceObjArr[i].addEventListener('end', e => {
                        console.log('timer end');
                        this.displayLoader = 'none';

                        //Delay transition slightly
                        setTimeout(() => {
                            this.$emit('detectEquipment');
                        }, 0); // original value = 250
                    });
                }
            }
        },

        showTimerWithoutSpeech(seconds) {
            console.log('showTimerWithoutSpeech: true');
            this.seconds = seconds;

            this.displayLoader = 'block';

            var timer = setInterval(() => {
                this.seconds--;
                if (this.seconds <= 0) {
                    console.log('timer end');
                    this.displayLoader = 'none';
                    clearInterval(timer);

                    this.$emit('endDetection');
                }
            }, 1000);
        }
    }
};
</script>

<style>
#detectionGuideBox {
    z-index: 50;
}

#guideTextBox {
    z-index: 1;
    width: 100% !important;
    height: 100% !important;
    padding: 0 100px;
}

#subtitle {
    font-size: 2.5rem;
    z-index: 4;
    background-color: rgba(0, 0, 0, 0.7);
    position: relative;
    top: 30%;
    font-weight: 300;
}

#timerDisplay {
    font-size: 5rem;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    color: #ffffff;
    font-weight: 600;
}

.loaderBox {
    left: 50% !important;
    margin-left: -175px;
    position: absolute !important;
    top: 50% !important;
    margin-top: -175px;
    z-index: 9000 !important;
}

.loaderBox .loader {
    position: relative;
    margin: 0px auto;
    width: 350px;
    height: 350px;
}

.loaderBox .loader:before {
    content: '';
    display: block;
    padding-top: 100%;
}

.timerLoader {
    position: absolute;
    top: 0;
    left: 0;
    margin: auto;
    width: 100%;
    height: 100%;
}
</style>
