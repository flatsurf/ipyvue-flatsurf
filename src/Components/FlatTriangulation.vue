<!--
TODO: Make all naming ressemble here the naming in libpolygon, i.e., things such as half-edge-map are not consistent.
-->
<template>
  <g>
  	<triangulation :polygon=layoutedPolygon.polygon />
	<saddle-connections :saddle-connections="saddleConnections" :layout="layoutedSaddleConnections" />
	<half-edges :half-edges="layoutedPolygon.halfEdges" :selected="selectedHalfEdges" :half-edge-map="halfEdges"
	  @reprioritize=reprioritize />
	<vertices :half-edges="layoutedPolygon.halfEdges" :vertices="vertices" :vectors="vectors" />
  </g>
</template>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import values from "lodash/values";
import mapValues from "lodash/mapValues";
import findIndex from "lodash/findIndex";
import includes from "lodash/includes";
import zip from "lodash-es/zip";
import Flatten from "@flatten-js/core";

import Triangulation from "./Primitives/Triangulation.vue";
import HalfEdges from "./HalfEdges.vue";
import Vertices from "./Vertices.vue";
import SaddleConnections from "./SaddleConnections.vue";
import Layout, { IVertices, IHalfEdges, IFaces, IVectors, IFace } from "../Layout/Triangulation";
import { layout as layoutSaddleConnection, ISaddleConnection } from "../Layout/SaddleConnection";
import BBox from "../Layout/BBox";
import Viewport from "./Shared/Viewport"

@Component({
	components: { Triangulation, HalfEdges, Vertices, SaddleConnections },
})
export default class FlatTriangulation extends Vue {
  @Prop({required: true}) private width!: number;
  @Prop({required: true}) private height!: number;
  @Prop({required: true}) private vertices!: IVertices;
  @Prop({required: true}) private halfEdges!: IHalfEdges;
  @Prop({required: true}) private faces!: IFaces;
  @Prop({required: true}) private vectors!: IVectors;
  @Prop({default: () => []}) private saddleConnections!: ISaddleConnection[];

  protected priorities = Object.keys(this.halfEdges);
  protected selectedHalfEdges : string[] = [];

  get layout() {
	return new Layout(this.vertices, this.halfEdges, this.faces, this.vectors);
  }

  get layouted() {
    return this.layout.layout(this.priorities);
  }

  get sourceViewport() {
	return new Viewport(BBox(values(this.layouted.layout)), true);
  }

  get targetViewport() {
	return new Viewport(new Flatten.Box(0, 0, this.width, this.height), false);
  }

  get layoutedPolygon() {
	const scaled = mapValues(this.layouted.layout, (p) => this.sourceViewport.transform(p, this.targetViewport, "CENTER"));
	const polygon = new Flatten.Polygon();
	const faces = this.faces.map((face) => [face, polygon.addFace(face.map((he) => scaled[he]))] as [IFace, Flatten.Face]);
	return {
	  halfEdges: scaled,
	  faces: new Map(faces),
	  polygon,
	};
  }

  get layoutedSaddleConnections() {
	return this.saddleConnections.map((sc) => layoutSaddleConnection(sc, this.layouted, this.halfEdges))
		.map((layout) => { return {
			direction: this.sourceViewport.transform(layout.direction, this.targetViewport, "CENTER"),
			segments: layout.segments.map((segment) => this.sourceViewport.transform(segment, this.targetViewport, "CENTER")),
		}});
  }

  reprioritize(halfEdge: string) {
	  console.log(halfEdge);
	  const isGlued = includes(this.layouted.glueings, halfEdge);

	  this.selectedHalfEdges = [halfEdge]
	  if (isGlued) {
		  this.selectedHalfEdges = [...this.selectedHalfEdges, this.halfEdges[halfEdge]];
	  }
	  setTimeout(() => { this.selectedHalfEdges = [] }, 300);

	  const oldPriorities = this.priorities.filter((he) => he !== halfEdge && he !== this.halfEdges[halfEdge]);
	  if (isGlued) {
		  this.priorities = [...oldPriorities, halfEdge, this.halfEdges[halfEdge]];
	  } else {
		  this.priorities = [halfEdge, this.halfEdges[halfEdge], ...oldPriorities];
	  }
  }
}
</script>