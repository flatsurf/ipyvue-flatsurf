<template>
    <g>
		<text :x="edge.ps.x" :y="edge.ps.y">{{ halfEdge }}</text>
		<extended-click-area @click="$emit('click')" @mouseenter="$emit('mouseenter')" @mouseleave="$emit('mouseleave')">
			<line class="half-edge" :x1="edge.ps.x" :y1="edge.ps.y" :x2="edge.pe.x" :y2="edge.pe.y" />
		</extended-click-area>
	</g>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";

import ExtendedClickArea from "../Shared/ExtendedClickArea.vue";

@Component({
	components: { ExtendedClickArea },
})
export default class HalfEdge extends Vue {
	@Prop({required: true, type: String}) halfEdge!: string;
	@Prop({required: true, type: Object}) edge!: Flatten.Segment;
}
</script>
<style lang="scss">
.flatsurf {
	text {
		visibility: hidden;
	}
	.highlight text {
		visibility: visible;
	}
	.highlight line {
		stroke: #1b9e77;
		stroke-width: 2px;
		cursor: pointer;
		// cursor: url("../../../node_modules/octicons/build/svg/git-branch.svg"), auto;
	}

	.selected line {
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