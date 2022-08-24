<!--
    Author: Wang Wei Liang Matthew
    Date Written: 10/08/2020
-->
<template>
    <v-container fluid>
        <equipment-selection></equipment-selection>
    </v-container>
</template>

<script>
import EquipmentSelection from '@/components/ppe_selection/EquipmentSelection';

export default {
    name: 'PPESelection',
    components: {
        EquipmentSelection,
    },
};
</script>

<style scoped></style>
