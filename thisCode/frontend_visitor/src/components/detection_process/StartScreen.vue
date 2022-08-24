<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <div
        id="startScreenBox"
        class="componentOuterBox"
        @click="removeStartText"
        ref="startScreenBox"
    >
        <!-- Particles -->
        <vue-particles
            color="#6ac5f3"
            :particleOpacity="0.7"
            :particlesNumber="125"
            shapeType="circle"
            :particleSize="4"
            linesColor="#6ac5f3"
            :linesWidth="1"
            :lineLinked="true"
            :lineOpacity="1"
            :linesDistance="75"
            :moveSpeed="0.8"
            :hoverEffect="false"
            hoverMode="grab"
            :clickEffect="true"
            clickMode="push"
            class="backParticles"
        >
        </vue-particles>
        <div
            id="startScreenTxt"
            class="d-flex justify-center align-center white--text"
            ref="startScreenTxt"
        >
            <div class="mb-10" style="width: 80%;">
                <div>
                    <span style="font-weight: normal;"
                        >PPE Detection System</span
                    >
                </div>
                <div class="mb-5">
                    <span style="font-size: 1.5rem; z-index: 3;"
                        >Beta Version</span
                    >
                </div>
                <div class="mb-3">
                    <v-icon
                        style="fill: white; width: 24%; height:100%;"
                        class="mr-12"
                        >$ectclogo</v-icon
                    >
                    <v-icon style="fill: white; width: 20%; height:100%;"
                        >$dsaclogo</v-icon
                    >
                </div>
                <div>
                    <span style="font-size: 1.5rem; z-index: 3;"
                        >Sponsored by TIEFA</span
                    >
                </div>
            </div>
            <div
                class="mt-12"
                style="position:absolute; bottom:18%; font-size: 2.8rem; z-index: 4;"
            >
                <span class="blinking">Tap anywhere to start</span>
            </div>
        </div>
        <component :is="currentComponent"></component>
    </div>
</template>

<script>
export default {
    name: 'StartScreen',

    data() {
        return {
            startTxt: null,
            startScreenBox: null,

            currentComponent: null
        };
    },

    mounted() {
        this.startTxt = this.$refs.startScreenTxt;
        this.startScreenBox = this.$refs.startScreenBox;
        this.startScreenBox.classList.add('fadeIn');
    },

    methods: {
        removeStartText() {
            console.log('removeStartText: true');
            this.startScreenBox.classList.remove('fadeIn');

            this.startScreenBox.addEventListener('animationend', () => {
                this.$emit('startScreenTapped');
            });
            this.startScreenBox.classList.add('fadeOut');
        }
    }
};
</script>

<style>
#startScreenBox {
    background: radial-gradient(
        circle at 50% 150%,
        rgb(13, 32, 142) 0%,
        rgb(57, 81, 201) 20%,
        rgb(46, 5, 107) 45%,
        rgb(40, 40, 40) 70%
    );
    z-index: 51;
}

.backParticles {
    width: 100%;
    height: 100%;
    overflow: hidden;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
}

#startScreenTxt {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    z-index: 2;
    font-weight: 300;
}

#startScreenTxt div div:first-child span {
    font-size: 3.7rem;
    z-index: 3;
}

.blinking {
    animation: blinkingText 5s infinite;
}

.fadeIn {
    animation: fadeIn 0.7s;
    animation-fill-mode: forwards;
}

.fadeOut {
    animation: fadeOut 0.7s;
    animation-fill-mode: forwards;
}

@keyframes blinkingText {
    0% {
        opacity: 1;
    }

    3% {
        opacity: 0.5;
    }

    5%,
    40% {
        opacity: 1;
    }

    43% {
        opacity: 0.5;
    }

    45% {
        opacity: 1;
    }

    48% {
        opacity: 0.5;
    }

    50% {
        opacity: 1;
    }

    50%,
    100% {
        opacity: 1;
    }
}

@keyframes fadeOut {
    0% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}

@keyframes fadeIn {
    0% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}
</style>
