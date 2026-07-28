"""Various small and named graphs, together with some compact generators."""

from _typeshed import Incomplete

from networkx.classes.graph import Graph
from networkx.utils.backends import _dispatchable

__all__ = [
    "LCF_graph",
    "bull_graph",
    "chvatal_graph",
    "cubical_graph",
    "desargues_graph",
    "diamond_graph",
    "dodecahedral_graph",
    "frucht_graph",
    "generalized_petersen_graph",
    "heawood_graph",
    "hoffman_singleton_graph",
    "house_graph",
    "house_x_graph",
    "icosahedral_graph",
    "krackhardt_kite_graph",
    "moebius_kantor_graph",
    "octahedral_graph",
    "pappus_graph",
    "petersen_graph",
    "sedgewick_maze_graph",
    "tetrahedral_graph",
    "truncated_cube_graph",
    "truncated_tetrahedron_graph",
    "tutte_graph",
]

@_dispatchable
def LCF_graph(n: int, shift_list: list[Incomplete], repeats: int, create_using=None) -> Graph[Incomplete]:
    """
    Return the cubic graph specified in LCF notation.

    LCF (Lederberg-Coxeter-Fruchte) notation[1]_ is a compressed
    notation used in the generation of various cubic Hamiltonian
    graphs of high symmetry. See, for example, `dodecahedral_graph`,
    `desargues_graph`, `heawood_graph` and `pappus_graph`.

    Nodes are drawn from ``range(n)``. Each node ``n_i`` is connected with
    node ``n_i + shift % n`` where ``shift`` is given by cycling through
    the input `shift_list` `repeat` s times.

    Parameters
    ----------
    n : int
       The starting graph is the `n`-cycle with nodes ``0, ..., n-1``.
       The null graph is returned if `n` < 1.

    shift_list : list
       A list of integer shifts mod `n`, ``[s1, s2, .., sk]``

    repeats : int
       Integer specifying the number of times that shifts in `shift_list`
       are successively applied to each current node in the n-cycle
       to generate an edge between ``n_current`` and ``n_current + shift mod n``.

    Returns
    -------
    G : Graph
       A graph instance created from the specified LCF notation.

    Examples
    --------
    The utility graph $K_{3,3}$

    >>> G = nx.LCF_graph(6, [3, -3], 3)
    >>> G.edges()
    EdgeView([(0, 1), (0, 5), (0, 3), (1, 2), (1, 4), (2, 3), (2, 5), (3, 4), (4, 5)])

    The Heawood graph:

    >>> G = nx.LCF_graph(14, [5, -5], 7)
    >>> nx.is_isomorphic(G, nx.heawood_graph())
    True

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/LCF_notation
    """
    ...
@_dispatchable
def bull_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Bull Graph

    The Bull Graph has 5 nodes and 5 edges. It is a planar undirected
    graph in the form of a triangle with two disjoint pendant edges [1]_
    The name comes from the triangle and pendant edges representing
    respectively the body and legs of a bull.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        A bull graph with 5 nodes

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Bull_graph.
    """
    ...
@_dispatchable
def chvatal_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Chvátal Graph

    The Chvátal Graph is an undirected graph with 12 nodes and 24 edges [1]_.
    It has 370 distinct (directed) Hamiltonian cycles, giving a unique generalized
    LCF notation of order 4, two of order 6 , and 43 of order 1 [2]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        The Chvátal graph with 12 nodes and 24 edges

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chv%C3%A1tal_graph
    .. [2] https://mathworld.wolfram.com/ChvatalGraph.html
    """
    ...
@_dispatchable
def cubical_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the 3-regular Platonic Cubical Graph

    The skeleton of the cube (the nodes and edges) form a graph, with 8
    nodes, and 12 edges. It is a special case of the hypercube graph.
    It is one of 5 Platonic graphs, each a skeleton of its
    Platonic solid [1]_.
    Such graphs arise in parallel processing in computers.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        A cubical graph with 8 nodes and 12 edges

    See Also
    --------
    tetrahedral_graph, octahedral_graph, dodecahedral_graph, icosahedral_graph

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Cube#Cubical_graph
    """
    ...
@_dispatchable
def desargues_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Desargues Graph

    The Desargues Graph is a non-planar, distance-transitive cubic graph
    with 20 nodes and 30 edges [1]_. It is isomorphic to the Generalized
    Petersen Graph GP(10, 3). It is a symmetric graph. It can be represented
    in LCF notation as [5,-5,9,-9]^5 [2]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Desargues Graph with 20 nodes and 30 edges

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Desargues_graph
    .. [2] https://mathworld.wolfram.com/DesarguesGraph.html
    """
    ...
@_dispatchable
def diamond_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Diamond graph

    The Diamond Graph is  planar undirected graph with 4 nodes and 5 edges.
    It is also sometimes known as the double triangle graph or kite graph [1]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Diamond Graph with 4 nodes and 5 edges

    References
    ----------
    .. [1] https://mathworld.wolfram.com/DiamondGraph.html
    """
    ...
@_dispatchable
def dodecahedral_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Platonic Dodecahedral graph.

    The dodecahedral graph has 20 nodes and 30 edges. The skeleton of the
    dodecahedron forms a graph. It is one of 5 Platonic graphs [1]_.
    It can be described in LCF notation as:
    ``[10, 7, 4, -4, -7, 10, -4, 7, -7, 4]^2`` [2]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Dodecahedral Graph with 20 nodes and 30 edges

    See Also
    --------
    tetrahedral_graph, cubical_graph, octahedral_graph, icosahedral_graph

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Regular_dodecahedron#Dodecahedral_graph
    .. [2] https://mathworld.wolfram.com/DodecahedralGraph.html
    """
    ...
@_dispatchable
def frucht_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Frucht Graph.

    The Frucht Graph is the smallest cubical graph whose
    automorphism group consists only of the identity element [1]_.
    It has 12 nodes and 18 edges and no nontrivial symmetries.
    It is planar and Hamiltonian [2]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Frucht Graph with 12 nodes and 18 edges

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Frucht_graph
    .. [2] https://mathworld.wolfram.com/FruchtGraph.html
    """
    ...
@_dispatchable
def heawood_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Heawood Graph, a (3,6) cage.

    The Heawood Graph is an undirected graph with 14 nodes and 21 edges,
    named after Percy John Heawood [1]_.
    It is cubic symmetric, nonplanar, Hamiltonian, and can be represented
    in LCF notation as ``[5,-5]^7`` [2]_.
    It is the unique (3,6)-cage: the regular cubic graph of girth 6 with
    minimal number of vertices [3]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Heawood Graph with 14 nodes and 21 edges

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Heawood_graph
    .. [2] https://mathworld.wolfram.com/HeawoodGraph.html
    .. [3] https://www.win.tue.nl/~aeb/graphs/Heawood.html
    """
    ...
@_dispatchable
def hoffman_singleton_graph() -> Graph[Incomplete]:
    """
    Returns the Hoffman-Singleton Graph.

    The Hoffman–Singleton graph is a symmetrical undirected graph
    with 50 nodes and 175 edges.
    All indices lie in ``Z % 5``: that is, the integers mod 5 [1]_.
    It is the only regular graph of vertex degree 7, diameter 2, and girth 5.
    It is the unique (7,5)-cage graph and Moore graph, and contains many
    copies of the Petersen Graph [2]_.

    Returns
    -------
    G : networkx Graph
        Hoffman–Singleton Graph with 50 nodes and 175 edges

    Notes
    -----
    Constructed from pentagon and pentagram as follows: Take five pentagons $P_h$
    and five pentagrams $Q_i$ . Join vertex $j$ of $P_h$ to vertex $h·i+j$ of $Q_i$ [3]_.

    References
    ----------
    .. [1] https://blogs.ams.org/visualinsight/2016/02/01/hoffman-singleton-graph/
    .. [2] https://mathworld.wolfram.com/Hoffman-SingletonGraph.html
    .. [3] https://en.wikipedia.org/wiki/Hoffman%E2%80%93Singleton_graph
    """
    ...
@_dispatchable
def house_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the House graph (square with triangle on top)

    The house graph is a simple undirected graph with
    5 nodes and 6 edges [1]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        House graph in the form of a square with a triangle on top

    References
    ----------
    .. [1] https://mathworld.wolfram.com/HouseGraph.html
    """
    ...
@_dispatchable
def house_x_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the House graph with a cross inside the house square.

    The House X-graph is the House graph plus the two edges connecting diagonally
    opposite vertices of the square base. It is also one of the two graphs
    obtained by removing two edges from the pentatope graph [1]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        House graph with diagonal vertices connected

    References
    ----------
    .. [1] https://mathworld.wolfram.com/HouseGraph.html
    """
    ...
@_dispatchable
def icosahedral_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Platonic Icosahedral graph.

    The icosahedral graph has 12 nodes and 30 edges. It is a Platonic graph
    whose nodes have the connectivity of the icosahedron. It is undirected,
    regular and Hamiltonian [1]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Icosahedral graph with 12 nodes and 30 edges.

    See Also
    --------
    tetrahedral_graph, cubical_graph, octahedral_graph, dodecahedral_graph

    References
    ----------
    .. [1] https://mathworld.wolfram.com/IcosahedralGraph.html
    """
    ...
@_dispatchable
def krackhardt_kite_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Krackhardt Kite Social Network.

    A 10 actor social network introduced by David Krackhardt
    to illustrate different centrality measures [1]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Krackhardt Kite graph with 10 nodes and 18 edges

    Notes
    -----
    The traditional labeling is:
    Andre=1, Beverley=2, Carol=3, Diane=4,
    Ed=5, Fernando=6, Garth=7, Heather=8, Ike=9, Jane=10.

    References
    ----------
    .. [1] Krackhardt, David. "Assessing the Political Landscape: Structure,
       Cognition, and Power in Organizations". Administrative Science Quarterly.
       35 (2): 342–369. doi:10.2307/2393394. JSTOR 2393394. June 1990.
    """
    ...
@_dispatchable
def moebius_kantor_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Moebius-Kantor graph.

    The Möbius-Kantor graph is the cubic symmetric graph on 16 nodes.
    Its LCF notation is [5,-5]^8, and it is isomorphic to the generalized
    Petersen Graph GP(8, 3) [1]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Moebius-Kantor graph

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/M%C3%B6bius%E2%80%93Kantor_graph
    """
    ...
@_dispatchable
def octahedral_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Platonic Octahedral graph.

    The octahedral graph is the 6-node 12-edge Platonic graph having the
    connectivity of the octahedron [1]_. If 6 couples go to a party,
    and each person shakes hands with every person except his or her partner,
    then this graph describes the set of handshakes that take place;
    for this reason it is also called the cocktail party graph [2]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Octahedral graph

    See Also
    --------
    tetrahedral_graph, cubical_graph, dodecahedral_graph, icosahedral_graph

    References
    ----------
    .. [1] https://mathworld.wolfram.com/OctahedralGraph.html
    .. [2] https://en.wikipedia.org/wiki/Tur%C3%A1n_graph#Special_cases
    """
    ...
@_dispatchable
def pappus_graph() -> Graph[Incomplete]:
    """
    Returns the Pappus graph.

    The Pappus graph is a cubic symmetric distance-regular graph with 18 nodes
    and 27 edges. It is Hamiltonian and can be represented in LCF notation as
    [5,7,-7,7,-7,-5]^3 [1]_.

    Returns
    -------
    G : networkx Graph
        Pappus graph

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Pappus_graph
    """
    ...
@_dispatchable
def petersen_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Petersen Graph.

    The Peterson Graph is a cubic, undirected graph with 10 nodes and 15 edges [1]_.
    Julius Petersen constructed the graph as the smallest counterexample
    against the claim that a connected bridgeless cubic graph
    has an edge colouring with three colours [2]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Petersen Graph

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Petersen_graph
    .. [2] https://www.win.tue.nl/~aeb/drg/graphs/Petersen.html
    """
    ...
@_dispatchable
def generalized_petersen_graph(n: int, k: int, *, create_using=None) -> Graph[Incomplete]:
    """
    Returns the Generalized Petersen Graph GP(n,k).

    The Generalized Peterson Graph consists of an outer cycle of n nodes
    connected to an inner circulant graph of n nodes, where nodes in the
    inner circulant are connected to their kth nearest neighbor [1]_ [2]_.
    A Generalized Petersen Graph is cubic with 2n nodes and 3n edges.

    Some well known graphs are examples of Generalized Petersen Graphs such
    as the Petersen Graph GP(5, 2), the Desargues graph GP(10, 3), the
    Moebius-Kantor graph GP(8, 3), and the dodecahedron graph GP(10, 2).

    Parameters
    ----------
    n : int
       Number of nodes in the outer cycle and inner circulant. ``n >= 3`` is required.

    k : int
       Neighbor to connect in the inner circulant. ``1 <= k <= n/2``.
       Note that some people require ``k < n/2`` but we and others allow equality.
       Also, ``k < n/2`` is equivalent to ``k <= floor((n-1)/2)``

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Generalized Petersen Graph n k

    References
    ----------
    .. [1] https://mathworld.wolfram.com/GeneralizedPetersenGraph.html
    .. [2] https://en.wikipedia.org/wiki/Generalized_Petersen_graph
    """
    ...
@_dispatchable
def sedgewick_maze_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Return a small maze with a cycle.

    This is the maze used in Sedgewick, 3rd Edition, Part 5, Graph
    Algorithms, Chapter 18, e.g. Figure 18.2 and following [1]_.
    Nodes are numbered 0,..,7

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Small maze with a cycle

    References
    ----------
    .. [1] Figure 18.2, Chapter 18, Graph Algorithms (3rd Ed), Sedgewick
    """
    ...
@_dispatchable
def tetrahedral_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the 3-regular Platonic Tetrahedral graph.

    Tetrahedral graph has 4 nodes and 6 edges. It is a
    special case of the complete graph, K4, and wheel graph, W4.
    It is one of the 5 platonic graphs [1]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Tetrahedral Graph

    See Also
    --------
    cubical_graph, octahedral_graph, dodecahedral_graph, icosahedral_graph

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Tetrahedron#Tetrahedral_graph
    """
    ...
@_dispatchable
def truncated_cube_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the skeleton of the truncated cube.

    The truncated cube is an Archimedean solid with 14 regular
    faces (6 octagonal and 8 triangular), 36 edges and 24 nodes [1]_.
    The truncated cube is created by truncating (cutting off) the tips
    of the cube one third of the way into each edge [2]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Skeleton of the truncated cube

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Truncated_cube
    .. [2] https://www.coolmath.com/reference/polyhedra-truncated-cube
    """
    ...
@_dispatchable
def truncated_tetrahedron_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the skeleton of the truncated Platonic tetrahedron.

    The truncated tetrahedron is an Archimedean solid with 4 regular hexagonal faces,
    4 equilateral triangle faces, 12 nodes and 18 edges. It can be constructed by truncating
    all 4 vertices of a regular tetrahedron at one third of the original edge length [1]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Skeleton of the truncated tetrahedron

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Truncated_tetrahedron
    """
    ...
@_dispatchable
def tutte_graph(create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]:
    """
    Returns the Tutte graph.

    The Tutte graph is a cubic polyhedral, non-Hamiltonian graph. It has
    46 nodes and 69 edges.
    It is a counterexample to Tait's conjecture that every 3-regular polyhedron
    has a Hamiltonian cycle.
    It can be realized geometrically from a tetrahedron by multiply truncating
    three of its vertices [1]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Tutte graph

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Tutte_graph
    """
    ...
