<template>
  <resizable-widget class="flatsurf" :initial-height="height" @resize="resize">
	<pan-zoom-widget :client-viewport="{width, height}" @pan-zoom="moved">
		<svg :height="height" width="100%">
			<g :transform="svgTranslation">
				<flat-triangulation :width="width * svgScale - 2*padding" :height="height * svgScale - 2*padding" :vertices=vertices :halfEdges=halfEdges :faces=faces :vectors=vectors />
			</g>
		</svg>
	</pan-zoom-widget>
  </resizable-widget>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import FlatTriangulation from "./Components/FlatTriangulation.vue";
import ResizableWidget from "./Components/Shared/ResizeCell.vue";
import PanZoomWidget from "./Components/Shared/PanZoom.vue";
import ResizeSensor from "css-element-queries/src/ResizeSensor"
import Flatten from "@flatten-js/core";

// TODO: Use BBOX.ts's transform
@Component({
	components: { FlatTriangulation, ResizableWidget, PanZoomWidget },
})
export default class App extends Vue {
  @Prop({required: true}) public value!: string;
  @Prop({default: 200}) public initialHeight!: number;
  @Prop({default: 5}) public padding!: number;

  get vertices() {
	  return [["1", "2", "3", "-1", "-2", "-3"]];
  }

  get halfEdges() {
	  return { [1]: "-1", [2]: "-2", [3]: "-3", [-1]: "1", [-2]: "2", [-3]: "3" };
  }

  get faces() {
	  return [["1", "3", "-2"], ["2", "-1", "-3"]];  
  }

  get vectors() {
	return {
	  [1]: new Flatten.Vector(1, 0),
	  [2]: new Flatten.Vector(1, 1),
	  [3]: new Flatten.Vector(0, 1),
	  [-1]: new Flatten.Vector(-1, 0),
	  [-2]: new Flatten.Vector(-1, -1),
	  [-3]: new Flatten.Vector(0, -1),
	}
  }

  protected height: number = this.initialHeight;
  protected width: number = this.initialHeight;

  // We only show a portion of the underlying SVG when this is >1
  protected svgScale: number = 1;
  protected svgLeft: number = 0;
  protected svgTop: number = 0;

  get svgTranslation() {
	  return `translate(${-this.svgLeft + this.padding} ${-this.svgTop + this.padding})`;
  }

  mounted() {
	this.resize();
	new ResizeSensor(this.$el, () => this.resize());
  }

  protected resize(height?: number) {
	this.height = height || this.height;
	this.width = this.$el.clientWidth;
  }

  protected moved(viewport: {left: number, top: number, width: number, height: number}) {
	// The factor by which we have to scale the SVG so that
	// one pixel in the client is one pixel in the virtual viewport.
	const scale = this.width / viewport.width;
	this.svgScale = scale;
	this.svgLeft = viewport.left * scale;
	this.svgTop = viewport.top * scale;
  }
}
</script>