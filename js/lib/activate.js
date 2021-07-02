import { Vue } from "jupyter-vue";
import { SurfaceViewer } from "vue-flatsurf";

export function activate(app, widget) {
  // Register flatsurf components as tags with Vue.js.
  Vue.component("surface-viewer", SurfaceViewer);
}
