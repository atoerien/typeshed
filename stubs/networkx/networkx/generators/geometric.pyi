"""Generators for geometric graphs."""

from _typeshed import Incomplete
from collections.abc import Callable, Iterable

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = [
    "geometric_edges",
    "geographical_threshold_graph",
    "navigable_small_world_graph",
    "random_geometric_graph",
    "soft_random_geometric_graph",
    "thresholded_random_geometric_graph",
    "waxman_graph",
    "geometric_soft_configuration_graph",
]

@_dispatchable
def geometric_edges(G: Graph[_Node], radius: float, p: float = 2) -> list[Incomplete]: ...
@_dispatchable
def random_geometric_graph(
    n: int | Iterable[Incomplete],
    radius: float,
    dim: int = 2,
    pos: dict[Incomplete, Incomplete] | None = None,
    p: float = 2,
    seed=None,
) -> Graph[Incomplete]: ...
@_dispatchable
def soft_random_geometric_graph(
    n: int | Iterable[Incomplete],
    radius: float,
    dim: int = 2,
    pos: dict[Incomplete, Incomplete] | None = None,
    p: float = 2,
    p_dist: Callable[..., Incomplete] | None = None,
    seed=None,
) -> Graph[Incomplete]: ...
@_dispatchable
def geographical_threshold_graph(
    n: int | Iterable[Incomplete],
    theta: float,
    dim: int = 2,
    pos: dict[Incomplete, Incomplete] | None = None,
    weight: dict[Incomplete, Incomplete] | None = None,
    metric: Callable[..., Incomplete] | None = None,
    p_dist: Callable[..., Incomplete] | None = None,
    seed=None,
) -> Graph[Incomplete]: ...
@_dispatchable
def waxman_graph(
    n: int | Iterable[Incomplete],
    beta: float = 0.4,
    alpha: float = 0.1,
    L: float | None = None,
    domain: tuple[float, float, float, float] = (0, 0, 1, 1),
    metric: Callable[..., Incomplete] | None = None,
    seed=None,
) -> Graph[Incomplete]: ...

# docstring marks p as int, but it still works with floats. So I think it's better for consistency
@_dispatchable
def navigable_small_world_graph(n: int, p: float = 1, q: int = 1, r: float = 2, dim: int = 2, seed=None): ...
@_dispatchable
def thresholded_random_geometric_graph(
    n: int | Iterable[Incomplete],
    radius: float,
    theta: float,
    dim: int = 2,
    pos: dict[Incomplete, Incomplete] | None = None,
    weight: dict[Incomplete, Incomplete] | None = None,
    p: float = 2,
    seed=None,
) -> Graph[Incomplete]: ...
@_dispatchable
def geometric_soft_configuration_graph(
    *, beta, n=None, gamma=None, mean_degree=None, kappas=None, seed=None
) -> Graph[Incomplete]:
    r"""
    Returns a random graph from the geometric soft configuration model.

    The $\mathbb{S}^1$ model [1]_ is the geometric soft configuration model
    which is able to explain many fundamental features of real networks such as
    small-world property, heteregenous degree distributions, high level of
    clustering, and self-similarity.

    In the geometric soft configuration model, a node $i$ is assigned two hidden
    variables: a hidden degree $\kappa_i$, quantifying its popularity, influence,
    or importance, and an angular position $\theta_i$ in a circle abstracting the
    similarity space, where angular distances between nodes are a proxy for their
    similarity. Focusing on the angular position, this model is often called
    the $\mathbb{S}^1$ model (a one-dimensional sphere). The circle's radius is
    adjusted to $R = N/2\pi$, where $N$ is the number of nodes, so that the density
    is set to 1 without loss of generality.

    The connection probability between any pair of nodes increases with
    the product of their hidden degrees (i.e., their combined popularities),
    and decreases with the angular distance between the two nodes.
    Specifically, nodes $i$ and $j$ are connected with the probability

    $p_{ij} = \frac{1}{1 + \frac{d_{ij}^\beta}{\left(\mu \kappa_i \kappa_j\right)^{\max(1, \beta)}}}$

    where $d_{ij} = R\Delta\theta_{ij}$ is the arc length of the circle between
    nodes $i$ and $j$ separated by an angular distance $\Delta\theta_{ij}$.
    Parameters $\mu$ and $\beta$ (also called inverse temperature) control the
    average degree and the clustering coefficient, respectively.

    It can be shown [2]_ that the model undergoes a structural phase transition
    at $\beta=1$ so that for $\beta<1$ networks are unclustered in the thermodynamic
    limit (when $N\to \infty$) whereas for $\beta>1$ the ensemble generates
    networks with finite clustering coefficient.

    The $\mathbb{S}^1$ model can be expressed as a purely geometric model
    $\mathbb{H}^2$ in the hyperbolic plane [3]_ by mapping the hidden degree of
    each node into a radial coordinate as

    $r_i = \hat{R} - \frac{2 \max(1, \beta)}{\beta \zeta} \ln \left(\frac{\kappa_i}{\kappa_0}\right)$

    where $\hat{R}$ is the radius of the hyperbolic disk and $\zeta$ is the curvature,

    $\hat{R} = \frac{2}{\zeta} \ln \left(\frac{N}{\pi}\right)
    - \frac{2\max(1, \beta)}{\beta \zeta} \ln (\mu \kappa_0^2)$

    The connection probability then reads

    $p_{ij} = \frac{1}{1 + \exp\left({\frac{\beta\zeta}{2} (x_{ij} - \hat{R})}\right)}$

    where

    $x_{ij} = r_i + r_j + \frac{2}{\zeta} \ln \frac{\Delta\theta_{ij}}{2}$

    is a good approximation of the hyperbolic distance between two nodes separated
    by an angular distance $\Delta\theta_{ij}$ with radial coordinates $r_i$ and $r_j$.
    For $\beta > 1$, the curvature $\zeta = 1$, for $\beta < 1$, $\zeta = \beta^{-1}$.


    Parameters
    ----------
    Either `n`, `gamma`, `mean_degree` are provided or `kappas`. The values of
    `n`, `gamma`, `mean_degree` (if provided) are used to construct a random
    kappa-dict keyed by node with values sampled from a power-law distribution.

    beta : positive number
        Inverse temperature, controlling the clustering coefficient.
    n : int (default: None)
        Size of the network (number of nodes).
        If not provided, `kappas` must be provided and holds the nodes.
    gamma : float (default: None)
        Exponent of the power-law distribution for hidden degrees `kappas`.
        If not provided, `kappas` must be provided directly.
    mean_degree : float (default: None)
        The mean degree in the network.
        If not provided, `kappas` must be provided directly.
    kappas : dict (default: None)
        A dict keyed by node to its hidden degree value.
        If not provided, random values are computed based on a power-law
        distribution using `n`, `gamma` and `mean_degree`.
    seed : int, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    Graph
        A random geometric soft configuration graph (undirected with no self-loops).
        Each node has three node-attributes:

        - ``kappa`` that represents the hidden degree.

        - ``theta`` the position in the similarity space ($\mathbb{S}^1$) which is
          also the angular position in the hyperbolic plane.

        - ``radius`` the radial position in the hyperbolic plane
          (based on the hidden degree).


    Examples
    --------
    Generate a network with specified parameters:

    >>> G = nx.geometric_soft_configuration_graph(
    ...     beta=1.5, n=100, gamma=2.7, mean_degree=5
    ... )

    Create a geometric soft configuration graph with 100 nodes. The $\beta$ parameter
    is set to 1.5 and the exponent of the powerlaw distribution of the hidden
    degrees is 2.7 with mean value of 5.

    Generate a network with predefined hidden degrees:

    >>> kappas = {i: 10 for i in range(100)}
    >>> G = nx.geometric_soft_configuration_graph(beta=2.5, kappas=kappas)

    Create a geometric soft configuration graph with 100 nodes. The $\beta$ parameter
    is set to 2.5 and all nodes with hidden degree $\kappa=10$.


    References
    ----------
    .. [1] Serrano, M. Á., Krioukov, D., & Boguñá, M. (2008). Self-similarity
       of complex networks and hidden metric spaces. Physical review letters, 100(7), 078701.

    .. [2] van der Kolk, J., Serrano, M. Á., & Boguñá, M. (2022). An anomalous
       topological phase transition in spatial random graphs. Communications Physics, 5(1), 245.

    .. [3] Krioukov, D., Papadopoulos, F., Kitsak, M., Vahdat, A., & Boguná, M. (2010).
       Hyperbolic geometry of complex networks. Physical Review E, 82(3), 036106.
    """
    ...
