<template>
	<g class="svg-label" :transform="transformation">
		<text><slot/></text>
	</g>
</template>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";

@Component
export default class SVGLabel extends Vue {
	@Prop({required: true, type: Object}) at!: Flatten.Segment;

	protected width: number = 1;
	protected height: number = 1;

	get position() {
		const midpoint = this.at.middle();
		let normal = this.at.tangentInStart().rotate90CW().normalize();
		return midpoint.translate(normal.multiply(8));
	}

	get transformation() {
		let angleCCW = new Flatten.Vector(1, 0).angleTo(this.at.tangentInStart());
		if (angleCCW >= Math.PI)
			angleCCW -= Math.PI;
		const angleCW = angleCCW - Math.PI;
		let angle = (Math.abs(angleCCW) < Math.abs(angleCW) ? angleCCW : angleCW) * 360 / (2*Math.PI);
		if (Math.abs(angle) > 30) {
			angle = 0;
		}
		return `translate(${this.position.x} ${this.position.y}) rotate(${angle}) translate(-6 4)`;
	}
}
</script>
<style lang="scss">
.flatsurf {
	.svg-label {
		font-size: 75%;
		text-align: center;
		font-weight: 700;
	}
}
</style>
