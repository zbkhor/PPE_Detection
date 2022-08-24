<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<!--
    Error 404 Page
-->
<template>
    <v-container id="container404">
        <div
            id="textDisplay"
            class="d-flex justify-center align-center flex-column"
        >
            <div id="msg404" class="blue--text text--darken-1 pb-6">
                <span>404</span>
            </div>
            <span
                class="grey--text text--darken-3 font-weight-light"
                style="font-size: 2.4rem;"
                >Sorry!</span
            ><br />
            <span class="mt-1 font-weight-light" style="font-size: 1.5rem;"
                >We can't find the page you are looking for.</span
            >
            <v-btn to="/" class="mt-16 pa-5 blue darken-1 white--text"
                >Go back to Home</v-btn
            >
        </div>
    </v-container>
</template>

<script>
export default {
    name: 'Error404',
};
</script>

<style>
#container404 {
    position: relative;
    height: 100%;
    padding-top: 100px;
}

#msg404 {
    font-size: 10rem;
    font-weight: 600;
    line-height: 1;
}
</style>
