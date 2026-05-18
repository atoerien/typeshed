from typing import overload

from pymeeus.Angle import Angle

class Interpolation:
    """
    Class Interpolation deals with finding intermediate values to those given
    in a table.

    Besides the basic interpolation, this class also provides methods to find
    the extrema (maximum or minimum value) in a given interval (if present),
    and it also has methods to find roots (the values of the argument 'x' for
    which the function 'y' becomes zero).

    Please note that it seems that Meeus uses the Bessel interpolation method
    (Chapter 3). However, this class uses the Newton interpolation method
    because it is (arguably) more flexible regarding the number of entries
    provided in the interpolation table.

    The constructor takes pairs of (x, y) values from the table of interest.
    These pairs of values can be given as a sequence of int/floats, tuples,
    lists or Angles. It is also possible to provide an Interpolation object to
    the constructor in order to get a copy.

    .. note:: When using Angles, be careful with the 360-to-0 discontinuity.

    If a sequence of int, floats or Angles is given, the values in the odd
    positions are considered to belong to the 'x' set, while the values in the
    even positions belong to the 'y' set. If only one tuple or list is
    provided, it is assumed that it is the 'y' set, and the 'x' set is build
    from 0 onwards with steps of length 1.

    Please keep in mind that a minimum of two data pairs are needed in order to
    carry out any interpolation. If only one value pair is provided, a
    ValueError exception will be raised.
    """
    @overload
    def __init__(self) -> None:
        """
        Interpolation constructor.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples, lists
        or Angles. It is also possible to provide an Interpolation object to
        the constructor in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another Interpolation object.
        :type args: int, float, list, tuple, :py:class:`Angle`,
           :py:class:`Interpolation`

        :returns: Interpolation object.
        :rtype: :py:class:`Interpolation`
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = Interpolation([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [1, 2, 3, 4, 5, 6]
        >>> print(i._y)
        [2, 4, 6, 8, 10, 12]
        >>> j = Interpolation([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = Interpolation(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [1, 2, 3]
        >>> print(k._y)
        [12, 5, -8]
        """
        ...
    @overload
    def __init__(self, a: Interpolation, /) -> None:
        """
        Interpolation constructor.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples, lists
        or Angles. It is also possible to provide an Interpolation object to
        the constructor in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another Interpolation object.
        :type args: int, float, list, tuple, :py:class:`Angle`,
           :py:class:`Interpolation`

        :returns: Interpolation object.
        :rtype: :py:class:`Interpolation`
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = Interpolation([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [1, 2, 3, 4, 5, 6]
        >>> print(i._y)
        [2, 4, 6, 8, 10, 12]
        >>> j = Interpolation([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = Interpolation(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [1, 2, 3]
        >>> print(k._y)
        [12, 5, -8]
        """
        ...
    @overload
    def __init__(self, a: list[float | Angle] | tuple[float | Angle, ...], /) -> None:
        """
        Interpolation constructor.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples, lists
        or Angles. It is also possible to provide an Interpolation object to
        the constructor in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another Interpolation object.
        :type args: int, float, list, tuple, :py:class:`Angle`,
           :py:class:`Interpolation`

        :returns: Interpolation object.
        :rtype: :py:class:`Interpolation`
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = Interpolation([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [1, 2, 3, 4, 5, 6]
        >>> print(i._y)
        [2, 4, 6, 8, 10, 12]
        >>> j = Interpolation([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = Interpolation(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [1, 2, 3]
        >>> print(k._y)
        [12, 5, -8]
        """
        ...
    @overload
    def __init__(
        self, a1: list[float | Angle] | tuple[float | Angle, ...], a2: list[float | Angle] | tuple[float | Angle, ...], /
    ) -> None:
        """
        Interpolation constructor.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples, lists
        or Angles. It is also possible to provide an Interpolation object to
        the constructor in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another Interpolation object.
        :type args: int, float, list, tuple, :py:class:`Angle`,
           :py:class:`Interpolation`

        :returns: Interpolation object.
        :rtype: :py:class:`Interpolation`
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = Interpolation([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [1, 2, 3, 4, 5, 6]
        >>> print(i._y)
        [2, 4, 6, 8, 10, 12]
        >>> j = Interpolation([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = Interpolation(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [1, 2, 3]
        >>> print(k._y)
        [12, 5, -8]
        """
        ...
    @overload
    def __init__(
        self, a1: float | Angle, a2: float | Angle, a3: float | Angle, a4: float | Angle, /, *rest: float | Angle
    ) -> None: ...

    @overload
    def set(self) -> None:
        """
        Method used to define the value pairs of Interpolation object.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples,
        lists, or Angles. It is also possible to provide an Interpolation
        object to this method in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another Interpolation object.
        :type args: int, float, list, tuple, :py:class:`Angle`

        :returns: None.
        :rtype: None
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = Interpolation()
        >>> i.set([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [1, 2, 3, 4, 5, 6]
        >>> print(i._y)
        [2, 4, 6, 8, 10, 12]
        >>> j = Interpolation()
        >>> j.set([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = Interpolation(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [1, 2, 3]
        >>> print(k._y)
        [12, 5, -8]
        >>> m = Interpolation(k)
        >>> print(m._x)
        [1, 2, 3]
        >>> print(m._y)
        [12, 5, -8]
        """
        ...
    @overload
    def set(self, a: Interpolation, /) -> None:
        """
        Method used to define the value pairs of Interpolation object.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples,
        lists, or Angles. It is also possible to provide an Interpolation
        object to this method in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another Interpolation object.
        :type args: int, float, list, tuple, :py:class:`Angle`

        :returns: None.
        :rtype: None
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = Interpolation()
        >>> i.set([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [1, 2, 3, 4, 5, 6]
        >>> print(i._y)
        [2, 4, 6, 8, 10, 12]
        >>> j = Interpolation()
        >>> j.set([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = Interpolation(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [1, 2, 3]
        >>> print(k._y)
        [12, 5, -8]
        >>> m = Interpolation(k)
        >>> print(m._x)
        [1, 2, 3]
        >>> print(m._y)
        [12, 5, -8]
        """
        ...
    @overload
    def set(self, a: list[float | Angle] | tuple[float | Angle, ...], /) -> None:
        """
        Method used to define the value pairs of Interpolation object.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples,
        lists, or Angles. It is also possible to provide an Interpolation
        object to this method in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another Interpolation object.
        :type args: int, float, list, tuple, :py:class:`Angle`

        :returns: None.
        :rtype: None
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = Interpolation()
        >>> i.set([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [1, 2, 3, 4, 5, 6]
        >>> print(i._y)
        [2, 4, 6, 8, 10, 12]
        >>> j = Interpolation()
        >>> j.set([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = Interpolation(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [1, 2, 3]
        >>> print(k._y)
        [12, 5, -8]
        >>> m = Interpolation(k)
        >>> print(m._x)
        [1, 2, 3]
        >>> print(m._y)
        [12, 5, -8]
        """
        ...
    @overload
    def set(
        self, a1: list[float | Angle] | tuple[float | Angle, ...], a2: list[float | Angle] | tuple[float | Angle, ...], /
    ) -> None:
        """
        Method used to define the value pairs of Interpolation object.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples,
        lists, or Angles. It is also possible to provide an Interpolation
        object to this method in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another Interpolation object.
        :type args: int, float, list, tuple, :py:class:`Angle`

        :returns: None.
        :rtype: None
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = Interpolation()
        >>> i.set([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [1, 2, 3, 4, 5, 6]
        >>> print(i._y)
        [2, 4, 6, 8, 10, 12]
        >>> j = Interpolation()
        >>> j.set([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = Interpolation(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [1, 2, 3]
        >>> print(k._y)
        [12, 5, -8]
        >>> m = Interpolation(k)
        >>> print(m._x)
        [1, 2, 3]
        >>> print(m._y)
        [12, 5, -8]
        """
        ...
    @overload
    def set(
        self, a1: float | Angle, a2: float | Angle, a3: float | Angle, a4: float | Angle, /, *rest: float | Angle
    ) -> None: ...

    def __len__(self) -> int: ...
    def get_tolerance(self) -> float: ...
    def set_tolerance(self, tol: float) -> None: ...
    def __call__(self, x: float | Angle) -> float | Angle: ...
    def derivative(self, x: float | Angle) -> float: ...
    def root(self, xl: float | Angle = 0, xh: float | Angle = 0, max_iter: int = 1000) -> float | Angle: ...
    def minmax(self, xl: float | Angle = 0, xh: float | Angle = 0, max_iter: int = 1000) -> float | Angle: ...

def main() -> None: ...
