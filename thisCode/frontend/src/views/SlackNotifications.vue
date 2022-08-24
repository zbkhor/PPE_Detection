<!--
    Author: Andre Ching Wei Jie
    Date Written: 12/08/2020
-->
<template>
    <v-container fluid>
        <slack-notif></slack-notif>
    </v-container>
</template>

<script>
import SlackNotif from '@/components/slack_notifications/SlackNotif';

export default {
    name: 'SlackNotifications',
    components: {
        SlackNotif,
    },
};
</script>

<style scoped></style>
