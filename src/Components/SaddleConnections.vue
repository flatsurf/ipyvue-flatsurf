<template>
    <g>
		<g v-for="(segments, i) in layout" :key="i">
			<line class="direction" :x1="segments.direction.start.x" :y1="segments.direction.start.y" :x2="segments.direction.end.x" :y2="segments.direction.end.y" />
			<line :class="`saddle-connection-${i}`" v-for="(segment, j) in segments.segments" :key="j"
				:x1="segment.start.x" :x2="segment.end.x" :y1="segment.start.y" :y2="segment.end.y" />
		</g>
  	</g>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import Flatten from "@flatten-js/core";

import { IHalfEdgeLayout } from "../Layout/Triangulation";
import { ISaddleConnection, ILayoutedSaddleConnection } from "../Layout/SaddleConnection";

@Component
export default class SaddleConnections extends Vue {
	@Prop({required: true, type: Array}) private saddleConnections!: ISaddleConnection[];
	@Prop({required: true, type: Array}) private layout!: ILayoutedSaddleConnection[];
}
</script>
<style lang="scss">
.flatsurf .saddle-connection-0 {
	stroke-width: 3px;
	stroke: red;
}

.flatsurf .saddle-connection-1 {
	stroke-width: 3px;
	stroke: cyan;
}

.flatsurf .direction {
	stroke-width: 3px;
	stroke:pink;
}
</style>
