<template>
	<g v-html="polygon.svg()" />
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";

@Component
export default class Triangulation extends Vue {
	@Prop({required: true, type: Object}) polygon!: Flatten.Polygon;
}
</script>
<style lang="scss">
path {
	stroke: grey;
	stroke-width: 1px;
	fill: transparent;
}
</style>