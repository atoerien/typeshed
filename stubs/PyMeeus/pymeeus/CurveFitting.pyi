from collections.abc import Callable
from typing import overload

from pymeeus.Angle import Angle

class CurveFitting:
    """
    Class CurveFitting deals with finding the function (linear, cuadratic, etc)
    that best fit a given set of points.

    The constructor takes pairs of (x, y) values from the table of interest.
    These pairs of values can be given as a sequence of int/floats, tuples,
    lists or Angles. It is also possible to provide a CurveFitting object to
    the constructor in order to get a copy.

    .. note:: When using Angles, be careful with the 360-to-0 discontinuity.

    If a sequence of int, floats or Angles is given, the values in the odd
    positions are considered to belong to the 'x' set, while the values in the
    even positions belong to the 'y' set. If only one tuple or list is
    provided, it is assumed that it is the 'y' set, and the 'x' set is build
    from 0 onwards with steps of length 1.

    Please keep in mind that a minimum of two data pairs are needed in order to
    carry out any fitting. If only one value pair is provided, a ValueError
    exception will be raised.
    """
    @overload
    def __init__(self) -> None:
        """
        CurveFitting constructor.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples, lists
        or Angles. It is also possible to provide a CurveFitting object to the
        constructor in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another CurveFitting object.
        :type args: int, float, list, tuple, :py:class:`Angle`,
           :py:class:`CurveFitting`

        :returns: CurveFitting object.
        :rtype: :py:class:`CurveFitting`
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = CurveFitting([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [5, 3, 6, 1, 2, 4]
        >>> print(i._y)
        [10, 6, 12, 2, 4, 8]
        >>> j = CurveFitting([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = CurveFitting(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [3, 1, 2]
        >>> print(k._y)
        [-8, 12, 5]
        >>> m = CurveFitting(k)
        >>> print(m._x)
        [3, 1, 2]
        >>> print(m._y)
        [-8, 12, 5]
        """
        ...
    @overload
    def __init__(self, a: CurveFitting, /) -> None:
        """
        CurveFitting constructor.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples, lists
        or Angles. It is also possible to provide a CurveFitting object to the
        constructor in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another CurveFitting object.
        :type args: int, float, list, tuple, :py:class:`Angle`,
           :py:class:`CurveFitting`

        :returns: CurveFitting object.
        :rtype: :py:class:`CurveFitting`
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = CurveFitting([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [5, 3, 6, 1, 2, 4]
        >>> print(i._y)
        [10, 6, 12, 2, 4, 8]
        >>> j = CurveFitting([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = CurveFitting(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [3, 1, 2]
        >>> print(k._y)
        [-8, 12, 5]
        >>> m = CurveFitting(k)
        >>> print(m._x)
        [3, 1, 2]
        >>> print(m._y)
        [-8, 12, 5]
        """
        ...
    @overload
    def __init__(self, a: list[float | Angle] | tuple[float | Angle, ...], /) -> None:
        """
        CurveFitting constructor.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples, lists
        or Angles. It is also possible to provide a CurveFitting object to the
        constructor in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another CurveFitting object.
        :type args: int, float, list, tuple, :py:class:`Angle`,
           :py:class:`CurveFitting`

        :returns: CurveFitting object.
        :rtype: :py:class:`CurveFitting`
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = CurveFitting([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [5, 3, 6, 1, 2, 4]
        >>> print(i._y)
        [10, 6, 12, 2, 4, 8]
        >>> j = CurveFitting([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = CurveFitting(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [3, 1, 2]
        >>> print(k._y)
        [-8, 12, 5]
        >>> m = CurveFitting(k)
        >>> print(m._x)
        [3, 1, 2]
        >>> print(m._y)
        [-8, 12, 5]
        """
        ...
    @overload
    def __init__(
        self, a1: list[float | Angle] | tuple[float | Angle, ...], a2: list[float | Angle] | tuple[float | Angle, ...], /
    ) -> None:
        """
        CurveFitting constructor.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples, lists
        or Angles. It is also possible to provide a CurveFitting object to the
        constructor in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another CurveFitting object.
        :type args: int, float, list, tuple, :py:class:`Angle`,
           :py:class:`CurveFitting`

        :returns: CurveFitting object.
        :rtype: :py:class:`CurveFitting`
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = CurveFitting([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [5, 3, 6, 1, 2, 4]
        >>> print(i._y)
        [10, 6, 12, 2, 4, 8]
        >>> j = CurveFitting([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = CurveFitting(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [3, 1, 2]
        >>> print(k._y)
        [-8, 12, 5]
        >>> m = CurveFitting(k)
        >>> print(m._x)
        [3, 1, 2]
        >>> print(m._y)
        [-8, 12, 5]
        """
        ...
    @overload
    def __init__(
        self, a1: float | Angle, a2: float | Angle, a3: float | Angle, a4: float | Angle, /, *rest: float | Angle
    ) -> None:
        """
        CurveFitting constructor.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples, lists
        or Angles. It is also possible to provide a CurveFitting object to the
        constructor in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value pair is
        provided, a ValueError exception will be raised.

        :param args: Input tabular values, or another CurveFitting object.
        :type args: int, float, list, tuple, :py:class:`Angle`,
           :py:class:`CurveFitting`

        :returns: CurveFitting object.
        :rtype: :py:class:`CurveFitting`
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = CurveFitting([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [5, 3, 6, 1, 2, 4]
        >>> print(i._y)
        [10, 6, 12, 2, 4, 8]
        >>> j = CurveFitting([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = CurveFitting(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [3, 1, 2]
        >>> print(k._y)
        [-8, 12, 5]
        >>> m = CurveFitting(k)
        >>> print(m._x)
        [3, 1, 2]
        >>> print(m._y)
        [-8, 12, 5]
        """
        ...

    @overload
    def set(self) -> None:
        """
        Method used to define the value pairs of CurveFitting object.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples,
        lists, or Angles. It is also possible to provide a CurveFitting object
        to this method in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value is provided, a
        ValueError exception will be raised.

        :param args: Input tabular values, or another CurveFitting object.
        :type args: int, float, list, tuple, :py:class:`Angle`

        :returns: None.
        :rtype: None
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = CurveFitting()
        >>> i.set([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [5, 3, 6, 1, 2, 4]
        >>> print(i._y)
        [10, 6, 12, 2, 4, 8]
        >>> j = CurveFitting()
        >>> j.set([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = CurveFitting(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [3, 1, 2]
        >>> print(k._y)
        [-8, 12, 5]
        """
        ...
    @overload
    def set(self, a: CurveFitting, /) -> None:
        """
        Method used to define the value pairs of CurveFitting object.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples,
        lists, or Angles. It is also possible to provide a CurveFitting object
        to this method in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value is provided, a
        ValueError exception will be raised.

        :param args: Input tabular values, or another CurveFitting object.
        :type args: int, float, list, tuple, :py:class:`Angle`

        :returns: None.
        :rtype: None
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = CurveFitting()
        >>> i.set([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [5, 3, 6, 1, 2, 4]
        >>> print(i._y)
        [10, 6, 12, 2, 4, 8]
        >>> j = CurveFitting()
        >>> j.set([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = CurveFitting(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [3, 1, 2]
        >>> print(k._y)
        [-8, 12, 5]
        """
        ...
    @overload
    def set(self, a: list[float | Angle] | tuple[float | Angle, ...], /) -> None:
        """
        Method used to define the value pairs of CurveFitting object.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples,
        lists, or Angles. It is also possible to provide a CurveFitting object
        to this method in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value is provided, a
        ValueError exception will be raised.

        :param args: Input tabular values, or another CurveFitting object.
        :type args: int, float, list, tuple, :py:class:`Angle`

        :returns: None.
        :rtype: None
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = CurveFitting()
        >>> i.set([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [5, 3, 6, 1, 2, 4]
        >>> print(i._y)
        [10, 6, 12, 2, 4, 8]
        >>> j = CurveFitting()
        >>> j.set([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = CurveFitting(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [3, 1, 2]
        >>> print(k._y)
        [-8, 12, 5]
        """
        ...
    @overload
    def set(
        self, a1: list[float | Angle] | tuple[float | Angle, ...], a2: list[float | Angle] | tuple[float | Angle, ...], /
    ) -> None:
        """
        Method used to define the value pairs of CurveFitting object.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples,
        lists, or Angles. It is also possible to provide a CurveFitting object
        to this method in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value is provided, a
        ValueError exception will be raised.

        :param args: Input tabular values, or another CurveFitting object.
        :type args: int, float, list, tuple, :py:class:`Angle`

        :returns: None.
        :rtype: None
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = CurveFitting()
        >>> i.set([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [5, 3, 6, 1, 2, 4]
        >>> print(i._y)
        [10, 6, 12, 2, 4, 8]
        >>> j = CurveFitting()
        >>> j.set([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = CurveFitting(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [3, 1, 2]
        >>> print(k._y)
        [-8, 12, 5]
        """
        ...
    @overload
    def set(
        self, a1: float | Angle, a2: float | Angle, a3: float | Angle, a4: float | Angle, /, *rest: float | Angle
    ) -> None:
        """
        Method used to define the value pairs of CurveFitting object.

        This takes pairs of (x, y) values from the table of interest. These
        pairs of values can be given as a sequence of int/floats, tuples,
        lists, or Angles. It is also possible to provide a CurveFitting object
        to this method in order to get a copy.

        .. note:: When using Angles, be careful with the 360-to-0 discontinuity

        If a sequence of int, floats or Angles is given, the values in the odd
        positions are considered to belong to the 'x' set, while the values in
        the even positions belong to the 'y' set. If only one tuple or list is
        provided, it is assumed that it is the 'y' set, and the 'x' set is
        build from 0 onwards with steps of length 1.

        Please keep in mind that a minimum of two data pairs are needed in
        order to carry out any interpolation. If only one value is provided, a
        ValueError exception will be raised.

        :param args: Input tabular values, or another CurveFitting object.
        :type args: int, float, list, tuple, :py:class:`Angle`

        :returns: None.
        :rtype: None
        :raises: ValueError if not enough input data pairs are provided.
        :raises: TypeError if input values are of wrong type.

        >>> i = CurveFitting()
        >>> i.set([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> print(i._x)
        [5, 3, 6, 1, 2, 4]
        >>> print(i._y)
        [10, 6, 12, 2, 4, 8]
        >>> j = CurveFitting()
        >>> j.set([3, -8, 1, 12, 2, 5, 8])
        >>> print(j._x)
        [0, 1, 2, 3, 4, 5, 6]
        >>> print(j._y)
        [3, -8, 1, 12, 2, 5, 8]
        >>> k = CurveFitting(3, -8, 1, 12, 2, 5, 8)
        >>> print(k._x)
        [3, 1, 2]
        >>> print(k._y)
        [-8, 12, 5]
        """
        ...

    def __len__(self) -> int:
        """
        This method returns the number of value pairs internally stored in
        this object.

        :returns: Number of value pairs internally stored
        :rtype: int

        >>> i = CurveFitting([5, 3, 6, 1, 2, 4, 9], [10, 6, 12, 2, 4, 8])
        >>> len(i)
        6
        """
        ...
    def correlation_coeff(self) -> float:
        """
        This method returns the coefficient of correlation, as a float.

        :returns: Coefficient of correlation.
        :rtype: float

        >>> cf = CurveFitting([73.0, 38.0, 35.0, 42.0, 78.0, 68.0, 74.0, 42.0,
        ...                    52.0, 54.0, 39.0, 61.0, 42.0, 49.0, 50.0, 62.0,
        ...                    44.0, 39.0, 43.0, 54.0, 44.0, 37.0],
        ...                   [90.4, 125.3, 161.8, 143.4, 52.5, 50.8, 71.5,
        ...                    152.8, 131.3, 98.5, 144.8, 78.1, 89.5, 63.9,
        ...                    112.1, 82.0, 119.8, 161.2, 208.4, 111.6, 167.1,
        ...                    162.1])
        >>> r = cf.correlation_coeff()
        >>> print(round(r, 3))
        -0.767
        """
        ...
    def linear_fitting(self) -> tuple[float, float]:
        """
        This method returns a tuple with the 'a', 'b' coefficients of the
        linear equation *'y = a*x + b'* that best fits the table data, using
        the least squares approach.

        :returns: 'a', 'b' coefficients of best linear equation fit.
        :rtype: tuple
        :raises: ZeroDivisionError if input data leads to a division by zero

        >>> cf = CurveFitting([73.0, 38.0, 35.0, 42.0, 78.0, 68.0, 74.0, 42.0,
        ...                    52.0, 54.0, 39.0, 61.0, 42.0, 49.0, 50.0, 62.0,
        ...                    44.0, 39.0, 43.0, 54.0, 44.0, 37.0],
        ...                   [90.4, 125.3, 161.8, 143.4, 52.5, 50.8, 71.5,
        ...                    152.8, 131.3, 98.5, 144.8, 78.1, 89.5, 63.9,
        ...                    112.1, 82.0, 119.8, 161.2, 208.4, 111.6, 167.1,
        ...                    162.1])
        >>> a, b = cf.linear_fitting()
        >>> print("a = {}       b = {}".format(round(a, 2), round(b, 2)))
        a = -2.49       b = 244.18
        """
        ...
    def quadratic_fitting(self) -> tuple[float, float, float]:
        """
        This method returns a tuple with the 'a', 'b', 'c' coefficients of
        the quadratic equation *'y = a*x*x + b*x + c'* that best fits the table
        data, using the least squares approach.

        :returns: 'a', 'b', 'c' coefficients of best quadratic equation fit.
        :rtype: tuple
        :raises: ZeroDivisionError if input data leads to a division by zero

        >>> cf2 = CurveFitting([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5,
        ...                     2.0, 2.5,3.0],
        ...                    [-9.372, -3.821, 0.291, 3.730, 5.822, 8.324,
        ...                     9.083, 6.957, 7.006, 0.365, -1.722])
        >>> a, b, c = cf2.quadratic_fitting()
        >>> print("a = {}; b = {}; c = {}".format(round(a, 2), round(b, 2),
        ...                                       round(c, 2)))
        a = -2.22; b = 3.76; c = 6.64
        """
        ...
    def general_fitting(
        self, f0: Callable[..., float], f1: Callable[..., float] = ..., f2: Callable[..., float] = ...
    ) -> tuple[float, float, float]:
        """
        This method returns a tuple with the 'a', 'b', 'c' coefficients of
        the general equation *'y = a*f0(x) + b*f1(x) + c*f2(x)'* that best fits
        the table data, using the least squares approach.

        :param f0, f1, f2: Functions used to build the general equation.
        :type f0, f1, f2: function
        :returns: 'a', 'b', 'c' coefficients of best general equation fit.
        :rtype: tuple
        :raises: ZeroDivisionError if input functions are null or input data
           leads to a division by zero

        >>> cf4 = CurveFitting([3, 20, 34, 50, 75, 88, 111, 129, 143, 160, 183,
        ...                     200, 218, 230, 248, 269, 290, 303, 320, 344],
        ...                    [0.0433, 0.2532, 0.3386, 0.3560, 0.4983, 0.7577,
        ...                     1.4585, 1.8628, 1.8264, 1.2431, -0.2043,
        ...                     -1.2431, -1.8422, -1.8726, -1.4889, -0.8372,
        ...                     -0.4377, -0.3640, -0.3508, -0.2126])
        >>> def sin1(x): return sin(radians(x))
        >>> def sin2(x): return sin(radians(2.0*x))
        >>> def sin3(x): return sin(radians(3.0*x))
        >>> a, b, c = cf4.general_fitting(sin1, sin2, sin3)
        >>> print("a = {}; b = {}; c = {}".format(round(a, 2), round(b, 2),
        ...                                       round(c, 2)))
        a = 1.2; b = -0.77; c = 0.39

        >>> cf5 = CurveFitting([0, 1.2, 1.4, 1.7, 2.1, 2.2])
        >>> a, b, c = cf5.general_fitting(sqrt)
        >>> print("a = {}; b = {}; c = {}".format(round(a, 3), round(b, 3),
        ...                                       round(c, 3)))
        a = 1.016; b = 0.0; c = 0.0
        """
        ...

def main() -> None: ...
