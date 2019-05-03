<!--
TODO: Would be cool to have a dot travel around the vertex on hover.
-->
<template>
	<extended-click-area @click="$emit('click')" @mouseenter="$emit('mouseenter')" @mouseleave="$emit('mouseleave')">
		<circle class="vertex" :cx="vertex.x" :cy="vertex.y" :r="3" />
	</extended-click-area>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";

import ExtendedClickArea from "../Shared/ExtendedClickArea.vue";

@Component({
	components: { ExtendedClickArea },
})
export default class Vertex extends Vue {
	@Prop({required: true, type: Object}) vertex!: Flatten.Point;
}
</script>
<style lang="scss">
.flatsurf {
	circle {
		stroke: transparent;
		fill: transparent;
	}

	.highlight circle {
		stroke: #d95f02;
		fill: #d95f02;
		stroke-width: 3px;
	}
}
</style>