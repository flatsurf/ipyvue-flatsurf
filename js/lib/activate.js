import { Vue } from "jupyter-vue";
import FlatSurface from "./flatsurf";

export function activate(app, widget) {
  // Register <flatsurf/> as a tag with Vue.js.
  Vue.component("flatsurf", FlatSurface);
}
