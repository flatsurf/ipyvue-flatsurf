import size from "lodash/size";
import keys from "lodash/keys";
import flattenDeep from "lodash/flattenDeep";
import findIndex from "lodash/findIndex";
import minBy from "lodash/minBy";
import includes from "lodash/includes";
import clone from "lodash/clone";
import Flatten from "@flatten-js/core";

export type IVertices = string[][];
export type IHalfEdges = {[id: string]: string};
export type IFace<T = string> = [T, T, T];
export type IFaces<T = string> = Array<IFace<T>>;
export type IVectors = {[id: string]: Flatten.Vector};
export type IGlueings = string[];
export type IHalfEdgeLayout = {[id: string]: Flatten.Segment};
export type ILayout = {
	layout: IHalfEdgeLayout,
	glueings: IGlueings,
};
export type IPriorities = string[];

export default class Triangulation {
	constructor(vertices: IVertices, halfEdges: IHalfEdges, faces: IFaces, vectors: IVectors) {
		this.vertices = vertices;
		this.halfEdges = halfEdges;
		this.faces = faces;
		this.vectors = vectors;
	}

	private readonly vertices: IVertices;
	private readonly halfEdges: IHalfEdges;
	private readonly faces: IFaces;
	private readonly vectors: IVectors;

	public layout(priorities: IPriorities) : ILayout {
		const layout: IHalfEdgeLayout = {};
		const glueings: IGlueings = [];

		while(size(layout) != size(this.halfEdges)) {
		  let reachableHalfEdges = flattenDeep(keys(size(layout) ? layout : this.halfEdges).map((he) => this.face(he))) as unknown as string[];
	
		  const bestHalfEdge = minBy(
			reachableHalfEdges.filter((halfEdge) => !(this.inOtherFace(halfEdge) in layout)),
			(halfEdge) => findIndex(priorities, (he) => he === halfEdge || he === this.inOtherFace(halfEdge)))!;

		  const newHalfEdge = this.inOtherFace(bestHalfEdge);
		  console.assert(!(String(newHalfEdge) in layout));

		  if (Object.keys(layout).length) {
		  	glueings.push(bestHalfEdge);
			glueings.push(newHalfEdge);
		  }
			
		  const newFace = clone(this.face(newHalfEdge))!;
		  while(newFace[0] !== newHalfEdge)
			  newFace.push(newFace.shift()!);
		  
		  let start = (layout[bestHalfEdge] || {pe: new Flatten.Point(0,0) }).pe;
		  for(const halfEdge of newFace) {
			  layout[halfEdge] = new Flatten.Segment(start, start.translate(this.vectors[halfEdge]));
			  start = start.translate(this.vectors[halfEdge]);
		  }
		}
	
		return { layout, glueings };
	}

	private face(halfEdge: string) {
		console.assert(halfEdge in this.halfEdges, halfEdge);
		return this.faces.find((face) => includes(face, halfEdge))!;
	}
  
	private inOtherFace(halfEdge: string) {
		console.assert(halfEdge in this.halfEdges, halfEdge);
		return this.halfEdges[Number(halfEdge)];
	}
}
