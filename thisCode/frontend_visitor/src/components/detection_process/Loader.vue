<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <div id="apiLoader">
        <!-- <svg
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            style="margin-top: auto; background: none; display: block; shape-rendering: auto;"
            width="350px"
            height="250px"
            viewBox="0 0 100 100"
        >
            <path
                fill="none"
                stroke="#47e90c"
                stroke-width="5"
                stroke-dasharray="42.76482137044271 42.76482137044271"
                d="M24.3 30C11.4 30 5 43.3 5 50s6.4 20 19.3 20c19.3 0 32.1-40 51.4-40 C88.6 30 95 43.3 95 50s-6.4 20-19.3 20C56.4 70 43.6 30 24.3 30z"
                stroke-linecap="round"
                style="transform:scale(1.2);transform-origin:50px 50px"
            >
                <animate
                    attributeName="stroke-dashoffset"
                    repeatCount="indefinite"
                    dur="1.7543859649122806s"
                    keyTimes="0;1"
                    values="0;256.58892822265625"
                ></animate>
            </path>
        </svg> -->
        <div id="apiLoaderText">
            <span class="textColor"
                >DETECTING AND
                <p>LOGGING RESULT</p></span
            >
            <!-- original text -->
        </div>
    </div>
</template>

<script>
export default {
    name: 'Loader',

    data() {
        return {};
    }
};
</script>

<style>
#apiLoader {
    position: absolute;
    height: 100%;
    display: flex;
    flex-direction: column;
}

#apiLoaderText {
    margin-bottom: auto;
    font-size: 3rem;
    /* color: #47e90c; */
    color: #008000;
    margin-top: 50px; /* original value = -25px */
    letter-spacing: 0.1666666667em !important;
}

.textColor {
    animation: textColor ease-in-out 1.5s infinite;
}

@-webkit-keyframes textColor {
    0% {
        color: #333333;
    }

    50% {
        color: #55e720;
    }

    100% {
        color: #333333;
    }
}

@keyframes textColor {
    0% {
        color: #333333;
    }

    50% {
        color: #55e720;
    }

    100% {
        color: #333333;
    }
}
</style>
