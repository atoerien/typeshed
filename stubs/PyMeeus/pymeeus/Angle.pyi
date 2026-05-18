from typing import overload
from typing_extensions import Self

class Angle:
    """
    Class Angle deals with angles in either decimal format (d.dd) or in
    sexagesimal format (d m' s'').

    It provides methods to handle an Angle object like it were a simple float,
    but adding the functionality associated with an angle.

    The constructor takes decimals and sexagesimal input. The sexagesimal
    angles can be given as separate degree, minutes, seconds values, or as
    tuples or lists. It is also possible to provide another Angle object as
    input.

    Also, if **radians=True** is passed to the constructor, then the input
    value is considered as in radians, and converted to degrees.
    """
    @overload
    def __init__(self, *, ra: bool = False) -> None:
        """
        Angle constructor.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees.

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(-13, 30, 0.0)
        >>> print(a)
        -13.5
        >>> b = Angle(a)
        >>> print(b)
        -13.5
        """
        ...
    @overload
    def __init__(self, a: Angle, /, *, ra: bool = False) -> None:
        """
        Angle constructor.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees.

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(-13, 30, 0.0)
        >>> print(a)
        -13.5
        >>> b = Angle(a)
        >>> print(b)
        -13.5
        """
        ...
    @overload
    def __init__(self, a: float, /, *, ra: bool = False, radians: bool = False) -> None:
        """
        Angle constructor.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees.

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(-13, 30, 0.0)
        >>> print(a)
        -13.5
        >>> b = Angle(a)
        >>> print(b)
        -13.5
        """
        ...
    @overload
    def __init__(self, a: list[float] | tuple[float, ...], /, *, ra: bool = False, radians: bool = False) -> None:
        """
        Angle constructor.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees.

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(-13, 30, 0.0)
        >>> print(a)
        -13.5
        >>> b = Angle(a)
        >>> print(b)
        -13.5
        """
        ...
    @overload
    def __init__(self, a1: float, a2: float, /, *, ra: bool = False) -> None:
        """
        Angle constructor.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees.

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(-13, 30, 0.0)
        >>> print(a)
        -13.5
        >>> b = Angle(a)
        >>> print(b)
        -13.5
        """
        ...
    @overload
    def __init__(self, a1: float, a2: float, a3: float, /, *, ra: bool = False) -> None:
        """
        Angle constructor.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees.

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(-13, 30, 0.0)
        >>> print(a)
        -13.5
        >>> b = Angle(a)
        >>> print(b)
        -13.5
        """
        ...
    @overload
    def __init__(self, a1: float, a2: float, a3: float, a4: float, /, *, ra: bool = False) -> None: ...

    @staticmethod
    def reduce_deg(deg: float | Angle) -> float:
        """
        Takes a degree value in decimal format and converts it to a float
        value in the +/-[0:360) range.

        :param deg: Input degree angle in decimal format.
        :type deg: int, float, :py:class:`Angle`

        :returns: Float value of the angle in the +/-[0:360) range.
        :rtype: float

        >>> a = 386.3
        >>> b = Angle.reduce_deg(a)
        >>> print(round(b, 1))
        26.3
        """
        ...
    @staticmethod
    def reduce_dms(degrees: float, minutes: float, seconds: float = 0.0) -> tuple[int, int, float, float]:
        """
        Takes a degree value in sexagesimal format and converts it to a
        value in the +/-[0:360) range (degrees) and [0:60) range (minutes and
        seconds). It also takes care of fractional degrees and minutes.

        :param degrees: Degrees.
        :type degrees: int, float
        :param minutes: Minutes.
        :type minutes: int, float
        :param seconds: Seconds. 0.0 by default.
        :type seconds: int, float

        :returns: Angle in sexagesimal format, with ranges properly adjusted.
        :rtype: tuple

        >>> print(Angle.reduce_dms(-743.0, 26.0, 49.6))
        (23, 26, 49.6, -1.0)
        """
        ...
    @staticmethod
    def deg2dms(deg: float | Angle) -> tuple[int, int, float, float]:
        """
        Converts input from decimal to sexagesimal angle format.

        :param deg: Degrees decimal format.
        :type deg: int, float

        :returns: Angle in sexagesimal format, with ranges adjusted.
        :rtype: tuple

        .. note:: The output format is (Degrees, Minutes, Seconds, sign)

        >>> print(Angle.deg2dms(23.44694444))
        (23, 26, 48.999983999997596, 1.0)
        """
        ...
    @staticmethod
    def dms2deg(degrees: float, minutes: float, seconds: float = 0.0) -> float: ...
    def get_tolerance(self) -> float: ...
    def set_tolerance(self, tol: float) -> None: ...
    def __call__(self) -> float: ...

    @overload
    def set(self, *, ra: bool = False) -> None:
        """
        Method used to define the value of the Angle object.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: None.
        :rtype: None
        :raises: TypeError if input values are of wrong type.
        """
        ...
    @overload
    def set(self, a: Angle, /, *, ra: bool = False) -> None:
        """
        Method used to define the value of the Angle object.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: None.
        :rtype: None
        :raises: TypeError if input values are of wrong type.
        """
        ...
    @overload
    def set(self, a: float, /, *, ra: bool = False, radians: bool = False) -> None:
        """
        Method used to define the value of the Angle object.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: None.
        :rtype: None
        :raises: TypeError if input values are of wrong type.
        """
        ...
    @overload
    def set(self, a: list[float] | tuple[float, ...], /, *, ra: bool = False, radians: bool = False) -> None:
        """
        Method used to define the value of the Angle object.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: None.
        :rtype: None
        :raises: TypeError if input values are of wrong type.
        """
        ...
    @overload
    def set(self, a1: float, a2: float, /, *, ra: bool = False) -> None:
        """
        Method used to define the value of the Angle object.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: None.
        :rtype: None
        :raises: TypeError if input values are of wrong type.
        """
        ...
    @overload
    def set(self, a1: float, a2: float, a3: float, /, *, ra: bool = False) -> None:
        """
        Method used to define the value of the Angle object.

        It takes decimals and sexagesimal input. The sexagesimal angles can be
        given as separate degree, minutes, seconds values, or as tuples or
        lists. It is also possible to provide another Angle object as input.

        If **radians=True** is passed, then the input value is converted from
        radians to degrees

        If **ra=True** is passed, then the input value is converted from Right
        Ascension to degrees

        :param args: Input angle, in decimal or sexagesimal format, or Angle
        :type args: int, float, list, tuple, :py:class:`Angle`
        :param radians: If True, input angle is in radians. False by default.
        :type radians: bool
        :param ra: If True, input angle is in Right Ascension. False by default
        :type ra: bool

        :returns: None.
        :rtype: None
        :raises: TypeError if input values are of wrong type.
        """
        ...
    @overload
    def set(self, a1: float, a2: float, a3: float, a4: float, /, *, ra: bool = False) -> None: ...

    def set_radians(self, rads: float) -> None: ...

    @overload
    def set_ra(self) -> None:
        """
        Define the value of the Angle object from a Right Ascension.

        It takes decimals and sexagesimal input. The sexagesimal Right
        Ascensions can be given as separate hours, minutes, seconds values, or
        as tuples or lists.

        :param args: Input Right Ascension, in decimal or sexagesimal format.
        :type args: int, float, list, tuple

        :returns: None.
        :rtype: None
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle()
        >>> a.set_ra(9, 14, 55.8)
        >>> print(a)
        138.7325
        """
        ...
    @overload
    def set_ra(self, a: float | Angle | list[float] | tuple[float, ...], /) -> None:
        """
        Define the value of the Angle object from a Right Ascension.

        It takes decimals and sexagesimal input. The sexagesimal Right
        Ascensions can be given as separate hours, minutes, seconds values, or
        as tuples or lists.

        :param args: Input Right Ascension, in decimal or sexagesimal format.
        :type args: int, float, list, tuple

        :returns: None.
        :rtype: None
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle()
        >>> a.set_ra(9, 14, 55.8)
        >>> print(a)
        138.7325
        """
        ...
    @overload
    def set_ra(self, a1: float, a2: float, /) -> None:
        """
        Define the value of the Angle object from a Right Ascension.

        It takes decimals and sexagesimal input. The sexagesimal Right
        Ascensions can be given as separate hours, minutes, seconds values, or
        as tuples or lists.

        :param args: Input Right Ascension, in decimal or sexagesimal format.
        :type args: int, float, list, tuple

        :returns: None.
        :rtype: None
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle()
        >>> a.set_ra(9, 14, 55.8)
        >>> print(a)
        138.7325
        """
        ...
    @overload
    def set_ra(self, a1: float, a2: float, a3: float, /) -> None:
        """
        Define the value of the Angle object from a Right Ascension.

        It takes decimals and sexagesimal input. The sexagesimal Right
        Ascensions can be given as separate hours, minutes, seconds values, or
        as tuples or lists.

        :param args: Input Right Ascension, in decimal or sexagesimal format.
        :type args: int, float, list, tuple

        :returns: None.
        :rtype: None
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle()
        >>> a.set_ra(9, 14, 55.8)
        >>> print(a)
        138.7325
        """
        ...
    @overload
    def set_ra(self, a1: float, a2: float, a3: float, a4: float, /) -> None: ...

    def dms_str(self, fancy: bool | None = True, n_dec: int = -1) -> str: ...
    def get_ra(self) -> float: ...
    def ra_str(self, fancy: bool | None = True, n_dec: int = -1) -> str: ...
    def rad(self) -> float: ...
    def dms_tuple(self) -> tuple[int, int, float, float]: ...
    def ra_tuple(self) -> tuple[int, int, float, float]: ...
    def to_positive(self) -> Self: ...
    def __eq__(self, b: float | Angle) -> bool: ...  # type: ignore[override]
    def __ne__(self, b: float | Angle) -> bool: ...  # type: ignore[override]
    def __lt__(self, b: float | Angle) -> bool: ...
    def __ge__(self, b: float | Angle) -> bool: ...
    def __gt__(self, b: float | Angle) -> bool: ...
    def __le__(self, b: float | Angle) -> bool: ...
    def __neg__(self) -> Angle: ...
    def __abs__(self) -> Angle: ...
    def __mod__(self, b: float | Angle) -> Angle: ...
    def __add__(self, b: float | Angle) -> Angle: ...
    def __sub__(self, b: float | Angle) -> Angle: ...
    def __mul__(self, b: float | Angle) -> Angle: ...
    def __div__(self, b: float | Angle) -> Angle: ...
    def __truediv__(self, b: float | Angle) -> Angle: ...
    def __pow__(self, b: float | Angle) -> Angle: ...
    def __imod__(self, b: float | Angle) -> Self: ...
    def __iadd__(self, b: float | Angle) -> Self: ...
    def __isub__(self, b: float | Angle) -> Self: ...
    def __imul__(self, b: float | Angle) -> Self: ...
    def __idiv__(self, b: float | Angle) -> Angle: ...
    def __itruediv__(self, b: float | Angle) -> Self: ...
    def __ipow__(self, b: float | Angle) -> Self: ...
    def __rmod__(self, b: float | Angle) -> Angle: ...
    def __radd__(self, b: float | Angle) -> Angle: ...
    def __rsub__(self, b: float | Angle) -> Angle: ...
    def __rmul__(self, b: float | Angle) -> Angle: ...
    def __rdiv__(self, b: float | Angle) -> Angle: ...
    def __rtruediv__(self, b: float | Angle) -> Angle: ...
    def __rpow__(self, b: float | Angle) -> Angle: ...
    def __float__(self) -> float: ...
    def __int__(self) -> int: ...
    def __round__(self, n: float = 0) -> Angle: ...

def main() -> None: ...
