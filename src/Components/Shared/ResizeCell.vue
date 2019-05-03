<!--
TODO: I assume that Jupyter Lab somehow communicates the size when a widget gets dragged into its own pane.
In that case, I should disable this.
-->
<template>
	<div class="flatsurf-container" :is-resizing="resizing">
		<slot />
		<div class="flatsurf-resizer" @mousedown.prevent="mousedown" />
	</div>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

@Component
export default class ResizableWidget extends Vue {
	@Prop({required: true, type: Number}) initialHeight!: number;

	protected height: number = this.initialHeight;
	protected resizing: boolean = false;

	protected mousedown() {
		if (!this.resizing) {
			window.addEventListener("mousemove", this.resize);
			window.addEventListener("mouseup", this.mouseup);
			this.resizing = true;
		}
	}

	protected mouseup() {
		this.resizing = false;
		window.removeEventListener("mousemove", this.resize);
	}

	protected resize(e : MouseEvent) {
		this.$emit("resize", Math.max(0, e.pageY - this.$el.getBoundingClientRect().top));
	}
}
</script>
<style lang="scss">
.flatsurf-container {
	position: relative;
}

.flatsurf-container[is-resizing="true"], .flatsurf-resizer {
  cursor: row-resize;
}

.flatsurf-resizer {
  position: absolute;
  bottom: 0px;
  width: 100%;
  height: 12px;

  background-image: url("../../../node_modules/octicons/build/svg/chevron-down.svg");
  background-repeat: no-repeat;
  background-position: center;
  opacity: .1;

  &:hover, .flatsurf-container[is-resizing="true"] & {
    background-color: #00000009;
	opacity: 1;
  }
}
</style>