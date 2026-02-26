from types import TracebackType

import ibm_db

class Db2connect:
    """Context manager to handle connections to DB2."""
    def __init__(self, dsn: str, username: str, password: str) -> None:
        """Instantiate a DB2 connection."""
        ...
    def __enter__(self) -> ibm_db.IBM_DBConnection:
        """Connect to DB2."""
        ...
    def __exit__(self, t: type[BaseException] | None, v: BaseException | None, tb: TracebackType | None) -> None:
        """Disconnect from DB2."""
        ...
