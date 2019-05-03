<template>
  <g>
	<vertex-flow v-if="active" :half-edge="halfEdges[active]" :angle="addAngle" :atRest="addAngle === 0" />
	<vertex-flow v-if="active && addAngle === 0" :half-edge="halfEdges[nextEdge(active, -1)]" :angle="angle(nextEdge(active, -1))" :atRest="addAngle === 0" />
	<vertex v-for="halfEdge in Object.keys(halfEdges)" :key="halfEdge" :vertex="halfEdges[halfEdge].ps"
	  :class="{
		   highlight: hovered[vertex(halfEdge)],
	  }"
	  @mouseenter="hover(halfEdge)" @mouseleave="unhover(halfEdge)"
	/>
  </g>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";
import mapValues from "lodash-es/mapValues";
import findIndex from "lodash-es/findIndex";
import includes from "lodash-es/includes";
import clone from "lodash-es/clone";
import sum from "lodash-es/sum";
import { TweenLite, TimelineLite, Power0 } from "gsap";

import { IVertices, IHalfEdgeLayout } from "../Layout/Triangulation";
import Vertex from "./Primitives/Vertex.vue";
import VertexFlow from "./Primitives/VertexFlow.vue";

@Component({
	components: { Vertex, VertexFlow },
})
export default class Vertices extends Vue {
  @Prop({required: true}) private vertices!: IVertices;
  @Prop({required: true}) private halfEdges!: IHalfEdgeLayout;

  protected hovered = this.vertices.map(() => false);
  protected active : string | null = null;
  protected addAngle = 0;
  protected timeline : TimelineLite | null = null;

  hover(halfEdge: string) {
	  this.unhover(halfEdge);
	  const vertex = this.vertex(halfEdge);
	  this.hovered[vertex] = true;

	  const atVertex = clone(this.vertices[vertex]);
	  while(atVertex[0] !== halfEdge)
		atVertex.unshift(atVertex.pop()!);
		
	  this.timeline = new TimelineLite();

	  for(const edge of atVertex) {
		  const angle = this.angle(edge);
		  this.timeline.add( () => { this.active = edge; this.addAngle = 0; });
		  this.timeline.add( TweenLite.to(this, 3.141/12, { addAngle: angle, delay: 0.3, ease: Power0.easeInOut}) );
	  }
	  this.timeline.add( () => { this.timeline!.restart(); });
  }

  angle(halfEdge: string) {
	  const vertex = this.vertex(halfEdge);
	  const nextHalfEdge = this.nextEdge(halfEdge);
	  return this.halfEdges[halfEdge].tangentInStart().angleTo(
		this.halfEdges[nextHalfEdge].tangentInStart());
  }

  unhover(halfEdge: string) {
	  if (this.timeline != null)
		  this.timeline.kill();
	  this.addAngle = 0;
	  this.active = null;
	  this.hovered = this.vertices.map(() => false);
  }

  vertex(halfEdge: string) {
	const vertex = findIndex(this.vertices, (v) => includes(v, halfEdge));
	console.assert(vertex !== -1);
	return vertex;
  }

  nextEdge(halfEdge: string, delta?: number): string {
	if (delta === 0)
		return halfEdge;
	if (delta === undefined)
		delta = 1;

	const vertex = this.vertex(halfEdge);
	const outEdges = this.vertices[vertex];
	if (delta < 0)
		return this.nextEdge(halfEdge, outEdges.length + delta);
	const nextHalfEdge = outEdges[(outEdges.indexOf(halfEdge) + 1) % outEdges.length];
	return this.nextEdge(nextHalfEdge, delta - 1);
  }
}
</script>
