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
    def __init__(self, a1: float, a2: float, a3: float, a4: float, /, *, ra: bool = False) -> None:
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
    def dms2deg(degrees: float, minutes: float, seconds: float = 0.0) -> float:
        """
        Converts an angle from sexagesimal to decimal format.

        :param degrees: Degrees.
        :type degrees: int, float
        :param minutes: Minutes.
        :type minutes: int, float
        :param seconds: Seconds. 0.0 by default.
        :type seconds: int, float

        :returns: Angle in decimal format, within +/-[0:360) range.
        :rtype: float

        >>> print(Angle.dms2deg(-23, 26, 48.999983999997596))
        -23.44694444
        """
        ...
    def get_tolerance(self) -> float:
        """
        Gets the internal tolerance value used to compare Angles.

        .. note:: The default tolerance value is **base.TOL**.

        :returns: Internal tolerance.
        :rtype: float
        """
        ...
    def set_tolerance(self, tol: float) -> None:
        """
        Changes the internal tolerance value used to compare Angles.

        :param tol: New tolerance value.
        :type tol: int, float

        :returns: None
        :rtype: None
        """
        ...
    def __call__(self) -> float:
        """
        Method used when object is called only with parenthesis.

        :returns: The internal value of the Angle object.
        :rtype: int, float

        >>> a = Angle(54.6)
        >>> print(a())
        54.6
        """
        ...

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
    def set(self, a1: float, a2: float, a3: float, a4: float, /, *, ra: bool = False) -> None:
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

    def set_radians(self, rads: float) -> None:
        """
        Method to define the value of the Angle object from radians.

        :param rads: Input angle, in radians.
        :type rads: int, float

        :returns: None.
        :rtype: None
        :raises: TypeError if input value is of wrong type.

        >>> a = Angle()
        >>> a.set_radians(pi)
        >>> print(a)
        180.0
        """
        ...

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
    def set_ra(self, a1: float, a2: float, a3: float, a4: float, /) -> None:
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

    def dms_str(self, fancy: bool | None = True, n_dec: int = -1) -> str:
        """
        Returns the Angle value as a sexagesimal string.

        The parameter **fancy** allows to print in "Dd M' S''" format if True,
        and in "D:M:S" (easier to parse) if False. On the other hand, the
        **n_dec** parameter sets the number of decimals used to print the
        seconds. Set to a negative integer to disable (default).

        :param fancy: Format of output string. True by default.
        :type fancy: bool
        :param n_dec: Number of decimals used to print the seconds
        :type fancy: int

        :returns: Angle value as string in sexagesimal format.
        :rtype: string
        :raises: TypeError if input value is of wrong type.

        >>> a = Angle(42.75)
        >>> print(a.dms_str())
        42d 45' 0.0''
        >>> print(a.dms_str(fancy=False))
        42:45:0.0
        >>> a = Angle(49, 13, 42.4817)
        >>> print(a.dms_str(n_dec=2))
        49d 13' 42.48''
        """
        ...
    def get_ra(self) -> float:
        """
        Returns the Angle value as a Right Ascension in float format

        :returns: The internal value of the Angle object as Right Ascension.
        :rtype: int, float

        >>> a = Angle(138.75)
        >>> print(a.get_ra())
        9.25
        """
        ...
    def ra_str(self, fancy: bool | None = True, n_dec: int = -1) -> str:
        """
        Returns the Angle value as a sexagesimal string in Right Ascension.

        The parameter **fancy** allows to print in "Hh M' S''" format if True,
        and in "H:M:S" (easier to parse) if False. On the other hand, the
        **n_dec** parameter sets the number of decimals used to print the
        seconds. Set to a negative integer to disable (default).

        :param fancy: Format of output string. True by default.
        :type fancy: bool
        :param n_dec: Number of decimals used to print the seconds
        :type fancy: int

        :returns: Angle value as Right Ascension in sexagesimal format.
        :rtype: string
        :raises: TypeError if input value is of wrong type.

        >>> a = Angle(138.75)
        >>> print(a.ra_str())
        9h 15' 0.0''
        >>> print(a.ra_str(fancy=False))
        9:15:0.0
        >>> a = Angle(2, 44, 11.98581, ra=True)
        >>> print(a.ra_str(n_dec=3))
        2h 44' 11.986''
        """
        ...
    def rad(self) -> float:
        """
        Returns the Angle value in radians.

        :returns: Angle value in radians.
        :rtype: float

        >>> a = Angle(47.762)
        >>> print(round(a.rad(), 8))
        0.83360416
        """
        ...
    def dms_tuple(self) -> tuple[int, int, float, float]:
        """
        Returns the Angle as a tuple containing (degrees, minutes, seconds,
        sign).

        :returns: Angle value as (degrees, minutes, seconds, sign).
        :rtype: tuple
        """
        ...
    def ra_tuple(self) -> tuple[int, int, float, float]:
        """
        Returns the Angle in Right Ascension format as a tuple containing
        (hours, minutes, seconds, sign).

        :returns: Angle value as RA in (hours, minutes, seconds, sign) format.
        :rtype: tuple
        """
        ...
    def to_positive(self) -> Self:
        """
        Converts the internal angle value from negative to positive.

        :returns: This angle object.
        :rtype: :py:class:`Angle`

        >>> a = Angle(-87.32)
        >>> print(a.to_positive())
        272.68
        """
        ...
    def __eq__(self, b: float | Angle) -> bool:
        """
        This method defines the 'is equal' operator between Angles.

        .. note:: For the comparison, the internal tolerance value is used.

        :returns: A boolean.
        :rtype: bool
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(172.01)
        >>> b = Angle(172.009)
        >>> a == b
        False
        """
        ...
    def __ne__(self, b: float | Angle) -> bool:
        """
        This method defines the 'is not equal' operator between Angles.

        .. note:: For the comparison, the internal tolerance value is used.

        :returns: A boolean.
        :rtype: bool

        >>> a = Angle(11.200001)
        >>> b = Angle(11.200000)
        >>> a != b
        True
        """
        ...
    def __lt__(self, b: float | Angle) -> bool:
        """
        This method defines the 'is less than' operator between Angles.

        :returns: A boolean.
        :rtype: bool
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(72.0)
        >>> b = Angle(72.0)
        >>> a < b
        False
        """
        ...
    def __ge__(self, b: float | Angle) -> bool:
        """
        This method defines 'is equal or greater' operator between Angles.

        :returns: A boolean.
        :rtype: bool
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(172.01)
        >>> b = Angle(172.009)
        >>> a >= b
        True
        """
        ...
    def __gt__(self, b: float | Angle) -> bool:
        """
        This method defines the 'is greater than' operator between Angles.

        :returns: A boolean.
        :rtype: bool
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(172.01)
        >>> b = Angle(172.009)
        >>> a > b
        True
        """
        ...
    def __le__(self, b: float | Angle) -> bool:
        """
        This method defines 'is equal or less' operator between Angles.

        :returns: A boolean.
        :rtype: bool
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(72.0)
        >>> b = Angle(72.0)
        >>> a <= b
        True
        """
        ...
    def __neg__(self) -> Angle:
        """
        This method is used to obtain the negative version of this Angle.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`

        >>> a = Angle(-11.2)
        >>> print(-a)
        11.2
        """
        ...
    def __abs__(self) -> Angle:
        """
        This method is used to obtain the absolute value of this Angle.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`

        >>> a = Angle(-303.67)
        >>> print(abs(a))
        303.67
        """
        ...
    def __mod__(self, b: float | Angle) -> Angle:
        """
        This method is used to obtain the module b of this Angle.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(333.0)
        >>> b = Angle(72.0)
        >>> print(a % b)
        45.0
        """
        ...
    def __add__(self, b: float | Angle) -> Angle:
        """
        This method defines the addition between Angles.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(83.1)
        >>> b = Angle(18.4)
        >>> print(a + b)
        101.5
        """
        ...
    def __sub__(self, b: float | Angle) -> Angle:
        """
        This method defines the subtraction between Angles.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(25.4)
        >>> b = Angle(10.2)
        >>> print(a - b)
        15.2
        """
        ...
    def __mul__(self, b: float | Angle) -> Angle:
        """
        This method defines the multiplication between Angles.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(33.0)
        >>> b = Angle(72.0)
        >>> print(a * b)
        216.0
        """
        ...
    def __div__(self, b: float | Angle) -> Angle:
        """
        This method defines the division between Angles.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: ZeroDivisionError if divisor is zero.
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(172.0)
        >>> b = Angle(86.0)
        >>> print(a/b)
        2.0
        """
        ...
    def __truediv__(self, b: float | Angle) -> Angle:
        """
        This method defines the division between Angles (Python 3).

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: ZeroDivisionError if divisor is zero.
        :raises: TypeError if input values are of wrong type.
        :see: __div__
        """
        ...
    def __pow__(self, b: float | Angle) -> Angle:
        """
        This method defines the power operation for Angles.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(12.5)
        >>> b = Angle(4.0)
        >>> print(a ** b)
        294.0625
        """
        ...
    def __imod__(self, b: float | Angle) -> Self:
        """
        This method defines the accumulative module b of this Angle.

        :returns: This Angle.
        :rtype: :py:class:`Angle`

        >>> a = Angle(330.0)
        >>> b = Angle(45.0)
        >>> a %= b
        >>> print(a)
        15.0
        """
        ...
    def __iadd__(self, b: float | Angle) -> Self:
        """
        This method defines the accumulative addition to this Angle.

        :returns: This Angle.
        :rtype: :py:class:`Angle`

        >>> a = Angle(172.1)
        >>> b = Angle(54.6)
        >>> a += b
        >>> print(a)
        226.7
        """
        ...
    def __isub__(self, b: float | Angle) -> Self:
        """
        This method defines the accumulative subtraction to this Angle.

        :returns: This Angle.
        :rtype: :py:class:`Angle`

        >>> a = Angle(97.0)
        >>> b = Angle(39.0)
        >>> a -= b
        >>> print(a)
        58.0
        """
        ...
    def __imul__(self, b: float | Angle) -> Self:
        """
        This method defines the accumulative multiplication to this Angle.

        :returns: This Angle.
        :rtype: :py:class:`Angle`

        >>> a = Angle(30.0)
        >>> b = Angle(55.0)
        >>> a *= b
        >>> print(a)
        210.0
        """
        ...
    def __idiv__(self, b: float | Angle) -> Angle:
        """
        This method defines the accumulative division to this Angle.

        :returns: This Angle.
        :rtype: :py:class:`Angle`
        :raises: ZeroDivisionError if divisor is zero.
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(330.0)
        >>> b = Angle(30.0)
        >>> a /= b
        >>> print(a)
        11.0
        """
        ...
    def __itruediv__(self, b: float | Angle) -> Self:
        """
        This method defines accumulative division to this Angle (Python3).

        :returns: This Angle.
        :rtype: :py:class:`Angle`
        :raises: ZeroDivisionError if divisor is zero.
        :raises: TypeError if input values are of wrong type.
        :see: __idiv__
        """
        ...
    def __ipow__(self, b: float | Angle) -> Self:
        """
        This method defines the accumulative power to this Angle.

        :returns: This Angle.
        :rtype: :py:class:`Angle`

        >>> a = Angle(37.0)
        >>> b = Angle(3.0)
        >>> a **= b
        >>> print(a)
        253.0
        """
        ...
    def __rmod__(self, b: float | Angle) -> Angle:
        """
        This method defines module operation between Angles by the right.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`

        >>> a = Angle(80.0)
        >>> print(350 % a)
        30.0
        """
        ...
    def __radd__(self, b: float | Angle) -> Angle:
        """
        This method defines the addition between Angles by the right

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`

        >>> a = Angle(83.1)
        >>> print(8.5 + a)
        91.6
        """
        ...
    def __rsub__(self, b: float | Angle) -> Angle:
        """
        This method defines the subtraction between Angles by the right.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(25.0)
        >>> print(24.0 - a)
        -1.0
        """
        ...
    def __rmul__(self, b: float | Angle) -> Angle:
        """
        This method defines multiplication between Angles by the right.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(11.0)
        >>> print(250.0 * a)
        230.0
        """
        ...
    def __rdiv__(self, b: float | Angle) -> Angle:
        """
        This method defines division between Angles by the right.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: ZeroDivisionError if divisor is zero.
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(80.0)
        >>> print(350 / a)
        4.375
        """
        ...
    def __rtruediv__(self, b: float | Angle) -> Angle:
        """
        This method defines division between Angle by the right (Python3).

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: ZeroDivisionError if divisor is zero.
        :raises: TypeError if input values are of wrong type.
        :see: __rdiv__
        """
        ...
    def __rpow__(self, b: float | Angle) -> Angle:
        """
        This method defines the power operation for Angles by the right.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`
        :raises: TypeError if input values are of wrong type.

        >>> a = Angle(5.0)
        >>> print(24.0 ** a)
        144.0
        """
        ...
    def __float__(self) -> float:
        """
        This method returns Angle value as a float.

        :returns: Internal angle value as a float.
        :rtype: float

        >>> a = Angle(213.8)
        >>> float(a)
        213.8
        """
        ...
    def __int__(self) -> int:
        """
        This method returns Angle value as an int.

        :returns: Internal angle value as an int.
        :rtype: int

        >>> a = Angle(213.8)
        >>> int(a)
        213
        """
        ...
    def __round__(self, n: float = 0) -> Angle:
        """
        This method returns an Angle with content rounded to 'n' decimal.

        :returns: A new Angle object.
        :rtype: :py:class:`Angle`

        >>> a = Angle(11.4361)
        >>> print(round(a, 2))
        11.44
        """
        ...

def main() -> None: ...
