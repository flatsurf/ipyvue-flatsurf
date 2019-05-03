import size from "lodash/size";
import keys from "lodash/keys";
import flattenDeep from "lodash/flattenDeep";
import findIndex from "lodash/findIndex";
import minBy from "lodash/minBy";
import includes from "lodash/includes";
import clone from "lodash/clone";
import Flatten from "@flatten-js/core";

export type Vertices = string[][];
export type HalfEdges = {[id: string]: string};
export type Face<T = string> = [T, T, T];
export type Faces<T = string> = Array<Face<T>>;
export type Vectors = {[id: string]: Flatten.Vector};
export type Layout = {[id: string]: Flatten.Segment};
export type Priorities = string[];

export default class Triangulation {
	constructor(vertices: Vertices, halfEdges: HalfEdges, faces: Faces, vectors: Vectors) {
		this.vertices = vertices;
		this.halfEdges = halfEdges;
		this.faces = faces;
		this.vectors = vectors;
	}

	private readonly vertices: Vertices;
	private readonly halfEdges: HalfEdges;
	private readonly faces: Faces;
	private readonly vectors: Vectors;

	public layout(priorities: Priorities) : Layout {
		const ret: Layout = {};

		while(size(ret) != size(this.halfEdges)) {
		  let reachableHalfEdges = flattenDeep(keys(size(ret) ? ret : this.halfEdges).map((he) => this.face(he))) as unknown as string[];
	
		  const bestHalfEdge = minBy(
			reachableHalfEdges.filter((halfEdge) => !(this.inOtherFace(halfEdge) in ret)),
			(halfEdge) => findIndex(priorities, (he) => he === halfEdge || he === this.inOtherFace(halfEdge)))!;
	
		  const newHalfEdge = this.inOtherFace(bestHalfEdge);
		  console.assert(!(String(newHalfEdge) in ret));
			
		  const newFace = clone(this.face(newHalfEdge))!;
		  while(newFace[0] !== newHalfEdge)
			  newFace.push(newFace.shift()!);
		  
		  let start = (ret[bestHalfEdge] || {pe: new Flatten.Point(0,0) }).pe;
		  for(const halfEdge of newFace) {
			  ret[halfEdge] = new Flatten.Segment(start, start.translate(this.vectors[halfEdge]));
			  start = start.translate(this.vectors[halfEdge]);
		  }
		}
	
		return ret;
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