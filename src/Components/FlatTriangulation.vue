<template>
  <g>
  	<triangulation :polygon=layoutedPolygon.polygon />
	<half-edge v-for="halfEdge in halfEdges" :key="halfEdge" :edge="layoutedPolygon.halfEdges[halfEdge]"
	  :class="{
		  highlight: hovered[halfEdge] || hovered[halfEdges[halfEdge]],
		  selected: selected[halfEdge],
	  }"
	  @click="prioritize(halfEdge)"
	  @mouseenter="hovered[halfEdge] = true"
	  @mouseleave="hovered[halfEdge] = false"
	/>
  </g>
</template>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import values from "lodash/values";
import mapValues from "lodash/mapValues";
import Flatten from "@flatten-js/core";

import Triangulation from "./Primitives/Triangulation.vue";
import HalfEdge from "./Primitives/HalfEdge.vue";
import Layout, { Vertices, HalfEdges, Faces, Vectors, Face } from "../Layout/Triangulation";
import BBox from "../Layout/BBox";
import {transform} from "../Layout/Viewport"

@Component({
	components: { Triangulation, HalfEdge },
})
export default class FlatTriangulation extends Vue {
  @Prop({required: true}) private width!: number;
  @Prop({required: true}) private height!: number;
  @Prop({required: true}) private vertices!: Vertices;
  @Prop({required: true}) private halfEdges!: HalfEdges;
  @Prop({required: true}) private faces!: Faces;
  @Prop({required: true}) private vectors!: Vectors;

  protected priorities = Object.keys(this.halfEdges);

  protected hovered = mapValues(this.halfEdges, (v) => false);
  protected selected = mapValues(this.halfEdges, (v) => false);

  get layout() {
	return new Layout(this.vertices, this.halfEdges, this.faces, this.vectors);
  }

  get layouted() {
	return this.layout.layout(this.priorities);
  }

  get layoutedPolygon() {
	const bbox = BBox(values(this.layouted));
	const target = new Flatten.Box(0, 0, this.width, this.height);
	const scaled = mapValues(this.layouted, (p) => transform(p, bbox, target, "CENTER"));
	const polygon = new Flatten.Polygon();
	const faces = this.faces.map((face) => [face, polygon.addFace(face.map((he) => scaled[he]))] as [Face, Flatten.Face]);
	return {
	  halfEdges: scaled,
	  faces: new Map(faces),
	  polygon
	};
  }

  prioritize(halfEdge: string) {
	  this.selected[halfEdge] = true;
	  setTimeout(() => { this.selected[halfEdge] = false }, 250);
	  this.priorities.unshift(halfEdge);
  }
}
</script>
<style scoped>


line.selected {
	stroke: green;
	stroke-dasharray: 10px;
}

line.selectedInOtherFace {
	stroke: red;
}

line {
	transition: all 1s eas-in-out;
}
</style>