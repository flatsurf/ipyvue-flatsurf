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
		stroke-width: 0;
		fill: transparent;
	}

	.highlight circle {
		fill: #d95f02;
	}
}
</style>