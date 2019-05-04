<template>
    <g class="half-edge">
		<svg-label :at="halfEdgeStart">{{ halfEdge }}</svg-label>
		<extended-click-area @click="$emit('click')" @mouseenter="$emit('mouseenter')" @mouseleave="$emit('mouseleave')">
			<line class="half-edge" :x1="edge.ps.x" :y1="edge.ps.y" :x2="edge.pe.x" :y2="edge.pe.y" />
		</extended-click-area>
	</g>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";

import ExtendedClickArea from "../Shared/ExtendedClickArea.vue";
import SvgLabel from "../Shared/SVGLabel.vue";

@Component({
	components: { ExtendedClickArea, SvgLabel },
})
export default class HalfEdge extends Vue {
	@Prop({required: true, type: String}) halfEdge!: string;
	@Prop({required: true, type: Object}) edge!: Flatten.Segment;

	get halfEdgeStart() {
		return new Flatten.Segment(this.edge.start, this.edge.start.translate(this.edge.tangentInStart().multiply(20)));
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
		// cursor: url("../../../node_modules/octicons/build/svg/git-branch.svg"), auto;
	}

	&.selected line {
		stroke: red;
		stroke-width: 2px;
		stroke-dasharray: 10;
		animation: dash 300ms linear;
	}
}

@keyframes dash {
	to { stroke-dashoffset: 25; }
}
</style>