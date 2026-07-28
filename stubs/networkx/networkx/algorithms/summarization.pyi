"""
Graph summarization finds smaller representations of graphs resulting in faster
runtime of algorithms, reduced storage needs, and noise reduction.
Summarization has applications in areas such as visualization, pattern mining,
clustering and community detection, and more.  Core graph summarization
techniques are grouping/aggregation, bit-compression,
simplification/sparsification, and influence based. Graph summarization
algorithms often produce either summary graphs in the form of supergraphs or
sparsified graphs, or a list of independent structures. Supergraphs are the
most common product, which consist of supernodes and original nodes and are
connected by edges and superedges, which represent aggregate edges between
nodes and supernodes.

Grouping/aggregation based techniques compress graphs by representing
close/connected nodes and edges in a graph by a single node/edge in a
supergraph. Nodes can be grouped together into supernodes based on their
structural similarities or proximity within a graph to reduce the total number
of nodes in a graph. Edge-grouping techniques group edges into lossy/lossless
nodes called compressor or virtual nodes to reduce the total number of edges in
a graph. Edge-grouping techniques can be lossless, meaning that they can be
used to re-create the original graph, or techniques can be lossy, requiring
less space to store the summary graph, but at the expense of lower
reconstruction accuracy of the original graph.

Bit-compression techniques minimize the amount of information needed to
describe the original graph, while revealing structural patterns in the
original graph.  The two-part minimum description length (MDL) is often used to
represent the model and the original graph in terms of the model.  A key
difference between graph compression and graph summarization is that graph
summarization focuses on finding structural patterns within the original graph,
whereas graph compression focuses on compressions the original graph to be as
small as possible.  **NOTE**: Some bit-compression methods exist solely to
compress a graph without creating a summary graph or finding comprehensible
structural patterns.

Simplification/Sparsification techniques attempt to create a sparse
representation of a graph by removing unimportant nodes and edges from the
graph.  Sparsified graphs differ from supergraphs created by
grouping/aggregation by only containing a subset of the original nodes and
edges of the original graph.

Influence based techniques aim to find a high-level description of influence
propagation in a large graph.  These methods are scarce and have been mostly
applied to social graphs.

*dedensification* is a grouping/aggregation based technique to compress the
neighborhoods around high-degree nodes in unweighted graphs by adding
compressor nodes that summarize multiple edges of the same type to
high-degree nodes (nodes with a degree greater than a given threshold).
Dedensification was developed for the purpose of increasing performance of
query processing around high-degree nodes in graph databases and enables direct
operations on the compressed graph.  The structural patterns surrounding
high-degree nodes in the original is preserved while using fewer edges and
adding a small number of compressor nodes.  The degree of nodes present in the
original graph is also preserved. The current implementation of dedensification
supports graphs with one edge type.

For more information on graph summarization, see `Graph Summarization Methods
and Applications: A Survey <https://dl.acm.org/doi/abs/10.1145/3186727>`_
"""

from _typeshed import Incomplete
from collections.abc import Iterable

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["dedensify", "snap_aggregation"]

@_dispatchable
def dedensify(
    G: Graph[_Node], threshold: int, prefix: str | None = None, copy: bool | None = True
) -> tuple[Graph[Incomplete], set[Incomplete]]: ...
@_dispatchable
def snap_aggregation(
    G: Graph[_Node],
    node_attributes: Iterable[Incomplete],
    edge_attributes: Iterable[Incomplete] | None = (),
    prefix: str = "Supernode-",
    supernode_attribute: str = "group",
    superedge_attribute: str = "types",
) -> Graph[Incomplete]: ...
