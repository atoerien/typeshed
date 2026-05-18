from typing import Literal, overload

from pymeeus.Angle import Angle
from pymeeus.Epoch import Epoch

class JupiterMoons:
    """
    Class JupiterMoons models the four galilean satellites of Jupiter. With:
    1: Io
    2: Europa
    3: Ganymede
    4: Callisto
    The algorithm used can be found in chapter 44 (high accuracy method) of
    Meeus' book Astronomic Algorithms
    """
    @staticmethod
    def jupiter_system_angles(epoch: Epoch) -> tuple[float, float]:
        """
        This method computes the ascending node of Jupiter as well as
        the node of the equator of Jupiter on the ecliptic (psi).

        :param epoch: Epoch to compute satellites' positions, as an Epoch
            object
        :type epoch: :py:class:`Epoch`
        :returns: Two float values with the ascending node of Jupiter and psi
        :rtype: (float, float)

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> psi_corrected, OMEGA_ascending_node_jupiter =         JupiterMoons.jupiter_system_angles(utc_1992_12_16_00_00_00)
        >>> print(round(psi_corrected, 9))
        317.105800921
        >>> print(round(OMEGA_ascending_node_jupiter, 9))
        100.39249943
        """
        ...
    @staticmethod
    def rectangular_positions_jovian_equatorial(
        epoch: Epoch, tofk5: bool = True, solar: bool = False, do_correction: bool = True
    ) -> tuple[
        tuple[float, float, float], tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]
    ]:
        """
        This method computes the rectangular geocentric position of
        Jupiter's satellites for a given epoch, using the E5-theory.

        :param epoch: Epoch to compute satellites' positions, as an Epoch
            object
        :type epoch: :py:class:`Epoch`
        :param tofk5: Whether or not the small correction to convert to the FK5
            system will be applied or not
        :type tofk5: bool
        :param solar: Whether the satellites' positions are observed from the
            Earth (False) or the Sun (True)
        :type solar: bool
        :param do_correction: Whether the satellites' positions is corrected
            for the effect of different light-time and perspective effect or
            not
        :type do_correction: bool

        :returns: Four tuple with the rectangular X, Y and Z coordinates in
            Jupiter radii (float), where Z is positive if the satellite is more
            distant than Jupiter.
        :rtype: tuple
        :raises: TypeError if input values are of wrong type.

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> io, europa, ganymede, callisto =         JupiterMoons.rectangular_positions_jovian_equatorial(         utc_1992_12_16_00_00_00)
        >>> print(io)
        (-3.450168811390241, 0.21370246960509387, -4.818966623735296)
        >>> print(europa)
        (7.441869121153001, 0.27524463479625677, -5.747104399729193)
        >>> print(ganymede)
        (1.201111684800708, 0.5899903274317162, -14.940581367576527)
        >>> print(callisto)
        (7.072022641384802, 1.0289678450543338, -25.224420329457175)
        """
        ...

    @overload
    @staticmethod
    def apparent_rectangular_coordinates(
        epoch: Epoch,
        X: float,
        Y: float,
        Z: float,
        OMEGA: float,
        psi: float,
        i: float,
        lambda_0: float,
        beta_0: float,
        D: float = 0,
        isFictional: Literal[True] = ...,
    ) -> float:
        """
        This method computes the apparent rectangular coordinates of a
        Jupiter satellite for given coordinates.

        :param epoch: Epoch to compute satellite position, as an Epoch object
        :type epoch: :py:class:`Epoch`
        :param X: X-coordinate of the satellite in Jupiter radii
        :type X: float
        :param Y: Y-coordinate of the satellite in Jupiter radii
        :type Y: float
        :param Z: Z-coordinate of the satellite in Jupiter radii
        :type Z: float
        :param OMEGA: longitude of the node of Jupiter
        :type OMEGA: float
        :param psi: longitude of the node of Jupiter
        :type psi: float
        :param i: inclination on the plane of the ecliptic
        :type i: float
        :param beta_0: Jupiter’s geocentric latitude
        :type beta_0: float
        :param lambda_0: Jupiter’s geocentric longitude
        :type lambda_0: float
        :param D: parameter calculated by the fifth fictional satellite
            (fictional satellite has to be calculated first, in order to
            calculate the coordinates of the remaining "true" satellites)
        :type D: float
        :param isFictional: Whether or not the satellite is the fictional
            satellite No. 5
        :type isFictional: bool

        :returns: A tuple with the apparent rectangular coordinates of the
            satellite or parameter D if isFictional=True
        :rtype: tuple, float
        :raises: TypeError if input values are wrong type

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> psi_corrected = 317.1058009213959
        >>> i_ecliptic_jupiter = 1.3036541530886598
        >>> lambda_0 = -2.9355662143229146
        >>> beta_0 = 0.021667777174910842
        >>> OMEGA_ascending_node_jupiter= 100.39249942976576
        >>> X_1 =  5.60361395790844
        >>> Y_1 = 1.9398758261880644
        >>> Z_1 = 0.00449258104769796
        >>> X_5 =  0
        >>> Y_5 = 0
        >>> Z_5 = 1
        >>> d = JupiterMoons.apparent_rectangular_coordinates(         utc_1992_12_16_00_00_00, X_5, Y_5, Z_5,         OMEGA_ascending_node_jupiter, psi_corrected, i_ecliptic_jupiter,         lambda_0, beta_0, isFictional=True)
        >>> print(round(d, 10))
        -0.0320562469
        >>> io = JupiterMoons.apparent_rectangular_coordinates(         utc_1992_12_16_00_00_00, X_1, Y_1, Z_1,         OMEGA_ascending_node_jupiter, psi_corrected, i_ecliptic_jupiter,         lambda_0, beta_0, d)
        >>> print(io)
        (-3.4489935969836503, 0.21361563816963675, -4.818966623735296)
        """
        ...
    @overload
    @staticmethod
    def apparent_rectangular_coordinates(
        epoch: Epoch,
        X: float,
        Y: float,
        Z: float,
        OMEGA: float,
        psi: float,
        i: float,
        lambda_0: float,
        beta_0: float,
        D: float = 0,
        isFictional: Literal[False] | None = False,
    ) -> tuple[float, float, float]:
        """
        This method computes the apparent rectangular coordinates of a
        Jupiter satellite for given coordinates.

        :param epoch: Epoch to compute satellite position, as an Epoch object
        :type epoch: :py:class:`Epoch`
        :param X: X-coordinate of the satellite in Jupiter radii
        :type X: float
        :param Y: Y-coordinate of the satellite in Jupiter radii
        :type Y: float
        :param Z: Z-coordinate of the satellite in Jupiter radii
        :type Z: float
        :param OMEGA: longitude of the node of Jupiter
        :type OMEGA: float
        :param psi: longitude of the node of Jupiter
        :type psi: float
        :param i: inclination on the plane of the ecliptic
        :type i: float
        :param beta_0: Jupiter’s geocentric latitude
        :type beta_0: float
        :param lambda_0: Jupiter’s geocentric longitude
        :type lambda_0: float
        :param D: parameter calculated by the fifth fictional satellite
            (fictional satellite has to be calculated first, in order to
            calculate the coordinates of the remaining "true" satellites)
        :type D: float
        :param isFictional: Whether or not the satellite is the fictional
            satellite No. 5
        :type isFictional: bool

        :returns: A tuple with the apparent rectangular coordinates of the
            satellite or parameter D if isFictional=True
        :rtype: tuple, float
        :raises: TypeError if input values are wrong type

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> psi_corrected = 317.1058009213959
        >>> i_ecliptic_jupiter = 1.3036541530886598
        >>> lambda_0 = -2.9355662143229146
        >>> beta_0 = 0.021667777174910842
        >>> OMEGA_ascending_node_jupiter= 100.39249942976576
        >>> X_1 =  5.60361395790844
        >>> Y_1 = 1.9398758261880644
        >>> Z_1 = 0.00449258104769796
        >>> X_5 =  0
        >>> Y_5 = 0
        >>> Z_5 = 1
        >>> d = JupiterMoons.apparent_rectangular_coordinates(         utc_1992_12_16_00_00_00, X_5, Y_5, Z_5,         OMEGA_ascending_node_jupiter, psi_corrected, i_ecliptic_jupiter,         lambda_0, beta_0, isFictional=True)
        >>> print(round(d, 10))
        -0.0320562469
        >>> io = JupiterMoons.apparent_rectangular_coordinates(         utc_1992_12_16_00_00_00, X_1, Y_1, Z_1,         OMEGA_ascending_node_jupiter, psi_corrected, i_ecliptic_jupiter,         lambda_0, beta_0, d)
        >>> print(io)
        (-3.4489935969836503, 0.21361563816963675, -4.818966623735296)
        """
        ...

    @staticmethod
    def calculate_delta(
        epoch: Epoch,
    ) -> tuple[float, float, Angle, Angle, float] | tuple[float, float, Literal[0], Literal[0], Literal[0]]:
        """
        This method calculates the distance between Earth and Jupiter
        (DELTA) for a given epoch by iteration.

        :param epoch: Epoch the distance should be calculated for.
        :type epoch: :py:class:`Epoch`

        :returns: Distance Earth-Jupiter in AU and light-time delay from
            Earth-Jupiter, together with Coordinates of Jupiter
        :rtype: tuple

        :raises: TypeError if input values are wrong type

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> delta, tau, l, b, r = JupiterMoons.calculate_delta(         utc_1992_12_16_00_00_00)
        >>> print(round(delta, 10))
        5.6611211815
        >>> print(round(tau, 10))
        0.032695909
        """
        ...

    @overload
    @staticmethod
    def correct_rectangular_positions(
        R: float, i_sat: int, DELTA: float, X_coordinate: list[float] | tuple[float, float, float]
    ) -> tuple[float, float, float]:
        """
        This method corrects the given rectangular coordinates of a Jupiter
        satellite in order to obtain higher accuracy by considering
        differential light-time and the perspective effect.

        :param R: Radius vector of the satellite
        :type R: float
        :param i_sat: Number of the satellite
        :type i_sat: int
        :param DELTA: Distance Observer-Jupiter in AU
        :type DELTA: float
        :param X_coordinate: Uncorrected X-coordinate of the satellite in
            Jupiter's radii or tuple for all coordinates
        :type X_coordinate: float, tuple, list
        :param Y_coordinate: Uncorrected Y-coordinate of the satellite in
            Jupiter's radii
        :type Y_coordinate: float
        :param Z_coordinate: Uncorrected Z-coordinate of the satellite in
            Jupiter's radii
        :type Z_coordinate: float

        :returns: A tuple with the corrected rectangular coordinates (X, Y, Z)
            of the satellite in Jupiter's radii
        :rtype: tuple
        :raises: TypeError if input values are wrong type

        Calculate corrected rectangular Coordinates X, Y and Z in Jupiter's
        radii for Io (1)

        >>> R = 5.929892730360271
        >>> i_sat = 1
        >>> DELTA = 5.6611211815432645
        >>> X_coordinate = -3.4489935969836503
        >>> Y_coordinate = 0.21361563816963675
        >>> Z_coordinate = -4.818966623735296
        >>> io = JupiterMoons.correct_rectangular_positions(R, i_sat, DELTA,         X_coordinate, Y_coordinate, Z_coordinate)
        >>> print(io)
        (-3.450168811390241, 0.21370246960509387, -4.818966623735296)
        """
        ...
    @overload
    @staticmethod
    def correct_rectangular_positions(
        R: float, i_sat: int, DELTA: float, X_coordinate: float, Y_coordinate: float = 0, Z_coordinate: float = 0
    ) -> tuple[float, float, float]:
        """
        This method corrects the given rectangular coordinates of a Jupiter
        satellite in order to obtain higher accuracy by considering
        differential light-time and the perspective effect.

        :param R: Radius vector of the satellite
        :type R: float
        :param i_sat: Number of the satellite
        :type i_sat: int
        :param DELTA: Distance Observer-Jupiter in AU
        :type DELTA: float
        :param X_coordinate: Uncorrected X-coordinate of the satellite in
            Jupiter's radii or tuple for all coordinates
        :type X_coordinate: float, tuple, list
        :param Y_coordinate: Uncorrected Y-coordinate of the satellite in
            Jupiter's radii
        :type Y_coordinate: float
        :param Z_coordinate: Uncorrected Z-coordinate of the satellite in
            Jupiter's radii
        :type Z_coordinate: float

        :returns: A tuple with the corrected rectangular coordinates (X, Y, Z)
            of the satellite in Jupiter's radii
        :rtype: tuple
        :raises: TypeError if input values are wrong type

        Calculate corrected rectangular Coordinates X, Y and Z in Jupiter's
        radii for Io (1)

        >>> R = 5.929892730360271
        >>> i_sat = 1
        >>> DELTA = 5.6611211815432645
        >>> X_coordinate = -3.4489935969836503
        >>> Y_coordinate = 0.21361563816963675
        >>> Z_coordinate = -4.818966623735296
        >>> io = JupiterMoons.correct_rectangular_positions(R, i_sat, DELTA,         X_coordinate, Y_coordinate, Z_coordinate)
        >>> print(io)
        (-3.450168811390241, 0.21370246960509387, -4.818966623735296)
        """
        ...

    @overload
    @staticmethod
    def check_phenomena(epoch: Epoch, check_all: Literal[True] = True, i_sat: int = 0) -> list[list[float]]:
        """
        This method returns the perspective distance to any phenomena of all
        satellites for the given epoch.

        :param epoch: Epoch the calculations should be made for
        :type epoch: :py:class:'Epoch'
        :param check_all: Whether all satellites should be checked
        :type check_all: bool
        :param i_sat: Which satellite should be checked
        :type i_sat: int

        :returns: Distance to the satellite being ecclipsed, occulted in
            penumbra
        :rtype: tuple

        :raises: TypeError if input values are wrong type

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> result_matrix = JupiterMoons.check_phenomena(         utc_1992_12_16_00_00_00)
        >>> print(result_matrix[0])
        [-3.457757270630766, -2.553301264153796, 0.0]
        >>> print(result_matrix[1])
        [-7.44770945299594, -8.33419997337025, 0.0]
        >>> print(result_matrix[2])
        [-1.3572840767173413, -3.817302564886177, 0.0]
        >>> print(result_matrix[3])
        [-7.157430454898491, -11.373611474420906, 0.0]

        >>> io_ecc_start_2021_02_12_14_19_14 = Epoch(2021, 2, 12.5966898148148)
        >>> result_matrix = JupiterMoons.check_phenomena(         io_ecc_start_2021_02_12_14_19_14)
        >>> print([round(result_matrix[0][0], 10), round(result_matrix[0][         1], 10), round(result_matrix[0][2], 10)])
        [1.192605868, 0.8560277162, 0.0]
        >>> print([round(result_matrix[1][0], 10), round(result_matrix[1][         1], 10), round(result_matrix[1][2], 10)])
        [-8.7397202369, -8.8930940921, 0.0]
        >>> print([round(result_matrix[2][0], 10), round(result_matrix[2][         1], 10), round(result_matrix[2][2], 10)])
        [14.0691219925, 13.8323491768, 0.0]
        >>> print([round(result_matrix[3][0], 10), round(result_matrix[3][         1], 10), round(result_matrix[3][2], 10)])
        [-2.9341209156, -3.9904598153, 0.0]
        """
        ...
    @overload
    @staticmethod
    def check_phenomena(epoch: Epoch, check_all: Literal[False] | None, i_sat: int = 0) -> tuple[float, float]:
        """
        This method returns the perspective distance to any phenomena of all
        satellites for the given epoch.

        :param epoch: Epoch the calculations should be made for
        :type epoch: :py:class:'Epoch'
        :param check_all: Whether all satellites should be checked
        :type check_all: bool
        :param i_sat: Which satellite should be checked
        :type i_sat: int

        :returns: Distance to the satellite being ecclipsed, occulted in
            penumbra
        :rtype: tuple

        :raises: TypeError if input values are wrong type

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> result_matrix = JupiterMoons.check_phenomena(         utc_1992_12_16_00_00_00)
        >>> print(result_matrix[0])
        [-3.457757270630766, -2.553301264153796, 0.0]
        >>> print(result_matrix[1])
        [-7.44770945299594, -8.33419997337025, 0.0]
        >>> print(result_matrix[2])
        [-1.3572840767173413, -3.817302564886177, 0.0]
        >>> print(result_matrix[3])
        [-7.157430454898491, -11.373611474420906, 0.0]

        >>> io_ecc_start_2021_02_12_14_19_14 = Epoch(2021, 2, 12.5966898148148)
        >>> result_matrix = JupiterMoons.check_phenomena(         io_ecc_start_2021_02_12_14_19_14)
        >>> print([round(result_matrix[0][0], 10), round(result_matrix[0][         1], 10), round(result_matrix[0][2], 10)])
        [1.192605868, 0.8560277162, 0.0]
        >>> print([round(result_matrix[1][0], 10), round(result_matrix[1][         1], 10), round(result_matrix[1][2], 10)])
        [-8.7397202369, -8.8930940921, 0.0]
        >>> print([round(result_matrix[2][0], 10), round(result_matrix[2][         1], 10), round(result_matrix[2][2], 10)])
        [14.0691219925, 13.8323491768, 0.0]
        >>> print([round(result_matrix[3][0], 10), round(result_matrix[3][         1], 10), round(result_matrix[3][2], 10)])
        [-2.9341209156, -3.9904598153, 0.0]
        """
        ...

    @staticmethod
    def is_phenomena(epoch: Epoch) -> list[list[bool]]:
        """
        This method checks if the given coordinates correspond with any
        satellite
        phenomena. It returns the type of phenomena for all satellites.

        :param epoch: Epoch the calculations should be made for
        :type epoch: :py:class:'Epoch'

        :returns: Result matrix for the four Galilean satellites
            Row 0: Io            Column 0: Occultation
            Row 1: Europa        Column 1: Eclipse
            Row 2: Ganymede      Column 2: No use
            Row 3: Callisto
        :rtype: tuple

        :raises: TypeError if input values are wrong type

        Calculation of result matrix for December 16 at 0h UTC

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> result_matrix = JupiterMoons.is_phenomena(utc_1992_12_16_00_00_00)
        >>> print(result_matrix[0])
        [False, False, False]
        >>> print(result_matrix[1])
        [False, False, False]
        >>> print(result_matrix[2])
        [False, False, False]
        >>> print(result_matrix[3])
        [False, False, False]
        >>> io_ecc_start_2021_02_12_14_19_14 = Epoch(2021, 2, 12.5966898148148)
        >>> result_matrix = JupiterMoons.is_phenomena(         io_ecc_start_2021_02_12_14_19_14)
        >>> print(result_matrix[0])
        [False, True, False]
        >>> print(result_matrix[1])
        [False, False, False]
        >>> print(result_matrix[2])
        [False, False, False]
        >>> print(result_matrix[3])
        [False, False, False]
        """
        ...
    @staticmethod
    def check_coordinates(X: float, Y: float) -> float:
        """
        This method checks if the given coordinates correspond with a
        satellite
        phenomena. It returns if the satellite with the given coordinates is
        hidden
        behind Jupiter or directly in front.

        :param X: X-coordinate of the satellite in Jupiter's radii
        :type X: float
        :param Y: Y-coordinate of the satellite in Jupiter's radii
        :type Y: float

        :returns: Perspective distance to Jupiter's center in Jupiter's radii
        :rtype: float

        Calculation of the perspective distance of the planet Io to the
        center of Jupiter
        for December 16 at 0h UTC as seen from the Earth

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> result_matrix =         JupiterMoons.rectangular_positions_jovian_equatorial(         utc_1992_12_16_00_00_00, solar=False)
        >>> io_radius_to_center_of_jupiter_earth =         JupiterMoons.check_coordinates(result_matrix[0][0], result_matrix[         0][1])
        >>> print(round(io_radius_to_center_of_jupiter_earth, 10))
        3.4577572706
        """
        ...
    @staticmethod
    def check_occultation(
        X: float = 0, Y: float = 0, Z: float = 0, epoch: Epoch | None = None, i_sat: int | None = None
    ) -> float:
        """
        This method checks if the given coordinates or Epoch correspond
        with a satellite being in occultation.

        :param X: X-coordinate of the satellite in Jupiter's radii
        :type X: float
        :param Y: Y-coordinate of the satellite in Jupiter's radii
        :type Y: float
        :param Z: Z-coordinate of the satellite in Jupiter's radii
        :type Z: float
        :param epoch: Epoch that should be checked
        :type epoch: :py:class:`Epoch`
        :param i_sat: Index of the satellite (only for given Epoch)
        :type i_sat: int

        :returns: Perspective distance to center of Jupiter in Jupiter radii
            as seen from the Earth (value of perspective distance is negative
            when the satellite is closer to the Earth than Jupiter, otherwise
            positive)
        :rtype: float
        :raises: TypeError if input values are wrong type


        Calculation of the perspective distance of the planet Io
        squareroot(X^2 + Y^2) to the center of Jupiter for December 16 at 0h
        UTC as seen from the Earth

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> result_matrix =         JupiterMoons.rectangular_positions_jovian_equatorial(         utc_1992_12_16_00_00_00, solar=False)
        >>> io_distance_to_center_of_jupiter_earthview =         JupiterMoons.check_occultation(result_matrix[0][0], result_matrix[         0][1])
        >>> print(round(io_distance_to_center_of_jupiter_earthview, 10))
        -3.4577572706
        """
        ...
    @staticmethod
    def check_eclipse(
        X_0: float = 0, Y_0: float = 0, Z_0: float = 0, epoch: Epoch | None = None, i_sat: int | None = None
    ) -> float:
        """
        This method checks if the given coordinates or Epoch correspond
        with a satellite being in eclipse.

        :param X_0: X-coordinate of the satellite in Jupiter's radii
            observed from the sun
        :type X_0: float
        :param Y_0: Y-coordinate of the satellite in Jupiter's radii
            observed from the sun
        :type Y_0: float
        :param Z_0: Z-coordinate of the satellite in Jupiter's radii
            observed from the sun
        :type Z_0: float
        :param epoch: Epoch that should be checked
        :type epoch: :py:class:`Epoch`
        :param i_sat: Index of the satellite (only for given Epoch)
        :type i_sat: int

        :returns: perspective distance to center of Jupiter in Jupiter radii
            as seen from the Sun (value of perspective distance is negative
            when the satellite is closer to the Sun than Jupiter, otherwise
            positive)
        :rtype: float
        :raises: TypeError if input values are wrong type


        Calculation of the Perspective distance of the planet Io
        squareroot(X_0^2 + Y_0^2) to the center of Jupiter for December 16 at
        0h UTC as seen from the Sun

        >>> utc_1992_12_16_00_00_00 = Epoch(1992, 12, 16, utc=True)
        >>> result_matrix =         JupiterMoons.rectangular_positions_jovian_equatorial(         utc_1992_12_16_00_00_00, solar=True)
        >>> io_radius_to_center_of_jupiter_sunview =         JupiterMoons.check_eclipse(result_matrix[0][0], result_matrix[0][1])
        >>> print(round(io_radius_to_center_of_jupiter_sunview, 10))
        -2.5533012642
        """
        ...

def main() -> None: ...
