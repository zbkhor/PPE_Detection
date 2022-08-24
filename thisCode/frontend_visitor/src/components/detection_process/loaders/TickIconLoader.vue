<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <div>
        <svg
            version="1.1"
            id="tick"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            style="margin: auto; background: none; display: block; shape-rendering: auto;"
            width="100px"
            height="100px"
            viewBox="-8.4 -8.4 53.8 53.8"
            preserveAspectRatio="xMidYMid"
        >
            <path
                class="circ path"
                style="        fill: none;
        stroke: #CDDC39;
        stroke-width: 3;
        stroke-linejoin: round;
        stroke-miterlimit: 10;"
                d="
	M30.5,6.5L30.5,6.5c6.6,6.6,6.6,17.4,0,24l0,0c-6.6,6.6-17.4,6.6-24,0l0,0c-6.6-6.6-6.6-17.4,0-24l0,0C13.1-0.2,23.9-0.2,30.5,6.5z"
            />

            <polyline
                class="tick path"
                style="        fill: none;
        stroke: #CDDC39;
        stroke-width: 3;
        stroke-linejoin: round;
        stroke-miterlimit: 10;"
                points="
	11.6,20 15.9,24.2 26.4,13.8 "
            />
        </svg>
    </div>
</template>

<style>
.circ {
    stroke-dasharray: 130;
    stroke-dashoffset: 130;
    animation: circ ease-out 1s;
    animation-iteration-count: 1;
    animation-fill-mode: forwards;
}

.tick {
    stroke-dasharray: 50;
    stroke-dashoffset: 50;
    animation: tick ease-out 0.5s;
    animation-delay: 1s;
    animation-iteration-count: 1;
    animation-fill-mode: forwards;
}

@-webkit-keyframes circ {
    to {
        stroke-dashoffset: 0;
    }
}

@keyframes circ {
    to {
        stroke-dashoffset: 0;
    }
}

@-webkit-keyframes tick {
    to {
        stroke-dashoffset: 0;
    }
}

@keyframes tick {
    to {
        stroke-dashoffset: 0;
    }
}
</style>
