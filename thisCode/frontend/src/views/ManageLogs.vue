<!--
    Author: Andre Ching Wei Jie
    Date Written: 12/08/2020
-->
<template>
    <v-container fluid>
        <manage-logs></manage-logs>
    </v-container>
</template>

<script>
import ManageLogs from '@/components/manage_logs/ManageLogsTable';

export default {
    name: 'ManageLogsE',
    components: {
        ManageLogs,
    },
};
</script>

<style scoped></style>
