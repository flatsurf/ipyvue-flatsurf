<template>
  <g>
	<half-edge v-for="halfEdge in Object.keys(halfEdges)" :key="halfEdge" :edge="halfEdges[halfEdge]" :half-edge="halfEdge"
	  :class="{
		  highlight: hovered[halfEdge] || hovered[halfEdgeMap[halfEdge]],
		  selected: includes(selected, halfEdge),
	  }"

	  @click="reprioritize(halfEdge)"
	  @mouseenter="hovered[halfEdge] = true"
	  @mouseleave="hovered[halfEdge] = false"
	/>
  </g>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";
import mapValues from "lodash/mapValues";
import includes from "lodash/includes";

import Layout, { IVertices, IHalfEdges, IFaces, IVectors, IFace, IHalfEdgeLayout } from "../Layout/Triangulation";
import HalfEdge from "./Primitives/HalfEdge.vue";

@Component({
	components: { HalfEdge },
	methods: { includes }
})
export default class HalfEdges extends Vue {
  @Prop({required: true}) private halfEdges!: IHalfEdgeLayout;
  @Prop({required: true}) private halfEdgeMap!: IHalfEdges;
  @Prop({default: () => []}) private selected!: string[];

  protected hovered = mapValues(this.halfEdges, (v) => false);

  protected reprioritize(halfEdge: string) {
	this.hovered = mapValues(this.hovered, () => false);
	this.$emit('reprioritize', halfEdge)
  }
}
</script>