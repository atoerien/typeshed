"""functions for 2D affine transformations"""

def nullTransform(): ...
def translate(dx: float, dy: float = 0): ...
def scale(sx: float, sy: float = 1): ...
def rotate(angle: float, cx: float = 0, cy: float = 0): ...
def skewX(angle: float): ...
def skewY(angle: float): ...
def mmult(A, B):
    """A postmultiplied by B"""
    ...
def combineTransforms(*T):
    """
    given transform matrices in the order they should be applied generate
    a combined transform.

    combineTransforms(T0,T1,T2) == mmult(T2,mmult(T1,T0))
                                == T2*T1*T0
    so that T0 is applied first, then T1 and finally T2.
    """
    ...
def inverse(A):
    """For A affine 2D represented as 6vec return 6vec version of A**(-1)"""
    ...
def zTransformPoint(A, v):
    """Apply the homogenous part of atransformation a to vector v --> A*v"""
    ...
def transformPoint(A, v):
    """Apply transformation a to vector v --> A*v"""
    ...
def transformPoints(matrix, V): ...
def zTransformPoints(matrix, V): ...

__all__ = (
    "nullTransform",
    "translate",
    "scale",
    "rotate",
    "skewX",
    "skewY",
    "mmult",
    "combineTransforms",
    "inverse",
    "zTransformPoint",
    "transformPoint",
    "transformPoints",
    "zTransformPoints",
)
