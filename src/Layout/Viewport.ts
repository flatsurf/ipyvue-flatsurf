import Flatten from "@flatten-js/core";

function width(box: Flatten.Box) { return box.xmax - box.xmin; }
function height(box: Flatten.Box) { return box.ymax - box.ymin; }

export function transform(segment: Flatten.Segment, sourceViewPort: Flatten.Box, targetViewPort: Flatten.Box, aspectRatio: "CENTER" | "IGNORE") : Flatten.Segment;
export function transform(segment: Flatten.Point, sourceViewPort: Flatten.Box, targetViewPort: Flatten.Box, aspectRatio: "CENTER" | "IGNORE") : Flatten.Point;
export function transform(point: Flatten.Segment | Flatten.Point, sourceViewPort: Flatten.Box, targetViewPort: Flatten.Box, aspectRatio: "CENTER" | "IGNORE") {
    if (point instanceof Flatten.Segment) {
		return new Flatten.Segment(transform(point.ps, sourceViewPort, targetViewPort, aspectRatio), transform(point.pe, sourceViewPort, targetViewPort, aspectRatio));
	}

	const pointInSource = point.translate(-sourceViewPort.xmin, -sourceViewPort.ymin);

	let xscale = width(targetViewPort) / width(sourceViewPort);
	let yscale = height(targetViewPort) / height(sourceViewPort);
	if (aspectRatio === "CENTER") {
		xscale = yscale = Math.min(xscale, yscale);

	}

	const pointInTarget = new Flatten.Point(
		pointInSource.x * xscale,
		pointInSource.y * yscale);

	let delta = new Flatten.Vector(targetViewPort.xmin, targetViewPort.ymin);
	if (aspectRatio === "CENTER"){
		delta.x += (width(targetViewPort) - width(sourceViewPort) * xscale) / 2;
		delta.y += (height(targetViewPort) - height(sourceViewPort) * yscale) / 2;
	}
	return pointInTarget.translate(delta);
}