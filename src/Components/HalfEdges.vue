<template>
  <g>
	<half-edge v-for="halfEdge in Object.keys(halfEdges)" :key="halfEdge" :edge="halfEdges[halfEdge]" :half-edge="halfEdge"
	  :class="{
		  highlight: (hovered[halfEdge] || hovered[halfEdgeMap[halfEdge]])
		    && !includes(selected, halfEdge) && !includes(selected, halfEdgeMap[halfEdge]),
		  selected: includes(selected, halfEdge),
	  }"
	  :indicator="indicator[halfEdge]"

	  @click="reprioritize(halfEdge)"
	  @mouseenter="hover(halfEdge)"
	  @mouseleave="unhover(halfEdge)"
      @mousemove="(x) => mousemove(halfEdge, x)"
	/>
  </g>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Flatten from "@flatten-js/core";
import mapValues from "lodash/mapValues";
import includes from "lodash/includes";

import Layout, { IVertices, IHalfEdges, IFaces, IVectors, IFace, IHalfEdgeLayout, IGlueings } from "../Layout/Triangulation";
import HalfEdge from "./Primitives/HalfEdge.vue";

@Component({
	components: { HalfEdge },
	methods: { includes }
})
export default class HalfEdges extends Vue {
  @Prop({required: true}) private halfEdges!: IHalfEdgeLayout;
  @Prop({required: true}) private glueings!: IGlueings;
  @Prop({required: true}) private halfEdgeMap!: IHalfEdges;
  @Prop({default: () => []}) private selected!: string[];

  protected hovered = mapValues(this.halfEdges, (v) => false);
  protected indicator = mapValues(this.halfEdges, (v) => null as number | null);

  protected reprioritize(halfEdge: string) {
	this.hovered = mapValues(this.hovered, () => false);
	this.indicator = mapValues(this.indicator, () => null);
	this.$emit('reprioritize', halfEdge)
  }

  protected unhover(halfEdge: string) {
	this.hovered[halfEdge] = false;
	this.indicator[halfEdge] = null;
	this.indicator[this.halfEdgeMap[halfEdge]] = null;
  }
  
  protected hover(halfEdge: string) {
	this.hovered[halfEdge] = true;
	this.indicator[halfEdge] = null;
	this.indicator[this.halfEdgeMap[halfEdge]] = null;
  }

  protected mousemove(halfEdge: string, relative: number) {
	if (this.hovered[halfEdge] && !includes(this.glueings, halfEdge)) {
		this.indicator[halfEdge] = relative;
		this.indicator[this.halfEdgeMap[halfEdge]] = 1 - relative;
	}
  }
}
</script>