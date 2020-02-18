<template>
    <g>
		  <saddle-connection v-for="(connection, i) in saddleConnections" :key="i"
		    :saddle-connection="connection"
		    :layout="layout[i]"
		  />
  	</g>
</template>
<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

import { ISaddleConnection, ILayoutedSaddleConnection } from "../Layout/SaddleConnection";
import SaddleConnection from "./Primitives/SaddleConnection.vue";

@Component({
	components: {SaddleConnection}
})
export default class SaddleConnections extends Vue {
	@Prop({required: true, type: Array}) private saddleConnections!: ISaddleConnection[];
	@Prop({required: true, type: Array}) private layout!: ILayoutedSaddleConnection[];
}
</script>
