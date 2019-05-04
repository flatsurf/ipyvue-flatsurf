import Flatten from "@flatten-js/core";
import clone from "lodash-es/clone";
import contains from "lodash-es/includes";

import { ILayout, IHalfEdges } from "./Triangulation";

// TODO: Cleanup naming of the types and variable names here and in the other Triangulation code.
// TODO: Alias HalfEdge to string where appropriate.

export type ISaddleConnection = {
	source: string,
	target: string,
	vector: Flatten.Vector,
	crossings: string[],
};

export type ILayoutedSaddleConnection = {
	segments: Flatten.Segment[],
	direction: Flatten.Segment,
}

export function layout(saddleConnection: ISaddleConnection, triangulation: ILayout, halfEdges: IHalfEdges) {
	const segments: Flatten.Segment[] = [];
	let start = triangulation.layout[saddleConnection.source].start;
	const direction = new Flatten.Segment(start, start.translate(saddleConnection.vector));
	const crossings = clone(saddleConnection.crossings);
	while(crossings.length) {
		const crossing = crossings.shift()!;
		if (contains(triangulation.glueings, crossing)) {
			continue;
		}

		// Since this half edge is not glued, we compute the intersection of our ray with it and add it to segments.
		const line = new Flatten.Line(start, start.translate(saddleConnection.vector));
		const crossingEdge = triangulation.layout[crossing];
		const crossingLine = new Flatten.Line(crossingEdge.start, crossingEdge.end);
		const intersection = line.intersect(crossingLine);
		console.assert(intersection.length === 1);
		const segment = new Flatten.Segment(start, intersection[0]);
		segments.push(segment);

		// Now, we move the intersection point to the corresponding half-edge and repeat.
		const alongHalfEdge = new Flatten.Vector(crossingEdge.start, segment.end);
		start = triangulation.layout[halfEdges[crossing]].end.translate(alongHalfEdge);
	}

	const target = triangulation.layout[saddleConnection.target].end;
	segments.push(new Flatten.Segment(start, target));

	return { 
		segments,
		direction
	}
}