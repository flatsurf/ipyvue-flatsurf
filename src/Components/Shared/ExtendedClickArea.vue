<template>
    <!-- we mousedown.prevent.stop so our parents won't see drag events -->
	<g class="extended-click-area" @mousedown.prevent.stop="$emit('mousedown')" @click="$emit('click')" @mouseenter="$emit('mouseenter')" @mouseleave="$emit('mouseleave')" @mousemove="(e) => $emit('mousemove', e)" >
		<g class="extension">
		  <slot/>
		</g>
		<slot/>
	</g>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

@Component
export default class ExtendedClickArea extends Vue {}
</script>
<style lang="scss">
.extended-click-area {
	.extension * {
		visibility: hidden !important;
		stroke-width: 30px !important;
		stroke-linejoin: round !important;
		stroke-linecap: butt !important;
		pointer-events: all !important;
	}

	.extension circle {
        stroke-width: inherit !important;
		transform-origin: center center;
		transform-box: fill-box;
		transform: scale(2);
	}
}
</style>