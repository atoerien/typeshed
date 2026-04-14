"""
PyAudio provides Python bindings for PortAudio, the cross-platform
audio I/O library. With PyAudio, you can easily use Python to play and
record audio on a variety of platforms.

.. include:: ../sphinx/examples.rst

Overview
--------

**Classes**
  :py:class:`PyAudio`, :py:class:`PyAudio.Stream`

.. only:: pamac

   **Host Specific Classes**
     :py:class:`PaMacCoreStreamInfo`

**Stream Conversion Convenience Functions**
  :py:func:`get_sample_size`, :py:func:`get_format_from_width`

**PortAudio version**
  :py:func:`get_portaudio_version`, :py:func:`get_portaudio_version_text`

.. |PaSampleFormat| replace:: :ref:`PortAudio Sample Format <PaSampleFormat>`
.. _PaSampleFormat:

**Portaudio Sample Formats**
  :py:data:`paFloat32`, :py:data:`paInt32`, :py:data:`paInt24`,
  :py:data:`paInt16`, :py:data:`paInt8`, :py:data:`paUInt8`,
  :py:data:`paCustomFormat`

.. |PaHostAPI| replace:: :ref:`PortAudio Host API <PaHostAPI>`
.. _PaHostAPI:

**PortAudio Host APIs**
  :py:data:`paInDevelopment`, :py:data:`paDirectSound`, :py:data:`paMME`,
  :py:data:`paASIO`, :py:data:`paSoundManager`, :py:data:`paCoreAudio`,
  :py:data:`paOSS`, :py:data:`paALSA`, :py:data:`paAL`, :py:data:`paBeOS`,
  :py:data:`paWDMKS`, :py:data:`paJACK`, :py:data:`paWASAPI`,
  :py:data:`paNoDevice`

.. |PaErrorCode| replace:: :ref:`PortAudio Error Code <PaErrorCode>`
.. _PaErrorCode:

**PortAudio Error Codes**
  :py:data:`paNoError`, :py:data:`paNotInitialized`,
  :py:data:`paUnanticipatedHostError`, :py:data:`paInvalidChannelCount`,
  :py:data:`paInvalidSampleRate`, :py:data:`paInvalidDevice`,
  :py:data:`paInvalidFlag`, :py:data:`paSampleFormatNotSupported`,
  :py:data:`paBadIODeviceCombination`, :py:data:`paInsufficientMemory`,
  :py:data:`paBufferTooBig`, :py:data:`paBufferTooSmall`,
  :py:data:`paNullCallback`, :py:data:`paBadStreamPtr`,
  :py:data:`paTimedOut`, :py:data:`paInternalError`,
  :py:data:`paDeviceUnavailable`,
  :py:data:`paIncompatibleHostApiSpecificStreamInfo`,
  :py:data:`paStreamIsStopped`, :py:data:`paStreamIsNotStopped`,
  :py:data:`paInputOverflowed`, :py:data:`paOutputUnderflowed`,
  :py:data:`paHostApiNotFound`, :py:data:`paInvalidHostApi`,
  :py:data:`paCanNotReadFromACallbackStream`,
  :py:data:`paCanNotWriteToACallbackStream`,
  :py:data:`paCanNotReadFromAnOutputOnlyStream`,
  :py:data:`paCanNotWriteToAnInputOnlyStream`,
  :py:data:`paIncompatibleStreamHostApi`

.. |PaCallbackReturnCodes| replace:: :ref:`PortAudio Callback Return Code <PaCallbackReturnCodes>`
.. _PaCallbackReturnCodes:

**PortAudio Callback Return Codes**
  :py:data:`paContinue`, :py:data:`paComplete`, :py:data:`paAbort`

.. |PaCallbackFlags| replace:: :ref:`PortAutio Callback Flag <PaCallbackFlags>`
.. _PaCallbackFlags:

**PortAudio Callback Flags**
  :py:data:`paInputUnderflow`, :py:data:`paInputOverflow`,
  :py:data:`paOutputUnderflow`, :py:data:`paOutputOverflow`,
  :py:data:`paPrimingOutput`
"""

import sys
from collections.abc import Callable, Mapping, Sequence
from typing import ClassVar, Final
from typing_extensions import TypeAlias

__docformat__: str

paFloat32: Final[int]
paInt32: Final[int]
paInt24: Final[int]
paInt16: Final[int]
paInt8: Final[int]
paUInt8: Final[int]
paCustomFormat: Final[int]

paInDevelopment: Final[int]
paDirectSound: Final[int]
paMME: Final[int]
paASIO: Final[int]
paSoundManager: Final[int]
paCoreAudio: Final[int]
paOSS: Final[int]
paALSA: Final[int]
paAL: Final[int]
paBeOS: Final[int]
paWDMKS: Final[int]
paJACK: Final[int]
paWASAPI: Final[int]
paNoDevice: Final[int]

paNoError: Final[int]
paNotInitialized: Final[int]
paUnanticipatedHostError: Final[int]
paInvalidChannelCount: Final[int]
paInvalidSampleRate: Final[int]
paInvalidDevice: Final[int]
paInvalidFlag: Final[int]
paSampleFormatNotSupported: Final[int]
paBadIODeviceCombination: Final[int]
paInsufficientMemory: Final[int]
paBufferTooBig: Final[int]
paBufferTooSmall: Final[int]
paNullCallback: Final[int]
paBadStreamPtr: Final[int]
paTimedOut: Final[int]
paInternalError: Final[int]
paDeviceUnavailable: Final[int]
paIncompatibleHostApiSpecificStreamInfo: Final[int]
paStreamIsStopped: Final[int]
paStreamIsNotStopped: Final[int]
paInputOverflowed: Final[int]
paOutputUnderflowed: Final[int]
paHostApiNotFound: Final[int]
paInvalidHostApi: Final[int]
paCanNotReadFromACallbackStream: Final[int]
paCanNotWriteToACallbackStream: Final[int]
paCanNotReadFromAnOutputOnlyStream: Final[int]
paCanNotWriteToAnInputOnlyStream: Final[int]
paIncompatibleStreamHostApi: Final[int]

paContinue: Final[int]
paComplete: Final[int]
paAbort: Final[int]

paInputUnderflow: Final[int]
paInputOverflow: Final[int]
paOutputUnderflow: Final[int]
paOutputOverflow: Final[int]
paPrimingOutput: Final[int]

paFramesPerBufferUnspecified: Final[int]

if sys.platform == "darwin":
    class PaMacCoreStreamInfo:
        paMacCoreChangeDeviceParameters: Final[int]
        paMacCoreFailIfConversionRequired: Final[int]
        paMacCoreConversionQualityMin: Final[int]
        paMacCoreConversionQualityMedium: Final[int]
        paMacCoreConversionQualityLow: Final[int]
        paMacCoreConversionQualityHigh: Final[int]
        paMacCoreConversionQualityMax: Final[int]
        paMacCorePlayNice: Final[int]
        paMacCorePro: Final[int]
        paMacCoreMinimizeCPUButPlayNice: Final[int]
        paMacCoreMinimizeCPU: Final[int]
        def __init__(self, flags: int | None = ..., channel_map: _ChannelMap | None = ...) -> None: ...
        def get_flags(self) -> int: ...
        def get_channel_map(self) -> _ChannelMap | None: ...

    _PaMacCoreStreamInfo: TypeAlias = PaMacCoreStreamInfo
else:
    _PaMacCoreStreamInfo: TypeAlias = None

# Auxiliary types
_ChannelMap: TypeAlias = Sequence[int]
_PaHostApiInfo: TypeAlias = Mapping[str, str | int]
_PaDeviceInfo: TypeAlias = Mapping[str, str | int | float]
_StreamCallback: TypeAlias = Callable[[bytes | None, int, Mapping[str, float], int], tuple[bytes | None, int]]

def get_format_from_width(width: int, unsigned: bool = ...) -> int:
    """
    Returns a PortAudio format constant for the specified *width*.

    :param width: The desired sample width in bytes (1, 2, 3, or 4)
    :param unsigned: For 1 byte width, specifies signed or unsigned format.

    :raises ValueError: when invalid *width*
    :rtype: A |PaSampleFormat| constant
    """
    ...
def get_portaudio_version() -> int:
    """
    Returns portaudio version.

    :rtype: int
    """
    ...
def get_portaudio_version_text() -> str:
    """
    Returns PortAudio version as a text string.

    :rtype: string
    """
    ...
def get_sample_size(format: int) -> int:
    """
    Returns the size (in bytes) for the specified sample *format*.

    :param format: A |PaSampleFormat| constant.
    :raises ValueError: on invalid specified `format`.
    :rtype: integer
    """
    ...

class Stream:
    """Reserved. Do not instantiate."""
    def __init__(
        self,
        PA_manager: PyAudio,
        rate: int,
        channels: int,
        format: int,
        input: bool = ...,
        output: bool = ...,
        input_device_index: int | None = ...,
        output_device_index: int | None = ...,
        frames_per_buffer: int = ...,
        start: bool = ...,
        input_host_api_specific_stream_info: _PaMacCoreStreamInfo | None = ...,
        output_host_api_specific_stream_info: _PaMacCoreStreamInfo | None = ...,
        stream_callback: _StreamCallback | None = ...,
    ) -> None: ...
    def close(self) -> None:
        """Closes the stream."""
        ...
    def get_cpu_load(self) -> float:
        """
        Return the CPU load. Always 0.0 when using the blocking API.

        :rtype: float
        """
        ...
    def get_input_latency(self) -> float:
        """
        Returns the input latency.

        :rtype: float
        """
        ...
    def get_output_latency(self) -> float:
        """
        Returns the output latency.

        :rtype: float
        """
        ...
    def get_read_available(self) -> int:
        """
        Return the number of frames that can be read without waiting.

        :rtype: integer
        """
        ...
    def get_time(self) -> float:
        """
        Returns stream time.

        :rtype: float
        """
        ...
    def get_write_available(self) -> int:
        """
        Return the number of frames that can be written without waiting.

        :rtype: integer
        """
        ...
    def is_active(self) -> bool:
        """
        Returns whether the stream is active.

        :rtype: bool
        """
        ...
    def is_stopped(self) -> bool:
        """
        Returns whether the stream is stopped.

        :rtype: bool
        """
        ...
    def read(self, num_frames: int, exception_on_overflow: bool = ...) -> bytes:
        """
        Read samples from the stream.

        Do not call when using non-blocking mode.

        :param num_frames: The number of frames to read.
        :param exception_on_overflow:
           Specifies whether an IOError exception should be thrown
           (or silently ignored) on input buffer overflow. Defaults
           to True.
        :raises IOError: if stream is not an input stream
          or if the read operation was unsuccessful.
        :rtype: bytes
        """
        ...
    def start_stream(self) -> None:
        """Starts the stream."""
        ...
    def stop_stream(self) -> None:
        """Stops the stream."""
        ...
    def write(self, frames: bytes, num_frames: int | None = ..., exception_on_underflow: bool = ...) -> None:
        """
        Write samples to the stream for playback.

        Do not call when using non-blocking mode.

        :param frames:
           The frames of data.
        :param num_frames:
           The number of frames to write.
           Defaults to None, in which this value will be
           automatically computed.
        :param exception_on_underflow:
           Specifies whether an IOError exception should be thrown
           (or silently ignored) on buffer underflow. Defaults
           to False for improved performance, especially on
           slower platforms.

        :raises IOError: if the stream is not an output stream
           or if the write operation was unsuccessful.

        :rtype: `None`
        """
        ...

# Use an alias to workaround pyright complaints about recursive definitions in the PyAudio class
_Stream = Stream

class PyAudio:
    """
    Python interface to PortAudio.

    Provides methods to:
     - initialize and terminate PortAudio
     - open and close streams
     - query and inspect the available PortAudio Host APIs
     - query and inspect the available PortAudio audio devices.

    **Stream Management**
      :py:func:`open`, :py:func:`close`

    **Host API**
      :py:func:`get_host_api_count`, :py:func:`get_default_host_api_info`,
      :py:func:`get_host_api_info_by_type`,
      :py:func:`get_host_api_info_by_index`,
      :py:func:`get_device_info_by_host_api_device_index`

    **Device API**
      :py:func:`get_device_count`, :py:func:`is_format_supported`,
      :py:func:`get_default_input_device_info`,
      :py:func:`get_default_output_device_info`,
      :py:func:`get_device_info_by_index`

    **Stream Format Conversion**
      :py:func:`get_sample_size`, :py:func:`get_format_from_width`

    **Details**
    """
    Stream: ClassVar[type[_Stream]]
    def __init__(self) -> None:
        """Initialize PortAudio."""
        ...
    def close(self, stream: _Stream) -> None:
        """
        Closes a stream. Use :py:func:`PyAudio.Stream.close` instead.

        :param stream: An instance of the :py:class:`PyAudio.Stream` object.
        :raises ValueError: if stream does not exist.
        """
        ...
    def get_default_host_api_info(self) -> _PaHostApiInfo:
        """
        Returns a dictionary containing the default Host API parameters.

        The keys of the dictionary mirror the data fields of PortAudio's
        ``PaHostApiInfo`` structure.

        :raises IOError: if no default input device is available
        :rtype: dict
        """
        ...
    def get_default_input_device_info(self) -> _PaDeviceInfo:
        """
        Returns the default input device parameters as a dictionary.

        The keys of the dictionary mirror the data fields of PortAudio's
        ``PaDeviceInfo`` structure.

        :raises IOError: No default input device available.
        :rtype: dict
        """
        ...
    def get_default_output_device_info(self) -> _PaDeviceInfo:
        """
        Returns the default output device parameters as a dictionary.

        The keys of the dictionary mirror the data fields of PortAudio's
        ``PaDeviceInfo`` structure.

        :raises IOError: No default output device available.
        :rtype: dict
        """
        ...
    def get_device_count(self) -> int:
        """
        Returns the number of PortAudio Host APIs.

        :rtype: integer
        """
        ...
    def get_device_info_by_host_api_device_index(self, host_api_index: int, host_api_device_index: int) -> _PaDeviceInfo:
        """
        Returns a dictionary containing the Device parameters for a
        given Host API's n'th device. The keys of the dictionary
        mirror the data fields of PortAudio's ``PaDeviceInfo`` structure.

        :param host_api_index: The Host API index number
        :param host_api_device_index: The n'th device of the host API
        :raises IOError: for invalid indices
        :rtype: dict
        """
        ...
    def get_device_info_by_index(self, device_index: int) -> _PaDeviceInfo:
        """
        Returns the device parameters for device specified in `device_index`
        as a dictionary. The keys of the dictionary mirror the data fields of
        PortAudio's ``PaDeviceInfo`` structure.

        :param device_index: The device index
        :raises IOError: Invalid `device_index`.
        :rtype: dict
        """
        ...
    def get_format_from_width(self, width: int, unsigned: bool = ...) -> int:
        """
        Returns a PortAudio format constant for the specified `width`.

        :param width: The desired sample width in bytes (1, 2, 3, or 4)
        :param unsigned: For 1 byte width, specifies signed or unsigned format.

        :raises ValueError: for invalid `width`
        :rtype: A |PaSampleFormat| constant.
        """
        ...
    def get_host_api_count(self) -> int:
        """
        Returns the number of available PortAudio Host APIs.

        :rtype: integer
        """
        ...
    def get_host_api_info_by_index(self, host_api_index: int) -> _PaHostApiInfo:
        """
        Returns a dictionary containing the Host API parameters for the
        host API specified by the `host_api_index`. The keys of the
        dictionary mirror the data fields of PortAudio's ``PaHostApiInfo``
        structure.

        :param host_api_index: The host api index
        :raises IOError: for invalid `host_api_index`
        :rtype: dict
        """
        ...
    def get_host_api_info_by_type(self, host_api_type: int) -> _PaHostApiInfo:
        """
        Returns a dictionary containing the Host API parameters for the
        host API specified by the `host_api_type`. The keys of the
        dictionary mirror the data fields of PortAudio's ``PaHostApiInfo``
        structure.

        :param host_api_type: The desired |PaHostAPI|
        :raises IOError: for invalid `host_api_type`
        :rtype: dict
        """
        ...
    def get_sample_size(self, format: int) -> int:
        """
        Returns the size (in bytes) for the specified sample `format`
        (a |PaSampleFormat| constant).

        :param format: A |PaSampleFormat| constant.
        :raises ValueError: Invalid specified `format`.
        :rtype: integer
        """
        ...
    def is_format_supported(
        self,
        rate: int,
        input_device: int | None = ...,
        input_channels: int | None = ...,
        input_format: int | None = ...,
        output_device: int | None = ...,
        output_channels: int | None = ...,
        output_format: int | None = ...,
    ) -> bool:
        """
        Checks if specified device configuration is supported.

        Returns True if the configuration is supported; raises ValueError
        otherwise.

        :param rate:
           Specifies the desired rate (in Hz)
        :param input_device:
           The input device index. Specify ``None`` (default) for
           half-duplex output-only streams.
        :param input_channels:
           The desired number of input channels. Ignored if
           `input_device` is not specified (or ``None``).
        :param input_format:
           PortAudio sample format constant defined
           in this module
        :param output_device:
           The output device index. Specify ``None`` (default) for
           half-duplex input-only streams.
        :param output_channels:
           The desired number of output channels. Ignored if
           `input_device` is not specified (or ``None``).
        :param output_format:
           |PaSampleFormat| constant.

        :rtype: bool
        :raises ValueError: tuple containing (error string, |PaErrorCode|).
        """
        ...
    def open(
        self,
        rate: int,
        channels: int,
        format: int,
        input: bool = ...,
        output: bool = ...,
        input_device_index: int | None = ...,
        output_device_index: int | None = ...,
        frames_per_buffer: int = ...,
        start: bool = ...,
        input_host_api_specific_stream_info: _PaMacCoreStreamInfo | None = ...,
        output_host_api_specific_stream_info: _PaMacCoreStreamInfo | None = ...,
        stream_callback: _StreamCallback | None = ...,
    ) -> _Stream:
        """
        Opens a new stream.

        See constructor for :py:func:`PyAudio.Stream.__init__` for parameter
        details.

        :returns: A new :py:class:`PyAudio.Stream`
        """
        ...
    def terminate(self) -> None:
        """
        Terminates PortAudio.

        :attention: Be sure to call this method for every instance of this
          object to release PortAudio resources.
        """
        ...
