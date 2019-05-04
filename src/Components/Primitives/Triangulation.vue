<template>
    <g>
		<path class="face" v-for="(face, i) in polygon.faces" :key="i" :d="face.svg()" />
	</g>
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
.flatsurf {
	path.face {
		stroke: #d1d1d1;
		stroke-width: 1px;
		fill: rgba(lightcyan, .5);
	}
}
</style>