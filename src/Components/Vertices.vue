<template>
  <g>
	<vertex-flow v-if="active" :half-edge="halfEdges[active]" :angle="addAngle" />
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
		  this.timeline.add( TweenLite.to(this, 3.141/8, { addAngle: angle, delay: 0.3, ease: Power0.easeInOut}) );
	  }
	  this.timeline.add( () => { this.timeline!.restart(); });
  }

  angle(halfEdge: string) {
	  const vertex = this.vertex(halfEdge);
	  const vertices = this.vertices[vertex];
	  const nextHalfEdge = vertices[(vertices.indexOf(halfEdge) + 1) % vertices.length];
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
}
</script>
