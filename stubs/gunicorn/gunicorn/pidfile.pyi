from _typeshed import StrOrBytesPath

class Pidfile:
    """
    Manage a PID file. If a specific name is provided
    it and '"%s.oldpid" % name' will be used. Otherwise
    we create a temp file using os.mkstemp.
    """
    fname: StrOrBytesPath
    pid: int | None

    def __init__(self, fname: StrOrBytesPath) -> None: ...
    def create(self, pid: int) -> None: ...
    def rename(self, path: StrOrBytesPath) -> None: ...
    def unlink(self) -> None:
        """delete pidfile"""
        ...
    def validate(self) -> None:
        """Validate pidfile and make it stale if needed"""
        ...
