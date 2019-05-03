<template>
  <g>
	<vertex v-for="halfEdge in Object.keys(halfEdges)" :key="halfEdge" :vertex="halfEdges[halfEdge].ps"
	  :class="{
		   highlight: hovered[vertex(halfEdge)],
	  }"
	  @mouseenter="hovered[vertex(halfEdge)] = true"
	  @mouseleave="hovered[vertex(halfEdge)] = false"
	/>
  </g>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";
import mapValues from "lodash-es/mapValues";
import findIndex from "lodash-es/findIndex";
import includes from "lodash-es/includes";

import { IVertices, IHalfEdgeLayout } from "../Layout/Triangulation";
import Vertex from "./Primitives/Vertex.vue";

@Component({
	components: { Vertex },
})
export default class Vertices extends Vue {
  @Prop({required: true}) private vertices!: IVertices;
  @Prop({required: true}) private halfEdges!: IHalfEdgeLayout;

  protected hovered = mapValues({...this.vertices}, (v) => false);

  vertex(halfEdge: string) {
	return findIndex(this.vertices, (v) => includes(v, halfEdge));
  }
}
</script>
