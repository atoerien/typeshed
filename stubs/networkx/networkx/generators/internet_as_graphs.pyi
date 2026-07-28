"""Generates graphs resembling the Internet Autonomous System network"""

from _typeshed import Incomplete
from collections.abc import Mapping

from networkx.classes.graph import Graph
from networkx.utils.backends import _dispatchable

__all__ = ["random_internet_as_graph"]

def uniform_int_from_avg(a, m, seed):
    """
    Pick a random integer with uniform probability.

    Returns a random integer uniformly taken from a distribution with
    minimum value 'a' and average value 'm', X~U(a,b), E[X]=m, X in N where
    b = 2*m - a.

    Notes
    -----
    p = (b-floor(b))/2
    X = X1 + X2; X1~U(a,floor(b)), X2~B(p)
    E[X] = E[X1] + E[X2] = (floor(b)+a)/2 + (b-floor(b))/2 = (b+a)/2 = m
    """
    ...
def choose_pref_attach(degs: Mapping[Incomplete, Incomplete], seed):
    """
    Pick a random value, with a probability given by its weight.

    Returns a random choice among degs keys, each of which has a
    probability proportional to the corresponding dictionary value.

    Parameters
    ----------
    degs: dictionary
        It contains the possible values (keys) and the corresponding
        probabilities (values)
    seed: random state

    Returns
    -------
    v: object
        A key of degs or None if degs is empty
    """
    ...

class AS_graph_generator:
    """Generates random internet AS graphs."""
    seed: Incomplete
    n_t: Incomplete
    n_m: Incomplete
    n_cp: Incomplete
    n_c: Incomplete
    d_m: Incomplete
    d_cp: Incomplete
    d_c: Incomplete
    p_m_m: Incomplete
    p_cp_m: Incomplete
    p_cp_cp: Incomplete
    t_m: float
    t_cp: float
    t_c: float
    def __init__(self, n, seed) -> None:
        """
        Initializes variables. Immediate numbers are taken from [1].

        Parameters
        ----------
        n: integer
            Number of graph nodes
        seed: random state
            Indicator of random number generation state.
            See :ref:`Randomness<randomness>`.

        Returns
        -------
        GG: AS_graph_generator object

        References
        ----------
        [1] A. Elmokashfi, A. Kvalbein and C. Dovrolis, "On the Scalability of
        BGP: The Role of Topology Growth," in IEEE Journal on Selected Areas
        in Communications, vol. 28, no. 8, pp. 1250-1261, October 2010.
        """
        ...
    G: Incomplete
    def t_graph(self) -> Graph[Incomplete]: ...
    def add_edge(self, i, j, kind) -> None: ...
    def choose_peer_pref_attach(self, node_list): ...
    def choose_node_pref_attach(self, node_list): ...
    def add_customer(self, i, j) -> None: ...
    def add_node(self, i, kind: str, reg2prob: float, avg_deg: float, t_edge_prob: float): ...
    def add_m_peering_link(self, m, to_kind: str) -> bool: ...
    def add_cp_peering_link(self, cp, to_kind: str) -> bool: ...
    regions: Incomplete
    def graph_regions(self, rn: int) -> None: ...
    def add_peering_links(self, from_kind, to_kind) -> None: ...
    customers: Incomplete
    providers: Incomplete
    nodes: Incomplete
    def generate(self) -> Graph[Incomplete]: ...

@_dispatchable
def random_internet_as_graph(n: int, seed=None) -> Graph[Incomplete]: ...
