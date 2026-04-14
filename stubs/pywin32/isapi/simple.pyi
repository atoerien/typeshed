"""
Simple base-classes for extensions and filters.

None of the filter and extension functions are considered 'optional' by the
framework.  These base-classes provide simple implementations for the
Initialize and Terminate functions, allowing you to omit them,

It is not necessary to use these base-classes - but if you don't, you
must ensure each of the required methods are implemented.
"""

class SimpleExtension:
    """Base class for a simple ISAPI extension"""
    def GetExtensionVersion(self, vi) -> None:
        """
        Called by the ISAPI framework to get the extension version

        The default implementation uses the classes docstring to
        set the extension description.
        """
        ...
    def HttpExtensionProc(self, control_block) -> int | None:
        """
        Called by the ISAPI framework for each extension request.

        sub-classes must provide an implementation for this method.
        """
        ...
    def TerminateExtension(self, status) -> None:
        """Called by the ISAPI framework as the extension terminates."""
        ...

class SimpleFilter:
    """Base class for a a simple ISAPI filter"""
    filter_flags: int | None
    def GetFilterVersion(self, fv) -> None:
        """
        Called by the ISAPI framework to get the extension version

        The default implementation uses the classes docstring to
        set the extension description, and uses the classes
        filter_flags attribute to set the ISAPI filter flags - you
        must specify filter_flags in your class.
        """
        ...
    def HttpFilterProc(self, fc) -> None:
        """
        Called by the ISAPI framework for each filter request.

        sub-classes must provide an implementation for this method.
        """
        ...
    def TerminateFilter(self, status) -> None:
        """Called by the ISAPI framework as the filter terminates."""
        ...
