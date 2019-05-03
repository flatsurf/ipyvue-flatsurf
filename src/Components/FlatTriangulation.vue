<template>
  <g>
  	<triangulation :polygon=layoutedPolygon.polygon />
	<half-edge v-for="halfEdge in halfEdges" :key="halfEdge" :edge="layoutedPolygon.halfEdges[halfEdge]"
	  :class="{
		  highlight: hoveredHalfEdge[halfEdge] || hoveredHalfEdge[halfEdges[halfEdge]],
		  selected: selectedHalfEdge[halfEdge],
	  }"
	  @click="reprioritize(halfEdge)"
	  @mouseenter="hoveredHalfEdge[halfEdge] = true"
	  @mouseleave="hoveredHalfEdge[halfEdge] = false"
	/>
	<vertex v-for="halfEdge in halfEdges" :key="'v' + halfEdge" :vertex="layoutedPolygon.halfEdges[halfEdge].ps"
	  :class="{
		   highlight: hoveredVertex[vertex(halfEdge)],
	  }"
	  @mouseenter="hoveredVertex[vertex(halfEdge)] = true"
	  @mouseleave="hoveredVertex[vertex(halfEdge)] = false"
	/>
  </g>
</template>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import values from "lodash/values";
import mapValues from "lodash/mapValues";
import findIndex from "lodash/findIndex";
import includes from "lodash/includes";
import Flatten from "@flatten-js/core";

import Triangulation from "./Primitives/Triangulation.vue";
import HalfEdge from "./Primitives/HalfEdge.vue";
import Vertex from "./Primitives/Vertex.vue";
import Layout, { Vertices, HalfEdges, Faces, Vectors, Face } from "../Layout/Triangulation";
import BBox from "../Layout/BBox";
import {transform} from "../Layout/Viewport"

@Component({
	components: { Triangulation, HalfEdge, Vertex },
})
export default class FlatTriangulation extends Vue {
  @Prop({required: true}) private width!: number;
  @Prop({required: true}) private height!: number;
  @Prop({required: true}) private vertices!: Vertices;
  @Prop({required: true}) private halfEdges!: HalfEdges;
  @Prop({required: true}) private faces!: Faces;
  @Prop({required: true}) private vectors!: Vectors;

  protected priorities = Object.keys(this.halfEdges);

  protected hoveredHalfEdge = mapValues(this.halfEdges, (v) => false);
  protected hoveredVertex = mapValues({...this.vertices}, (v) => false);
  protected selectedHalfEdge = mapValues(this.halfEdges, (v) => false);

  get layout() {
	return new Layout(this.vertices, this.halfEdges, this.faces, this.vectors);
  }

  get layouted() {
	return this.layout.layout(this.priorities);
  }

  get layoutedPolygon() {
	const bbox = BBox(values(this.layouted.layout));
	const target = new Flatten.Box(0, 0, this.width, this.height);
	const scaled = mapValues(this.layouted.layout, (p) => transform(p, bbox, target, "CENTER"));
	const polygon = new Flatten.Polygon();
	const faces = this.faces.map((face) => [face, polygon.addFace(face.map((he) => scaled[he]))] as [Face, Flatten.Face]);
	return {
	  halfEdges: scaled,
	  faces: new Map(faces),
	  polygon
	};
  }

  vertex(halfEdge: string) {
	return findIndex(this.vertices, (v) => includes(v, halfEdge));
  }

  reprioritize(halfEdge: string) {
	  const isGlued = includes(this.layouted.glueings, halfEdge);

	  this.selectedHalfEdge[halfEdge] = true;
	  setTimeout(() => { this.selectedHalfEdge[halfEdge] = false }, 250);
	  if (isGlued) {
		this.selectedHalfEdge[this.halfEdges[halfEdge]] = true;
		setTimeout(() => { this.selectedHalfEdge[this.halfEdges[halfEdge]] = false }, 250);  
	  }

	  const oldPriorities = this.priorities.filter((he) => he !== halfEdge && he !== this.halfEdges[halfEdge]);
	  if (isGlued) {
		  this.priorities = [...oldPriorities, halfEdge, this.halfEdges[halfEdge]];
	  } else {
		  this.priorities = [halfEdge, this.halfEdges[halfEdge], ...oldPriorities];
	  }
	  
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