<template>
	<div @dblclick="reset" >
		<slot />
	</div>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import panzoom from "pan-zoom";

@Component
export default class PanZoomWidget extends Vue {
	@Prop({required: true, type: Object}) protected clientViewport!: {width: number, height: number};

	private virtualLeft = 0
	private virtualTop = 0;
	// The size of one virtual pixel in the client viewport.
	// zoomed in when < 1, zoomed out when > 1.
	private scale = 1;

	get virtualViewport() {
		return {
			left: this.virtualLeft,
			top: this.virtualTop,
			width: this.clientViewport.width * this.scale,
			height: this.clientViewport.height * this.scale,
		}
	}

	private unpanzoom?: () => void;

	mounted() {
		this.unpanzoom = panzoom(this.$el, this.change);
		this.reset();
	}

	beforeDestroy() {
		this.unpanzoom!();
	}

	protected change(e: any) {
		// We either zoom or pan; mixing this is harder to implement and probably confusing anyway.
		if (e.dz !== 0) {
			// We'll scale the viewport by a factor that seemed reasonable with my mouse wheel.
			const scale = Math.exp(e.dz/96);

			// Scale the virtual viewport such that the point under the cursor remains unchanged.
			const originalViewportCoordinate = {
				left: this.virtualLeft + e.x * this.scale,
				top: this.virtualTop + e.y * this.scale,
			}
			this.scale *= scale;
			this.virtualLeft = originalViewportCoordinate.left - e.x * this.scale;
			this.virtualTop = originalViewportCoordinate.top - e.y * this.scale;
		} else {
			this.virtualLeft -= e.dx * this.scale;
			this.virtualTop -= e.dy * this.scale;
		}

		this.$emit("pan-zoom", this.virtualViewport);
	}

	protected reset() {
		this.virtualLeft = 0;
		this.virtualTop = 0;
		this.scale = 1;

		this.$emit("pan-zoom", this.virtualViewport);
	}
}
</script>