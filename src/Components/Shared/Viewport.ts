import Flatten from "@flatten-js/core";

function flip(box: Flatten.Box) : Flatten.Box;
function flip(point: Flatten.Point) : Flatten.Point;
function flip(shape: Flatten.Point | Flatten.Box) {
	if (shape instanceof Flatten.Box) {
		return new Flatten.Box(shape.xmin, -shape.ymax, shape.xmax, -shape.ymin);
	} else {
		return shape.transform(new Flatten.Matrix(1, 0, 0, -1));
	}
}

export default class Viewport {
    constructor(bounds: Flatten.Box, cartesian: boolean) {
		this.bounds = bounds;
		this.cartesian = cartesian;
	}

	// Whether the coordinate system positively oriented (like Mathematicians come to expect)
	// or not (like Computer Scientists are used to.)
	public readonly cartesian: boolean;
	public readonly bounds: Flatten.Box;

	get width() {
		return this.bounds.xmax - this.bounds.xmin;
	}

	get height() {
		return this.bounds.ymax - this.bounds.ymin;
	}

	public flip() {
		return new Viewport(flip(this.bounds), !this.cartesian);
	}

	public transform(segment: Flatten.Segment, target: Viewport, aspectRatio: "CENTER" | "IGNORE") : Flatten.Segment;
	public transform(point: Flatten.Point, target: Viewport, aspectRatio: "CENTER" | "IGNORE") : Flatten.Point;
	public transform(shape: Flatten.Segment | Flatten.Point, target: Viewport, aspectRatio: "CENTER" | "IGNORE") {
		if (shape instanceof Flatten.Segment) {
			return new Flatten.Segment(
				this.transform(shape.ps, target, aspectRatio),
				this.transform(shape.pe, target, aspectRatio));
		}
		if (!this.cartesian) {
			return this.flip().transform(flip(shape), target, aspectRatio);
		}
		if (!target.cartesian) {
			return flip(this.transform(shape, target.flip(), aspectRatio));
		}
	
		const pointInSource = shape.translate(-this.bounds.xmin, -this.bounds.ymin);
	
		let xscale = target.width / this.width;
		let yscale = target.height / this.height;
		if (aspectRatio === "CENTER") {
			xscale = yscale = Math.min(xscale, yscale);
	
		}
	
		const pointInTarget = new Flatten.Point(
			pointInSource.x * xscale,
			pointInSource.y * yscale);
	
		let delta = new Flatten.Vector(target.bounds.xmin, target.bounds.ymin);
		if (aspectRatio === "CENTER"){
			delta.x += (target.width - this.width * xscale) / 2;
			delta.y += (target.height - this.height * yscale) / 2;
		}
		return pointInTarget.translate(delta);	
	};
}