<template>
	<g class="saddle-connection" :class="{selected}">
		<extended-click-area class="vector" @click="selected = !selected">
			<arrow :segment="layout.direction" />
		</extended-click-area>
		<g class="flow">
			<line v-for="(segment, i) in layout.segments" :key="i"
				:x1="segment.start.x" :x2="segment.end.x"
				:y1="segment.start.y" :y2="segment.end.y" />
		</g>
	</g>
</template>
<script lang="ts">
import { Prop, Vue, Component } from "vue-property-decorator";

import { ILayoutedSaddleConnection, ISaddleConnection } from "../../Layout/SaddleConnection";
import ExtendedClickArea from "../Shared/ExtendedClickArea.vue";
import Arrow from "../Shared/SVGArrow.vue";

@Component({
	components: { ExtendedClickArea, Arrow }
})
export default class SaddleConnection extends Vue {
	@Prop({required: true, type: Object}) private saddleConnection!: ISaddleConnection;
	@Prop({required: true, type: Object}) private layout!: ILayoutedSaddleConnection;

	protected selected: boolean = false;
}
</script>
<style lang="scss">
.flatsurf {
	.vector {
		stroke-width: 2px;
		stroke: rgba(#a6761d, .2);
		fill: rgba(#a6761d, .2);
	}

	.vector:hover {
		stroke-width: 3px;
		stroke: rgba(#a6761d, .5);
		fill: rgba(#a6761d, .5);
		cursor: pointer;
	}

	.selected .vector {
		stroke-width: 3px;
		stroke: #a6761d;
		fill: #a6761d;
	}

	.flow line {
		stroke-width: 2px;
		stroke: rgba(#e6ab02, .2);
	}

	.vector:hover ~ .flow line {
		stroke: rgba(#e6ab02, .5);
	}

	.selected .flow line {
		stroke: #e6ab02 !important;
	}
}
</style>

