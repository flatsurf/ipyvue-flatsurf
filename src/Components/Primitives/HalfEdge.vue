<template>
    <g class="half-edge">
		<circle v-if="cursor != null" :cx="cursor.x" :cy="cursor.y" r="20" stroke="red" stroke-width="5" />
		<svg-arrow class="indicator" v-if="indicator != null" :segment="indicatorArrow" />
		<svg-label :at="halfEdgeStart">{{ halfEdge }}</svg-label>
		<extended-click-area @click="$emit('click')" @mouseenter="$emit('mouseenter')" @mouseleave="$emit('mouseleave')" @mousemove="mousemove">
			<line class="half-edge" :x1="edge.ps.x" :y1="edge.ps.y" :x2="edge.pe.x" :y2="edge.pe.y" />
		</extended-click-area>
	</g>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";

import ExtendedClickArea from "../Shared/ExtendedClickArea.vue";
import SvgLabel from "../Shared/SVGLabel.vue";
import SvgArrow from "../Shared/SVGArrow.vue";

@Component({
	components: { ExtendedClickArea, SvgLabel, SvgArrow },
})
export default class HalfEdge extends Vue {
	@Prop({required: true, type: String}) halfEdge!: string;
	@Prop({required: true, type: Object}) edge!: Flatten.Segment;
	@Prop({default: null}) indicator!: number | null;

	private point: SVGPoint = null!;

	mounted() {
		const svg = this.$el.closest("svg")!;
		this.point = (svg as any).createSVGPoint();
	}
	private cursor: Flatten.Point | null = null;

	get halfEdgeStart() {
		return new Flatten.Segment(this.edge.start, this.edge.start.translate(this.edge.tangentInStart().multiply(20)));
	}

	get indicatorArrow() {
		if (this.indicator == null)
			return null;
		const end = this.edge.start.translate(this.edge.tangentInStart().multiply(this.edge.length).multiply(this.indicator));
		const start = end.translate(this.edge.tangentInStart().rotate90CCW().multiply(10));
		return new Flatten.Segment(start, end);
	}

	protected mousemove(e: MouseEvent) {
		const line = new Flatten.Line(this.edge.start, this.edge.end);

		this.point.x = e.clientX;
		this.point.y = e.clientY;
		this.point = this.point.matrixTransform((this.$el as any).getScreenCTM().inverse());
		// The cursor position relative to the SVG coordinate system
		const cursor = new Flatten.Point(this.point.x, this.point.y);
		const projection = cursor.projectionOn(line);
		if (projection.distanceTo(this.edge)[0] > 1) {
			// ignore this if the cursor does not project close to the segment but outside the endpoints.
			return;
		}

		const relative = new Flatten.Segment(this.edge.start, projection).length / this.edge.length;
		this.$emit("mousemove", relative);
	}
}
</script>
<style lang="scss">
.flatsurf .half-edge {
	.svg-label {
		opacity: 0;
		transition: none;
	}
	&.highlight .svg-label {
		opacity: 1;
		transition: opacity 250ms ease-in;
	}
	&.highlight line {
		stroke: #1b9e77;
		stroke-width: 2px;
		cursor: pointer;
	}

	&.selected line {
		stroke: red;
		stroke-width: 2px;
		stroke-dasharray: 10;
		animation: dash 300ms linear;
	}

	.indicator {
		fill: #d95f02;
	}
}

@keyframes dash {
	to { stroke-dashoffset: 25; }
}
</style>