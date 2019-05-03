import Flatten from "@flatten-js/core";
import min from "lodash/min";
import max from "lodash/max";
import flatten from "lodash/flatten";

export default function bbox(items: Array<Flatten.Point | Flatten.Segment>) {
	const points = flatten(items.map((item) => item instanceof Flatten.Point ? item : [item.ps, item.pe]));

	return new Flatten.Box(
		min(points.map((p) => p.x)),
		min(points.map((p) => p.y)),
		max(points.map((p) => p.x)),
		max(points.map((p) => p.y))
	);
}