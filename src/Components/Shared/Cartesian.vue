<template>
	<g class="cartesian" :transform="`translate(0 ${height}) scale(1 -1)`">
		<slot />
	</g>
</template>
<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class Cartesian extends Vue {
	@Prop({required: true, type: Number}) height!: number;
}
</script>
<style lang="scss">
.flatsurf .cartesian {
	text {
		transform: scaleY(-1);
	}
}
</style>
