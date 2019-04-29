<template>
  <div>
    <h1>{{ value }} !</h1>
  </div>
</template>
<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  props: ["value"],
});
</script>

