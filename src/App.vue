<template>
  <resizable-widget class="flatsurf" :initial-height="height" @resize="resize">
	<pan-zoom-widget :client-viewport="clientViewport" @pan-zoom="moved">
		<svg :height="height" width="100%">
			<g :transform="svgTranslation">
				<flat-triangulation :width="clientViewport.width * svgScale" :height="clientViewport.height * svgScale" :vertices=vertices :halfEdges=halfEdges :faces=faces :vectors=vectors />
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
import mapValues from "lodash/mapValues";
import transform from "lodash/transform";

@Component({
	components: { FlatTriangulation, ResizableWidget, PanZoomWidget },
})
export default class App extends Vue {
  @Prop({required: true}) public value!: string;
  @Prop({default: 200}) public initialHeight!: number;
  @Prop({default: 5}) public padding!: number;

/*
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
*/

  get vertices() {
	  return [["-12", "4", "-6", "-1", "-8", "6", "-5", "3", "-10", "5", "-4", "2"],["-11", "7", "1", "8", "-7", "9", "-3", "10", "-9", "11", "-2", "12"]];
  }

  get halfEdges() {
	  return transform(this.vectors, (r, v, k) => r[k] = String(-Number(k)));
  }

  get faces() {
	  return [["-12", "-2", "-4"], ["-11", "-9", "-7"], ["-10", "-3", "-5"], ["-8", "1", "-6"], ["-1", "7", "8"], ["2", "11", "12"], ["3", "9", "10"], ["4", "5", "6"]];
  }

  get vectors() {
	  const data = {
		  [1]: [1,0], [2]: [0.5,-0.866025], [3]: [0.5,0.866025], [4]: [3.0017,1.73303], [5]: [-3.0017,1.73303], [6]: [0,-3.46606],
		  [7]: [0,-3.46606], [8]: [1,3.46606], [9]: [-3.0017,1.73303], [10]: [2.5017,-2.59906], [11]: [3.0017,1.73303], [12]: [-3.5017,-0.867005],
	  } as any;
	  for (let he in data) {
		  data[-Number(he)] = [-data[he][0], -data[he][1]];
	  }
	  return mapValues(data, (v) => new Flatten.Vector(v[0], v[1]));
  }

  protected height: number = this.initialHeight;
  protected width: number = this.initialHeight;

  get clientViewport() {
	  return { width: this.width - 2*this.padding, height: this.height - 2*this.padding };
  }

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
	const scale = this.clientViewport.width / viewport.width;
	this.svgScale = scale;
	this.svgLeft = viewport.left * scale;
	this.svgTop = viewport.top * scale;
  }
}
</script>