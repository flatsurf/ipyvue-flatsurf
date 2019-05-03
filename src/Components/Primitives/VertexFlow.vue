<template>
    <g>
	  <circle class="vertex-flow" :class="{rest: atRest}" :cx="pos.x" :cy="pos.y" :r="3" />
	</g>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";

import HalfEdge from './HalfEdge.vue';

@Component({
	components: { HalfEdge }
})
export default class VertexFlow extends Vue {
	@Prop({required: true, type: Object}) halfEdge!: Flatten.Segment;
	@Prop({required: true, type: Number}) angle!: number;
	@Prop({default: false, type: Boolean}) atRest!: boolean;

	get pos() {
		// Since we are not in a Cartesian coordinate system (the y-axis is flipped)
		// we turn CW here.
		const rotated = this.halfEdge.rotate(this.angle, this.halfEdge.start);
		const unit = rotated.tangentInStart();
		return rotated.ps.translate(unit.multiply(10));
	}
}
</script>
<style lang="scss">
.flatsurf {
  .vertex-flow {
      fill: #7570b3;
	  stroke-width: 0;
  }
  .rest {
	  fill: lighten(#7570b3, 20);
  }
}
</style>
