from typing import Any, Final, final, overload
from typing_extensions import Self

__version__: Final[str]
ATTR_CASE: Final = 3271982
CASE_LOWER: Final = 1
CASE_NATURAL: Final = 0
CASE_UPPER: Final = 2
PARAM_FILE: Final = 11
QUOTED_LITERAL_REPLACEMENT_OFF: Final = 0
QUOTED_LITERAL_REPLACEMENT_ON: Final = 1
SQL_API_SQLROWCOUNT: Final[int]
SQL_ATTR_AUTOCOMMIT: Final[int]
SQL_ATTR_CALL_RETURN: Final[int]
SQL_ATTR_CURRENT_SCHEMA: Final[int]
SQL_ATTR_CURSOR_TYPE: Final[int]
SQL_ATTR_INFO_ACCTSTR: Final[int]
SQL_ATTR_INFO_APPLNAME: Final[int]
SQL_ATTR_INFO_PROGRAMNAME: Final[int]
SQL_ATTR_INFO_USERID: Final[int]
SQL_ATTR_INFO_WRKSTNNAME: Final[int]
SQL_ATTR_PARAMSET_SIZE: Final[int]
SQL_ATTR_PARAM_BIND_TYPE: Final[int]
SQL_ATTR_QUERY_TIMEOUT: Final[int]
SQL_ATTR_ROWCOUNT_PREFETCH: Final[int]
SQL_ATTR_TRUSTED_CONTEXT_PASSWORD: Final[int]
SQL_ATTR_TRUSTED_CONTEXT_USERID: Final[int]
SQL_ATTR_TXN_ISOLATION: Final[int]
SQL_ATTR_USE_TRUSTED_CONTEXT: Final[int]
SQL_ATTR_XML_DECLARATION: Final[int]
SQL_AUTOCOMMIT_OFF: Final[int]
SQL_AUTOCOMMIT_ON: Final[int]
SQL_BIGINT: Final[int]
SQL_BINARY: Final[int]
SQL_BIT: Final[int]
SQL_BLOB: Final[int]
SQL_BLOB_LOCATOR: Final[int]
SQL_BOOLEAN: Final[int]
SQL_CHAR: Final[int]
SQL_CLOB: Final[int]
SQL_CLOB_LOCATOR: Final[int]
SQL_CURSOR_DYNAMIC: Final[int]
SQL_CURSOR_FORWARD_ONLY: Final[int]
SQL_CURSOR_KEYSET_DRIVEN: Final[int]
SQL_CURSOR_STATIC: Final[int]
SQL_DBCLOB: Final[int]
SQL_DBCLOB_LOCATOR: Final[int]
SQL_DBMS_NAME: Final[int]
SQL_DBMS_VER: Final[int]
SQL_DECFLOAT: Final[int]
SQL_DECIMAL: Final[int]
SQL_DOUBLE: Final[int]
SQL_FALSE: Final[int]
SQL_FLOAT: Final[int]
SQL_GRAPHIC: Final[int]
SQL_INDEX_CLUSTERED: Final[int]
SQL_INDEX_OTHER: Final[int]
SQL_INTEGER: Final[int]
SQL_LONGVARBINARY: Final[int]
SQL_LONGVARCHAR: Final[int]
SQL_LONGVARGRAPHIC: Final[int]
SQL_NUMERIC: Final[int]
SQL_PARAM_BIND_BY_COLUMN: Final[int]
SQL_PARAM_INPUT: Final[int]
SQL_PARAM_INPUT_OUTPUT: Final[int]
SQL_PARAM_OUTPUT: Final[int]
SQL_REAL: Final[int]
SQL_ROWCOUNT_PREFETCH_OFF: Final[int]
SQL_ROWCOUNT_PREFETCH_ON: Final[int]
SQL_SMALLINT: Final[int]
SQL_TABLE_STAT: Final[int]
SQL_TINYINT: Final[int]
SQL_TRUE: Final[int]
SQL_TXN_NO_COMMIT: Final[int]
SQL_TXN_READ_COMMITTED: Final[int]
SQL_TXN_READ_UNCOMMITTED: Final[int]
SQL_TXN_REPEATABLE_READ: Final[int]
SQL_TXN_SERIALIZABLE: Final[int]
SQL_TYPE_DATE: Final[int]
SQL_TYPE_TIME: Final[int]
SQL_TYPE_TIMESTAMP: Final[int]
SQL_VARBINARY: Final[int]
SQL_VARCHAR: Final[int]
SQL_VARGRAPHIC: Final[int]
SQL_WCHAR: Final[int]
SQL_WLONGVARCHAR: Final[int]
SQL_WVARCHAR: Final[int]
SQL_XML: Final[int]
USE_WCHAR: Final = 100
WCHAR_NO: Final = 0
WCHAR_YES: Final = 1

SQL_ATTR_ACCESS_MODE: Final[int]
SQL_ATTR_ALLOW_INTERLEAVED_GETDATA: Final[int]
SQL_ATTR_ANSI_APP: Final[int]
SQL_ATTR_APPEND_FOR_FETCH_ONLY: Final[int]
SQL_ATTR_APP_USES_LOB_LOCATOR: Final[int]
SQL_ATTR_ASYNC_ENABLE: Final[int]
SQL_ATTR_AUTO_IPD: Final[int]
SQL_ATTR_CACHE_USRLIBL: Final[int]
SQL_ATTR_CLIENT_APPLCOMPAT: Final[int]
SQL_ATTR_CLIENT_CODEPAGE: Final[int]
SQL_ATTR_COLUMNWISE_MRI: Final[int]
SQL_ATTR_COMMITONEOF: Final[int]
SQL_ATTR_CONCURRENT_ACCESS_RESOLUTION: Final[int]
SQL_ATTR_CONFIG_KEYWORDS_ARRAY_SIZE: Final[int]
SQL_ATTR_CONFIG_KEYWORDS_MAXLEN: Final[int]
SQL_ATTR_CONNECTION_DEAD: Final[int]
SQL_ATTR_CONNECTTYPE: Final[int]
SQL_ATTR_CONNECT_NODE: Final[int]
SQL_ATTR_CONNECT_PASSIVE: Final[int]
SQL_ATTR_CONN_CONTEXT: Final[int]
SQL_ATTR_CURRENT_CATALOG: Final[int]
SQL_ATTR_CURRENT_IMPLICIT_XMLPARSE_OPTION: Final[int]
SQL_ATTR_CURRENT_PACKAGE_PATH: Final[int]
SQL_ATTR_CURRENT_PACKAGE_SET: Final[int]
SQL_ATTR_DATE_FMT: Final[int]
SQL_ATTR_DATE_SEP: Final[int]
SQL_ATTR_DB2EXPLAIN: Final[int]
SQL_ATTR_DB2_APPLICATION_HANDLE: Final[int]
SQL_ATTR_DB2_APPLICATION_ID: Final[int]
SQL_ATTR_DB2_SQLERRP: Final[int]
SQL_ATTR_DECFLOAT_ROUNDING_MODE: Final[int]
SQL_ATTR_DECIMAL_SEP: Final[int]
SQL_ATTR_DESCRIBE_CALL: Final[int]
SQL_ATTR_DESCRIBE_OUTPUT_LEVEL: Final[int]
SQL_ATTR_DETECT_READ_ONLY_TXN: Final[int]
SQL_ATTR_ENLIST_IN_DTC: Final[int]
SQL_ATTR_EXTENDED_INDICATORS: Final[int]
SQL_ATTR_FET_BUF_SIZE: Final[int]
SQL_ATTR_FORCE_ROLLBACK: Final[int]
SQL_ATTR_FREE_LOCATORS_ON_FETCH: Final[int]
SQL_ATTR_GET_LATEST_MEMBER: Final[int]
SQL_ATTR_GET_LATEST_MEMBER_NAME: Final[int]
SQL_ATTR_IGNORE_SERVER_LIST: Final[int]
SQL_ATTR_INFO_CRRTKN: Final[int]
SQL_ATTR_INFO_PROGRAMID: Final[int]
SQL_ATTR_KEEP_DYNAMIC: Final[int]
SQL_ATTR_LOB_CACHE_SIZE: Final[int]
SQL_ATTR_LOB_FILE_THRESHOLD: Final[int]
SQL_ATTR_LOGIN_TIMEOUT: Final[int]
SQL_ATTR_LONGDATA_COMPAT: Final[int]
SQL_ATTR_MAPCHAR: Final[int]
SQL_ATTR_MAXBLKEXT: Final[int]
SQL_ATTR_MAX_LOB_BLOCK_SIZE: Final[int]
SQL_ATTR_NETWORK_STATISTICS: Final[int]
SQL_ATTR_OVERRIDE_CHARACTER_CODEPAGE: Final[int]
SQL_ATTR_OVERRIDE_CODEPAGE: Final[int]
SQL_ATTR_OVERRIDE_PRIMARY_AFFINITY: Final[int]
SQL_ATTR_PARC_BATCH: Final[int]
SQL_ATTR_PING_DB: Final[int]
SQL_ATTR_PING_NTIMES: Final[int]
SQL_ATTR_PING_REQUEST_PACKET_SIZE: Final[int]
SQL_ATTR_QUERY_PREFETCH: Final[int]
SQL_ATTR_QUIET_MODE: Final[int]
SQL_ATTR_READ_ONLY_CONNECTION: Final[int]
SQL_ATTR_RECEIVE_TIMEOUT: Final[int]
SQL_ATTR_REOPT: Final[int]
SQL_ATTR_REPORT_ISLONG_FOR_LONGTYPES_OLEDB: Final[int]
SQL_ATTR_REPORT_SEAMLESSFAILOVER_WARNING: Final[int]
SQL_ATTR_REPORT_TIMESTAMP_TRUNC_AS_WARN: Final[int]
SQL_ATTR_RETRYONERROR: Final[int]
SQL_ATTR_RETRY_ON_MERGE: Final[int]
SQL_ATTR_SERVER_MSGTXT_MASK: Final[int]
SQL_ATTR_SERVER_MSGTXT_SP: Final[int]
SQL_ATTR_SESSION_GLOBAL_VAR: Final[int]
SQL_ATTR_SESSION_TIME_ZONE: Final[int]
SQL_ATTR_SPECIAL_REGISTER: Final[int]
SQL_ATTR_SQLCOLUMNS_SORT_BY_ORDINAL_OLEDB: Final[int]
SQL_ATTR_STMT_CONCENTRATOR: Final[int]
SQL_ATTR_STREAM_GETDATA: Final[int]
SQL_ATTR_STREAM_OUTPUTLOB_ON_CALL: Final[int]
SQL_ATTR_TIME_FMT: Final[int]
SQL_ATTR_TIME_SEP: Final[int]
SQL_ATTR_TRUSTED_CONTEXT_ACCESSTOKEN: Final[int]
SQL_ATTR_USER_REGISTRY_NAME: Final[int]
SQL_ATTR_WCHARTYPE: Final[int]

@final
class IBM_DBClientInfo:
    """IBM DataServer Client Information object"""
    def __new__(cls, *args: object, **kwargs: object) -> Self: ...
    APPL_CODEPAGE: int
    CONN_CODEPAGE: int
    DATA_SOURCE_NAME: str
    DRIVER_NAME: str
    DRIVER_ODBC_VER: str
    DRIVER_VER: str
    ODBC_SQL_CONFORMANCE: str
    ODBC_VER: str

@final
class IBM_DBConnection:
    """IBM DataServer connection object"""
    def __new__(cls, *args: object, **kwargs: object) -> Self: ...

@final
class IBM_DBServerInfo:
    """IBM DataServer Information object"""
    def __new__(cls, *args: object, **kwargs: object) -> Self: ...
    DBMS_NAME: str
    DBMS_VER: str
    DB_CODEPAGE: int
    DB_NAME: str
    DFT_ISOLATION: str
    IDENTIFIER_QUOTE_CHAR: str
    INST_NAME: str
    ISOLATION_OPTION: tuple[str, str, str, str, str]
    KEYWORDS: str
    LIKE_ESCAPE_CLAUSE: bool
    MAX_COL_NAME_LEN: int
    MAX_IDENTIFIER_LEN: int
    MAX_INDEX_SIZE: int
    MAX_PROC_NAME_LEN: int
    MAX_ROW_SIZE: int
    MAX_SCHEMA_NAME_LEN: int
    MAX_STATEMENT_LEN: int
    MAX_TABLE_NAME_LEN: int
    NON_NULLABLE_COLUMNS: bool
    PROCEDURES: bool
    SPECIAL_CHARS: str
    SQL_CONFORMANCE: str

@final
class IBM_DBStatement:
    """IBM DataServer cursor object"""
    def __new__(cls, *args: object, **kwargs: object) -> Self: ...

def active(connection: IBM_DBConnection | None, /) -> bool:
    """Checks if the specified connection resource is active"""
    ...
def autocommit(connection: IBM_DBConnection, value: int = ..., /) -> int | bool:
    """Returns or sets the AUTOCOMMIT state for a database connection"""
    ...
def bind_param(
    stmt: IBM_DBStatement,
    parameter_number: int,
    variable: str,
    parameter_type: int | None = ...,
    data_type: int | None = ...,
    precision: int | None = ...,
    scale: int | None = ...,
    size: int | None = ...,
    /,
) -> bool:
    """Binds a Python variable to an SQL statement parameter"""
    ...
@overload
def callproc(connection: IBM_DBConnection, procname: str, /) -> IBM_DBStatement | None:
    """Returns a tuple containing OUT/INOUT variable value"""
    ...
@overload
def callproc(connection: IBM_DBConnection, procname: str, parameters: tuple[object, ...], /) -> tuple[object, ...] | None:
    """Returns a tuple containing OUT/INOUT variable value"""
    ...
def check_function_support(connection: IBM_DBConnection, function_id: int, /) -> bool:
    """return true if fuction is supported otherwise return false"""
    ...
def client_info(connection: IBM_DBConnection, /) -> IBM_DBClientInfo | bool:
    """Returns a read-only object with information about the DB2 database client"""
    ...
def close(connection: IBM_DBConnection, /) -> bool:
    """Close a database connection"""
    ...
def column_privileges(
    connection: IBM_DBConnection,
    qualifier: str | None = ...,
    schema: str | None = ...,
    table_name: str | None = ...,
    column_name: str | None = ...,
    /,
) -> IBM_DBStatement:
    """Returns a result set listing the columns and associated privileges for a table."""
    ...
def columns(
    connection: IBM_DBConnection,
    qualifier: str | None = ...,
    schema: str | None = ...,
    table_name: str | None = ...,
    column_name: str | None = ...,
    /,
) -> IBM_DBStatement:
    """Returns a result set listing the columns and associated metadata for a table"""
    ...
def commit(connection: IBM_DBConnection, /) -> bool:
    """Commits a transaction"""
    ...
def conn_error(connection: IBM_DBConnection | None = ..., /) -> str:
    """Returns a string containing the SQLSTATE returned by the last connection attempt"""
    ...
def conn_errormsg(connection: IBM_DBConnection | None = ..., /) -> str:
    """Returns an error message and SQLCODE value representing the reason the last database connection attempt failed"""
    ...
def conn_warn(connection: IBM_DBConnection | None = ..., /) -> str:
    """Returns a warning string containing the SQLSTATE returned by the last connection attempt"""
    ...
def connect(
    database: str, user: str, password: str, options: dict[int, int | str] | None = ..., replace_quoted_literal: int = ..., /
) -> IBM_DBConnection | None:
    """Connect to the database"""
    ...
def createdb(connection: IBM_DBConnection, dbName: str, codeSet: str = ..., mode: str = ..., /) -> bool:
    """Create db"""
    ...
def createdbNX(connection: IBM_DBConnection, dbName: str, codeSet: str = ..., mode: str = ..., /) -> bool:
    """createdbNX"""
    ...
def cursor_type(stmt: IBM_DBStatement, /) -> int:
    """Returns the cursor type used by a statement resource"""
    ...
def debug(option: str | bool) -> None:
    """Enable logging with optional log file or disable logging"""
    ...
def dropdb(connection: IBM_DBConnection, dbName: str, /) -> bool:
    """Drop db"""
    ...
def exec_immediate(
    connection: IBM_DBConnection, statement: str | None, options: dict[int, int] = ..., /
) -> IBM_DBStatement | bool:
    """Prepares and executes an SQL statement."""
    ...
def execute(stmt: IBM_DBStatement, parameters: tuple[object, ...] | None = ..., /) -> bool:
    """Executes an SQL statement that was prepared by ibm_db.prepare()"""
    ...
def execute_many(
    stmt: IBM_DBStatement, seq_of_parameters: tuple[object, ...], options: dict[int, int] = ..., /
) -> int | None:
    """Execute SQL with multiple rows."""
    ...
def fetchall(stmt: IBM_DBStatement, /) -> list[tuple[object, ...]]:
    """Fetch all rows from the result set."""
    ...
def fetchmany(stmt: IBM_DBStatement, numberOfRows: int, /) -> list[tuple[object, ...]]:
    """Fetch a specified number of rows from the result set."""
    ...
def fetchone(stmt: IBM_DBStatement, /) -> tuple[object, ...]:
    """Fetch a single row from the result set."""
    ...
def fetch_assoc(stmt: IBM_DBStatement, row_number: int = ..., /) -> dict[str, object] | bool:
    """Returns a dictionary, indexed by column name, representing a row in a result set"""
    ...
def fetch_both(stmt: IBM_DBStatement, row_number: int = ..., /) -> dict[int | str, object] | bool:
    """Returns a dictionary, indexed by both column name and position, representing a row in a result set"""
    ...
def fetch_row(stmt: IBM_DBStatement, row_number: int = ..., /) -> bool:
    """Sets the result set pointer to the next row or requested row"""
    ...
def fetch_tuple(stmt: IBM_DBStatement, row_number: int = ..., /) -> tuple[object, ...]:
    """Returns an tuple, indexed by column position, representing a row in a result set"""
    ...
def field_display_size(stmt: IBM_DBStatement, column: int | str, /) -> int | bool:
    """Returns the maximum number of bytes required to display a column"""
    ...
def field_name(stmt: IBM_DBStatement, column: int | str, /) -> str | bool:
    """Returns the name of the column in the result set"""
    ...
def field_nullable(stmt: IBM_DBStatement, column: int | str, /) -> bool:
    """Returns indicated column can contain nulls or not"""
    ...
def field_num(stmt: IBM_DBStatement, column: int | str, /) -> int | bool:
    """Returns the position of the named column in a result set"""
    ...
def field_precision(stmt: IBM_DBStatement, column: int | str, /) -> int | bool:
    """Returns the precision of the indicated column in a result set"""
    ...
def field_scale(stmt: IBM_DBStatement, column: int | str, /) -> int | bool:
    """Returns the scale of the indicated column in a result set"""
    ...
def field_type(stmt: IBM_DBStatement, column: int | str, /) -> str | bool:
    """Returns the data type of the indicated column in a result set"""
    ...
def field_width(stmt: IBM_DBStatement, column: int | str, /) -> int | bool:
    """Returns the width of the indicated column in a result set"""
    ...
def foreign_keys(
    connection: IBM_DBConnection,
    pk_qualifier: str | None,
    pk_schema: str | None,
    pk_table_name: str | None,
    fk_qualifier: str | None = ...,
    fk_schema: str | None = ...,
    fk_table_name: str | None = ...,
    /,
) -> IBM_DBStatement:
    """Returns a result set listing the foreign keys for a table"""
    ...
def free_result(stmt: IBM_DBStatement, /) -> bool:
    """Frees resources associated with a result set"""
    ...
def free_stmt(stmt: IBM_DBStatement, /) -> bool:
    """Frees resources associated with the indicated statement resource"""
    ...
def get_db_info(connection: IBM_DBConnection, option: int, /) -> str | bool:
    """Returns an object with properties that describe the DB2 database server according to the option passed"""
    ...
def get_last_serial_value(stmt: IBM_DBStatement, /) -> str | bool:
    """Returns last serial value inserted for identity column"""
    ...
def get_num_result(stmt: IBM_DBStatement, /) -> int | bool:
    """Returns the number of rows in a current open non-dynamic scrollable cursor"""
    ...
def get_option(resc: IBM_DBConnection | IBM_DBStatement, options: int, type: int, /) -> Any:
    """Gets the specified option in the resource."""
    ...
def get_sqlcode(connection_or_stmt: IBM_DBConnection | IBM_DBStatement | None = None, /) -> str:
    """Returns a string containing the SQLCODE returned by the last connection attempt/ SQL statement"""
    ...
def next_result(stmt: IBM_DBStatement, /) -> IBM_DBStatement | bool:
    """Requests the next result set from a stored procedure"""
    ...
def num_fields(stmt: IBM_DBStatement, /) -> int | bool:
    """Returns the number of fields contained in a result set"""
    ...
def num_rows(stmt: IBM_DBStatement, /) -> int:
    """Returns the number of rows affected by an SQL statement"""
    ...
def pconnect(
    database: str, username: str, password: str, options: dict[int, int | str] | None = ..., /
) -> IBM_DBConnection | None:
    """Returns a persistent connection to a database"""
    ...
def prepare(
    connection: IBM_DBConnection, statement: str, options: dict[int, int | str] | None = ..., /
) -> IBM_DBStatement | bool:
    """Prepares an SQL statement."""
    ...
def primary_keys(
    connection: IBM_DBConnection, qualifier: str | None, schema: str | None, table_name: str | None, /
) -> IBM_DBStatement:
    """Returns a result set listing primary keys for a table"""
    ...
def procedure_columns(
    connection: IBM_DBConnection, qualifier: str | None, schema: str | None, procedure: str | None, parameter: str | None, /
) -> IBM_DBStatement | bool:
    """Returns a result set listing the parameters for one or more stored procedures."""
    ...
def procedures(
    connection: IBM_DBConnection, qualifier: str | None, schema: str | None, procedure: str | None, /
) -> IBM_DBStatement | bool:
    """Returns a result set listing the stored procedures registered in a database"""
    ...
def recreatedb(connection: IBM_DBConnection, dbName: str, codeSet: str | None = ..., mode: str | None = ..., /) -> bool:
    """recreate db"""
    ...
def result(stmt: IBM_DBStatement, column: int | str, /) -> Any:
    """Returns a single column from a row in the result set"""
    ...
def rollback(connection: IBM_DBConnection, /) -> bool:
    """Rolls back a transaction"""
    ...
def server_info(connection: IBM_DBConnection, /) -> IBM_DBServerInfo | bool:
    """Returns an object with properties that describe the DB2 database server"""
    ...
def set_option(resc: IBM_DBConnection | IBM_DBStatement, options: dict[int, int | str], type: int, /) -> bool:
    """Sets the specified option in the resource"""
    ...
def special_columns(
    connection: IBM_DBConnection, qualifier: str | None, schema: str | None, table_name: str | None, scope: int, /
) -> IBM_DBStatement:
    """Returns a result set listing the unique row identifier columns for a table"""
    ...
def statistics(
    connection: IBM_DBConnection, qualifier: str | None, schema: str | None, table_name: str | None, unique: bool | None, /
) -> IBM_DBStatement:
    """Returns a result set listing the index and statistics for a table"""
    ...
def stmt_error(stmt: IBM_DBStatement = ..., /) -> str:
    """Returns a string containing the SQLSTATE returned by an SQL statement"""
    ...
def stmt_errormsg(stmt: IBM_DBStatement = ..., /) -> str:
    """Returns a string containing the last SQL statement error message"""
    ...
def stmt_warn(connection: IBM_DBConnection = ..., /) -> IBM_DBStatement:
    """Returns a warning string containing the SQLSTATE returned by last SQL statement"""
    ...
def table_privileges(
    connection: IBM_DBConnection, qualifier: str | None = ..., schema: str | None = ..., table_name: str | None = ..., /
) -> IBM_DBStatement | bool:
    """Returns a result set listing the tables and associated privileges in a database"""
    ...
def tables(
    connection: IBM_DBConnection,
    qualifier: str | None = ...,
    schema: str | None = ...,
    table_name: str | None = ...,
    table_type: str | None = ...,
    /,
) -> IBM_DBStatement | bool:
    """Returns a result set listing the tables and associated metadata in a database"""
    ...
