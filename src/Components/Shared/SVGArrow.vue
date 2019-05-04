<template>
	<g class="arrow">
		<line :x1="segmentWithoutArrow.start.x" :y1="segmentWithoutArrow.start.y"
		    :x2="segmentWithoutArrow.end.x" :y2="segmentWithoutArrow.end.y" />
		<path d="M 0 -3 L 12 0 L 0 3 z" :transform=moveToEnd stroke-width="0"/>
	</g>
</template>
<script lang="ts">
import { Prop, Vue, Component } from "vue-property-decorator";
import Flatten from "@flatten-js/core";

@Component
export default class SVGArrow extends Vue {
	@Prop({required: true, type: Object}) segment!: Flatten.Segment;

	get segmentWithoutArrow() {
		return new Flatten.Segment(this.segment.start, this.segment.end.translate(this.segment.tangentInEnd().multiply(12)));
	}

	get moveToEnd() {
		return `translate(${this.segmentWithoutArrow.end.x} ${this.segmentWithoutArrow.end.y}) rotate(${-this.segment.tangentInStart().angleTo(new Flatten.Vector(1,0))*360 / (2*Math.PI)} 0 0)`
	}
}
</script>

