<template>
  <resizable-widget class="flatsurf" :initial-height="height" @resize="resize">
	<pan-zoom-widget :client-viewport="clientViewport" @pan-zoom="moved" :cartesian="true" >
		<svg :height="height" width="100%">
			<g :transform="svgTranslation">
					<flat-triangulation :width="clientViewport.width * svgScale" :height="clientViewport.height * svgScale"
						:vertices=vertices :halfEdges=halfEdges :faces=faces :vectors=vectors
						:saddle-connections=saddleConnections />
			</g>
		</svg>
	</pan-zoom-widget>
  </resizable-widget>
</template>
<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
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

  get halfEdges() {
	  return transform(this.vectors, (result, value, key) => (result as string[])[Number(key)] = String(-Number(key)));
  }

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

/*
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

  get saddleConnections() {
	  return [];
		  // TODO: Should we keep the weird semantics of target? (see saddle_connection.hpp)
		  { source: "11", target: "3", vector: new Flatten.Vector(6.00339,5.19811), crossings: ["12", "-2", "12", "-4", "5", "-10"] },
		  { source: "-5", target: "-2", vector: new Flatten.Vector(6.00339, 5.19811), crossings: ["-10", "9", "-11", "12", "-2", "12"] }
	  ]
  }
*/

  get vertices() {
	  return [[-18, 7, 14, -13, 5, 12, -11, -8, 17, -16, 6, 15, -14, 1, -10, -12, -3, 18, -17, -9, 13, -15, 4, 11, 10, -2, 16], [-7, 3, -5, 9, 8, -4, -6, 2, -1]]
	  	.map((v) => v.map((he) => String(he)));
  }

  get faces() {
	  return [[-18, -3, -7], [-17, -8, 9], [-16, -2, -6], [-15, 6, -4], [-14, 7, -1], [-13, -9, -5], [-12, 5, 3], [-11, 4, 8], [-10, 11, 12], [1, 2, 10], [13, 14, 15], [16, 17, 18]]
		.map((v) => v.map((he) => String(he)));
  }

  get vectors() {
	  const data = {
		  [1]: [-0.673648,-0.565258], [2]: [0.673648,-0.565258], [3]: [-0.826352,-0.300767], [4]: [0.826352,-0.300767],
		  [5]: [-0.152704,0.866025], [6]: [0.439693,0.76157], [7]: [0.439693,-0.76157], [8]: [0.152704,0.866025],
		  [9]: [0.879385,0], [10]: [0,1.13052], [11]: [0.979055,0.565258], [12]: [-0.979055,0.565258],
		  [13]: [-0.726682,-0.866025], [14]: [1.11334,-0.196312], [15]: [-0.386659,1.06234], [16]: [-1.11334,-0.196312],
		  [17]: [0.726682,-0.866025], [18]: [0.386659,1.06234]
	  } as any;
	  for (let he in data) {
		  data[-Number(he)] = [-data[he][0], -data[he][1]];
	  }
	  return mapValues(data, (v) => new Flatten.Vector(v[0], v[1]));
  }

  get saddleConnections() {
	  return [
		  { source: "-3", target: "5", vector: new Flatten.Vector(3.43969, 2.49362), crossings: ["-7", "-14", "15", "6", "-2", "10", "12"] },
		  { source: "11", target: "18", vector: new Flatten.Vector(8.70961, 6.31407), crossings: ["12", "5", "-13", "15", "-4", "8", "-17", "16", "-2", "10", "12", "5", "-9", "-17", "18", "-7", "-14", "15", "-4", "8", "-17"]}
	  ]
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
