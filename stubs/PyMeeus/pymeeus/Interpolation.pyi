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

    def __len__(self) -> int:
        """
        This method returns the number of interpolation points (x, y, pairs)
        stored in this :class:`Interpolation` object.

        :returns: Number of interpolation points internally stored
        :rtype: int

        >>> i = Interpolation([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> len(i)
        6
        """
        ...
    def get_tolerance(self) -> float:
        """
        Gets the internal tolerance value used for comparisons.

        .. note:: The default tolerance value is TOL.

        :returns: Internal tolerance.
        :rtype: float
        """
        ...
    def set_tolerance(self, tol: float) -> None:
        """
        Changes the internal tolerance value used for comparisons.

        :param tol: New tolerance value.
        :type tol: int, float

        :returns: None
        :rtype: None
        """
        ...
    def __call__(self, x: float | Angle) -> float | Angle:
        """
        Method to interpolate the function at a given 'x'.

        :param x: Point where the interpolation will be carried out.
        :type x: int, float, :py:class:`Angle`

        :returns: Resulting value of the interpolation.
        :rtype: float
        :raises: ValueError if input value is outside of interpolation range.
        :raises: TypeError if input value is of wrong type.

        >>> i = Interpolation([7, 8, 9], [0.884226, 0.877366, 0.870531])
        >>> y = round(i(8.18125), 6)
        >>> print(y)
        0.876125
        """
        ...
    def derivative(self, x: float | Angle) -> float:
        """
        Method to compute the derivative from interpolation polynomial.

        :param x: Point where the interpolation derivative will be carried out.
        :type x: int, float, :py:class:`Angle`

        :returns: Resulting value of the interpolation derivative.
        :rtype: float
        :raises: ValueError if input value is outside of interpolation range.
        :raises: TypeError if input value is of wrong type.

        >>> m = Interpolation([-1.0, 0.0, 1.0], [-2.0, 3.0, 2.0])
        >>> m.derivative(-1.0)
        8.0
        >>> m.derivative(0.5)
        -1.0
        """
        ...
    def root(self, xl: float | Angle = 0, xh: float | Angle = 0, max_iter: int = 1000) -> float | Angle:
        """
        Method to find the root inside the [xl, xh] range.

        This method applies, in principle, the Newton method to find the root;
        however, if conditions are such that Newton method may not bei properly
        behaving or converging, then it switches to the linear Interpolation
        method.

        If values xl, xh are not given, the limits of the interpolation table
        values will be used.

        .. note:: This method returns a ValueError exception if the
           corresponding yl = f(xl) and yh = f(xh) values have the same sign.
           In that case, the method assumes there is no root in the [xl, xh]
           interval.

        .. note:: If any of the xl, xh values is beyond the limits given by the
           interpolation values, its value will be set to the corresponding
           limit.

        .. note:: If xl == xh (and not zero), a ValueError exception is raised.

        .. note:: If the method doesn't converge within max_iter ierations,
           then a ValueError exception is raised.

        :param xl: Lower limit of interval where the root will be looked for.
        :type xl: int, float, :py:class:`Angle`
        :param xh: Higher limit of interval where the root will be looked for.
        :type xh: int, float, :py:class:`Angle`
        :param max_iter: Maximum number of iterations allowed.
        :type max_iter: int

        :returns: Root of the interpolated function within [xl, xh] interval.
        :rtype: int, float, :py:class:`Angle`
        :raises: ValueError if yl = f(xl), yh = f(xh) have same sign.
        :raises: ValueError if xl == xh.
        :raises: ValueError if maximum number of iterations is exceeded.
        :raises: TypeError if input value is of wrong type.

        >>> m = Interpolation([-1.0, 0.0, 1.0], [-2.0, 3.0, 2.0])
        >>> round(m.root(), 8)
        -0.72075922
        """
        ...
    def minmax(self, xl: float | Angle = 0, xh: float | Angle = 0, max_iter: int = 1000) -> float | Angle:
        """
        Method to find the minimum or maximum inside the [xl, xh] range.

        Finding the minimum or maximum (extremum) of a function within a given
        interval is akin to find the root of its derivative. Therefore, this
        method creates an interpolation object for the derivative function, and
        calls the root method of that object. See :meth:`root` method for more
        details.

        If values xl, xh are not given, the limits of the interpolation table
        values will be used.

        .. note::

           This method returns a ValueError exception if the corresponding
           derivatives yl' = f'(xl) and yh' = f'(xh) values have the same sign.
           In that case, the method assumes there is no extremum in the
           [xl, xh] interval.

        .. note::

           If any of the xl, xh values is beyond the limits given by the
           interpolation values, its value will be set to the corresponding
           limit.

        .. note:: If xl == xh (and not zero), a ValueError exception is raised.

        .. note:: If the method doesn't converge within max_iter ierations,
           then a ValueError exception is raised.

        :param xl: Lower limit of interval where a extremum will be looked for.
        :type xl: int, float, :py:class:`Angle`
        :param xh: Higher limit of interval where extremum will be looked for.
        :type xh: int, float, :py:class:`Angle`
        :param max_iter: Maximum number of iterations allowed.
        :type max_iter: int

        :returns: Extremum of interpolated function within [xl, xh] interval.
        :rtype: int, float, :py:class:`Angle`
        :raises: ValueError if yl = f(xl), yh = f(xh) have same sign.
        :raises: ValueError if xl == xh.
        :raises: ValueError if maximum number of iterations is exceeded.
        :raises: TypeError if input value is of wrong type.

        >>> m = Interpolation([-1.0, 0.0, 1.0], [-2.0, 3.0, 2.0])
        >>> round(m.minmax(), 8)
        0.33333333
        """
        ...

def main() -> None: ...
