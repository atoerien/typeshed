from _typeshed import Unused
from collections.abc import Callable, Sequence
from io import IOBase
from typing import Final, Literal, TypeAlias, TypedDict, TypeVar, final, overload, type_check_only
from typing_extensions import NotRequired

_T = TypeVar("_T")

_FileOrFd: TypeAlias = IOBase | int

_CupsDevice = TypedDict(
    "_CupsDevice",
    {"device-class": str, "device-info": str, "device-make-and-model": str, "device-id": str, "device-location": str},
)

_CupsDocument = TypedDict("_CupsDocument", {"file": str, "document-format": NotRequired[str], "document-name": NotRequired[str]})

_CupsPPD = TypedDict(
    "_CupsPPD",
    {
        "ppd-natural-language": str,
        "ppd-make": str,
        "ppd-make-and-model": str,
        "ppd-device-id": str,
        "ppd-product": str,
        "ppd-psversion": str,
        "ppd-type": str,
        "ppd-model-number": int,
    },
)

_CupsPPD2 = TypedDict(
    "_CupsPPD2",
    {
        "ppd-natural-language": list[str],
        "ppd-make": list[str],
        "ppd-make-and-model": list[str],
        "ppd-device-id": list[str],
        "ppd-product": list[str],
        "ppd-psversion": list[str],
        "ppd-type": list[str],
        "ppd-model-number": list[int],
    },
)

_CupsJob = TypedDict(
    "_CupsJob",
    {
        "number-of-documents": int,
        "job-media-progress": int,
        "job-more-info": str,
        "job-preserved": bool,
        "job-printer-up-time": int,
        "job-printer-uri": str,
        "job-uri": str,
        "printer-uri": str,
        "document-format-detected": str,
        "document-format": str,
        "job-priority": int,
        "job-uuid": str,
        "date-time-at-completed": str,
        "date-time-at-creation": str,
        "date-time-at-processing": str,
        "time-at-completed": int,
        "time-at-creation": int,
        "time-at-processing": int,
        "job-state": int,
        "job-state-reasons": str,
        "job-impressions-completed": int,
        "job-media-sheets-completed": int,
        "job-k-octets": int,
        "job-hold-until": str,
        "job-sheets": list[str],
        "job-printer-state-message": str,
        "job-printer-state-reasons": str,
        "job-name": str,
        "job-originating-user-name": str,
    },
)

_CupsAttributeInfo = TypedDict(
    "_CupsAttributeInfo", {"attributes-charset": str, "attributes-natural-language": str, "job-id": int}
)

@type_check_only
class _CupsOptionChoice(TypedDict):
    choice: str
    text: str
    marked: bool

@type_check_only
class _CupsJobWithAttributeInfo(_CupsJob, _CupsAttributeInfo): ...

_CupsEvent = TypedDict(  # noqa: Y049
    "_CupsEvent",
    {
        "notify-charset": str,
        "notify-natural-language": str,
        "notify-subscription-id": int,
        "notify-sequence-number": int,
        "notify-subscribed-event": str,
        "printer-up-time": int,
        "notify-text": str,
        "notify-printer-uri": str,
        "printer-name": str,
        "printer-state": int,
        "printer-state-reasons": list[str],
        "printer-is-accepting-jobs": bool,
        "notify-job-id": int,
        "job-state": int,
        "job-name": str,
        "job-state-reasons": str,
        "job-impressions-completed": int,
    },
)

_CupsNotifications = TypedDict(
    "_CupsNotifications", {"notify-get-interval": int, "printer-up-time": int, "events": list[_CupsEvent]}
)

_CupsPrinter = TypedDict(
    "_CupsPrinter",
    {
        "marker-change-time": int,
        "printer-config-change-date-time": str,
        "printer-config-change-time": int,
        "printer-current-time": str,
        "printer-dns-sd-name": str | None,
        "printer-error-policy": str,
        "printer-error-policy-supported": list[str],
        "printer-icons": str,
        "printer-is-accepting-jobs": bool,
        "printer-is-shared": bool,
        "printer-is-temporary": bool,
        "printer-more-info": str,
        "printer-op-policy": str,
        "printer-state": int,
        "printer-state-change-date-time": str,
        "printer-state-change-time": int,
        "printer-state-message": str,
        "printer-state-reasons": list[str],
        "printer-strings-uri": str,
        "printer-type": int,
        "printer-up-time": int,
        "printer-uri-supported": list[str],
        "queued-job-count": int,
        "uri-security-supported": list[str],
        "uri-authentication-supported": list[str],
        "printer-id": int,
        "printer-name": str,
        "printer-location": str,
        "printer-geo-location": str,
        "printer-info": str,
        "printer-organization": str,
        "printer-organizational-unit": str,
        "printer-uuid": str,
        "job-quota-period": int,
        "job-k-limit": int,
        "job-page-limit": int,
        "job-sheets-default": tuple[str, str],
        "device-uri": str,
        "document-format-supported": list[str],
        "copies-default": int,
        "document-format-default": str,
        "job-cancel-after-default": int,
        "job-hold-until-default": str,
        "job-priority-default": int,
        "number-up-default": int,
        "notify-lease-duration-default": int,
        "notify-events-default": list[str],
        "orientation-requested-default": int | None,
        "print-color-mode-default": str,
        "print-quality-default": int,
        "copies-supported": tuple[int, int],
        "ipp-features-supported": list[str],
        "job-creation-attributes-supported": list[str],
        "printer-make-and-model": str,
        "finishings-supported": list[int],
        "finishings-default": int,
        "charset-configured": str,
        "charset-supported": list[str],
        "compression-supported": list[str],
        "cups-version": str,
        "generated-natural-language-supported": list[str],
        "ipp-versions-supported": list[str],
        "ippget-event-life": int,
        "job-cancel-after-supported": tuple[int, int],
        "job-hold-until-supported": list[str],
        "job-ids-supported": bool,
        "job-k-octets-supported": tuple[int, int],
        "job-priority-supported": list[int],
        "job-settable-attributes-supported": list[str],
        "job-sheets-supported": list[str],
        "jpeg-k-octets-supported": tuple[int, int],
        "jpeg-x-dimension-supported": tuple[int, int],
        "jpeg-y-dimension-supported": tuple[int, int],
        "media-col-supported": list[str],
        "multiple-document-handling-supported": list[str],
        "multiple-document-jobs-supported": bool,
        "multiple-operation-time-out": int,
        "multiple-operation-time-out-action": str,
        "natural-language-configured": str,
        "notify-attributes-supported": list[str],
        "notify-lease-duration-supported": tuple[int, int],
        "notify-max-events-supported": list[int],
        "notify-events-supported": list[str],
        "notify-pull-method-supported": list[str],
        "notify-schemes-supported": list[str],
        "number-up-supported": list[int],
        "number-up-layout-supported": list[str],
        "operations-supported": list[int],
        "orientation-requested-supported": list[int],
        "page-delivery-supported": list[str],
        "page-ranges-supported": bool,
        "pdf-k-octets-supported": tuple[int, int],
        "pdf-versions-supported": list[str],
        "pdl-override-supported": list[str],
        "print-scaling-supported": list[str],
        "printer-get-attributes-supported": list[str],
        "printer-op-policy-supported": list[str],
        "printer-settable-attributes-supported": list[str],
        "server-is-sharing-printers": bool,
        "which-jobs-supported": list[str],
    },
)

_CupsPrinterSimple = TypedDict(
    "_CupsPrinterSimple",
    {
        "printer-is-shared": bool,
        "printer-state": int,
        "printer-state-message": str,
        "printer-state-reasons": list[str],
        "printer-type": int,
        "printer-uri-supported": str,
        "printer-location": str,
        "printer-info": str,
        "device-uri": str,
        "printer-make-and-model": str,
    },
)

_CupsSubscription = TypedDict(
    "_CupsSubscription",
    {
        "notify-events": list[str],
        "notify-lease-duration": int,
        "notify-pull-method": NotRequired[str],
        "notify-recipient-uri": NotRequired[str],
        "notify-subscriber-user-name": str,
        "notify-time-interval": int,
        "notify-subscription-id": int,
    },
)

CUPS_DEST_FLAGS_CANCELED: Final[int]
CUPS_DEST_FLAGS_CONNECTING: Final[int]
CUPS_DEST_FLAGS_ERROR: Final[int]
CUPS_DEST_FLAGS_MORE: Final[int]
CUPS_DEST_FLAGS_NONE: Final[int]
CUPS_DEST_FLAGS_REMOVED: Final[int]
CUPS_DEST_FLAGS_RESOLVING: Final[int]
CUPS_DEST_FLAGS_UNCONNECTED: Final[int]
CUPS_FORMAT_AUTO: Final[str]
CUPS_FORMAT_COMMAND: Final[str]
CUPS_FORMAT_PDF: Final[str]
CUPS_FORMAT_POSTSCRIPT: Final[str]
CUPS_FORMAT_RAW: Final[str]
CUPS_FORMAT_TEXT: Final[str]
CUPS_PRINTER_AUTHENTICATED: Final[int]
CUPS_PRINTER_BIND: Final[int]
CUPS_PRINTER_BW: Final[int]
CUPS_PRINTER_CLASS: Final[int]
CUPS_PRINTER_COLLATE: Final[int]
CUPS_PRINTER_COLOR: Final[int]
CUPS_PRINTER_COMMANDS: Final[int]
CUPS_PRINTER_COPIES: Final[int]
CUPS_PRINTER_COVER: Final[int]
CUPS_PRINTER_DEFAULT: Final[int]
CUPS_PRINTER_DELETE: Final[int]
CUPS_PRINTER_DISCOVERED: Final[int]
CUPS_PRINTER_DUPLEX: Final[int]
CUPS_PRINTER_FAX: Final[int]
CUPS_PRINTER_IMPLICIT: Final[int]
CUPS_PRINTER_LARGE: Final[int]
CUPS_PRINTER_LOCAL: Final[int]
CUPS_PRINTER_MEDIUM: Final[int]
CUPS_PRINTER_NOT_SHARED: Final[int]
CUPS_PRINTER_OPTIONS: Final[int]
CUPS_PRINTER_PUNCH: Final[int]
CUPS_PRINTER_REJECTING: Final[int]
CUPS_PRINTER_REMOTE: Final[int]
CUPS_PRINTER_SMALL: Final[int]
CUPS_PRINTER_SORT: Final[int]
CUPS_PRINTER_STAPLE: Final[int]
CUPS_PRINTER_VARIABLE: Final[int]
CUPS_SERVER_DEBUG_LOGGING: Final[str]
CUPS_SERVER_REMOTE_ADMIN: Final[str]
CUPS_SERVER_REMOTE_ANY: Final[str]
CUPS_SERVER_REMOTE_PRINTERS: Final[str]
CUPS_SERVER_SHARE_PRINTERS: Final[str]
CUPS_SERVER_USER_CANCEL_ANY: Final[str]
HTTP_AUTHORIZATION_CANCELED: Final[int]
HTTP_BAD_GATEWAY: Final[int]
HTTP_BAD_REQUEST: Final[int]
HTTP_ENCRYPT_ALWAYS: Final[int]
HTTP_ENCRYPT_IF_REQUESTED: Final[int]
HTTP_ENCRYPT_NEVER: Final[int]
HTTP_ENCRYPT_REQUIRED: Final[int]
HTTP_ERROR: Final[int]
HTTP_FORBIDDEN: Final[int]
HTTP_GATEWAY_TIMEOUT: Final[int]
HTTP_NOT_FOUND: Final[int]
HTTP_NOT_IMPLEMENTED: Final[int]
HTTP_NOT_MODIFIED: Final[int]
HTTP_NOT_SUPPORTED: Final[int]
HTTP_OK: Final[int]
HTTP_PKI_ERROR: Final[int]
HTTP_REQUEST_TIMEOUT: Final[int]
HTTP_SERVER_ERROR: Final[int]
HTTP_SERVICE_UNAVAILABLE: Final[int]
HTTP_STATUS_BAD_GATEWAY: Final[int]
HTTP_STATUS_BAD_REQUEST: Final[int]
HTTP_STATUS_CUPS_AUTHORIZATION_CANCELED: Final[int]
HTTP_STATUS_CUPS_PKI_ERROR: Final[int]
HTTP_STATUS_ERROR: Final[int]
HTTP_STATUS_FORBIDDEN: Final[int]
HTTP_STATUS_GATEWAY_TIMEOUT: Final[int]
HTTP_STATUS_NOT_FOUND: Final[int]
HTTP_STATUS_NOT_IMPLEMENTED: Final[int]
HTTP_STATUS_NOT_MODIFIED: Final[int]
HTTP_STATUS_NOT_SUPPORTED: Final[int]
HTTP_STATUS_OK: Final[int]
HTTP_STATUS_REQUEST_TIMEOUT: Final[int]
HTTP_STATUS_SERVER_ERROR: Final[int]
HTTP_STATUS_SERVICE_UNAVAILABLE: Final[int]
HTTP_STATUS_UNAUTHORIZED: Final[int]
HTTP_STATUS_UPGRADE_REQUIRED: Final[int]
HTTP_UNAUTHORIZED: Final[int]
HTTP_UPGRADE_REQUIRED: Final[int]
IPP_ATTRIBUTE: Final[int]
IPP_ATTRIBUTES: Final[int]
IPP_ATTRIBUTES_NOT_SETTABLE: Final[int]
IPP_AUTHENTICATION_CANCELED: Final[int]
IPP_BAD_REQUEST: Final[int]
IPP_CHARSET: Final[int]
IPP_COMPRESSION_ERROR: Final[int]
IPP_COMPRESSION_NOT_SUPPORTED: Final[int]
IPP_CONFLICT: Final[int]
IPP_CREATE_JOB_SUBSCRIPTION: Final[int]
IPP_CREATE_PRINTER_SUBSCRIPTION: Final[int]
IPP_DATA: Final[int]
IPP_DEVICE_ERROR: Final[int]
IPP_DOCUMENT_ACCESS_ERROR: Final[int]
IPP_DOCUMENT_FORMAT: Final[int]
IPP_DOCUMENT_FORMAT_ERROR: Final[int]
IPP_ERROR: Final[int]
IPP_ERROR_JOB_CANCELED: Final[int]
IPP_FINISHINGS_BALE: Final[int]
IPP_FINISHINGS_BIND: Final[int]
IPP_FINISHINGS_BIND_BOTTOM: Final[int]
IPP_FINISHINGS_BIND_LEFT: Final[int]
IPP_FINISHINGS_BIND_RIGHT: Final[int]
IPP_FINISHINGS_BIND_TOP: Final[int]
IPP_FINISHINGS_BOOKLET_MAKER: Final[int]
IPP_FINISHINGS_COVER: Final[int]
IPP_FINISHINGS_EDGE_STITCH: Final[int]
IPP_FINISHINGS_EDGE_STITCH_BOTTOM: Final[int]
IPP_FINISHINGS_EDGE_STITCH_LEFT: Final[int]
IPP_FINISHINGS_EDGE_STITCH_RIGHT: Final[int]
IPP_FINISHINGS_EDGE_STITCH_TOP: Final[int]
IPP_FINISHINGS_FOLD: Final[int]
IPP_FINISHINGS_JOB_OFFSET: Final[int]
IPP_FINISHINGS_NONE: Final[int]
IPP_FINISHINGS_PUNCH: Final[int]
IPP_FINISHINGS_SADDLE_STITCH: Final[int]
IPP_FINISHINGS_STAPLE: Final[int]
IPP_FINISHINGS_STAPLE_BOTTOM_LEFT: Final[int]
IPP_FINISHINGS_STAPLE_BOTTOM_RIGHT: Final[int]
IPP_FINISHINGS_STAPLE_DUAL_BOTTOM: Final[int]
IPP_FINISHINGS_STAPLE_DUAL_LEFT: Final[int]
IPP_FINISHINGS_STAPLE_DUAL_RIGHT: Final[int]
IPP_FINISHINGS_STAPLE_DUAL_TOP: Final[int]
IPP_FINISHINGS_STAPLE_TOP_LEFT: Final[int]
IPP_FINISHINGS_STAPLE_TOP_RIGHT: Final[int]
IPP_FINISHINGS_TRIM: Final[int]
IPP_FORBIDDEN: Final[int]
IPP_GONE: Final[int]
IPP_HEADER: Final[int]
IPP_IDLE: Final[int]
IPP_IGNORED_ALL_NOTIFICATIONS: Final[int]
IPP_IGNORED_ALL_SUBSCRIPTIONS: Final[int]
IPP_INTERNAL_ERROR: Final[int]
IPP_JOB_ABORTED: Final[int]
IPP_JOB_CANCELED: Final[int]
IPP_JOB_COMPLETED: Final[int]
IPP_JOB_HELD: Final[int]
IPP_JOB_PENDING: Final[int]
IPP_JOB_PROCESSING: Final[int]
IPP_JOB_STOPPED: Final[int]
IPP_LANDSCAPE: Final[int]
IPP_MAX_NAME: Final[int]
IPP_MULTIPLE_JOBS_NOT_SUPPORTED: Final[int]
IPP_NOT_ACCEPTING: Final[int]
IPP_NOT_AUTHENTICATED: Final[int]
IPP_NOT_AUTHORIZED: Final[int]
IPP_NOT_FOUND: Final[int]
IPP_NOT_POSSIBLE: Final[int]
IPP_OK: Final[int]
IPP_OK_BUT_CANCEL_SUBSCRIPTION: Final[int]
IPP_OK_CONFLICT: Final[int]
IPP_OK_EVENTS_COMPLETE: Final[int]
IPP_OK_IGNORED_NOTIFICATIONS: Final[int]
IPP_OK_IGNORED_SUBSCRIPTIONS: Final[int]
IPP_OK_SUBST: Final[int]
IPP_OK_TOO_MANY_EVENTS: Final[int]
IPP_OPERATION_NOT_SUPPORTED: Final[int]
IPP_OP_ACTIVATE_PRINTER: Final[int]
IPP_OP_CANCEL_CURRENT_JOB: Final[int]
IPP_OP_CANCEL_JOB: Final[int]
IPP_OP_CANCEL_JOBS: Final[int]
IPP_OP_CANCEL_MY_JOBS: Final[int]
IPP_OP_CANCEL_SUBSCRIPTION: Final[int]
IPP_OP_CLOSE_JOB: Final[int]
IPP_OP_CREATE_JOB: Final[int]
IPP_OP_CREATE_JOB_SUBSCRIPTIONS: Final[int]
IPP_OP_CREATE_PRINTER_SUBSCRIPTIONS: Final[int]
IPP_OP_CUPS_ACCEPT_JOBS: Final[int]
IPP_OP_CUPS_ADD_MODIFY_CLASS: Final[int]
IPP_OP_CUPS_ADD_MODIFY_PRINTER: Final[int]
IPP_OP_CUPS_AUTHENTICATE_JOB: Final[int]
IPP_OP_CUPS_DELETE_CLASS: Final[int]
IPP_OP_CUPS_DELETE_PRINTER: Final[int]
IPP_OP_CUPS_GET_CLASSES: Final[int]
IPP_OP_CUPS_GET_DEFAULT: Final[int]
IPP_OP_CUPS_GET_DOCUMENT: Final[int]
IPP_OP_CUPS_GET_PPD: Final[int]
IPP_OP_CUPS_GET_PPDS: Final[int]
IPP_OP_CUPS_GET_PRINTERS: Final[int]
IPP_OP_CUPS_MOVE_JOB: Final[int]
IPP_OP_CUPS_REJECT_JOBS: Final[int]
IPP_OP_CUPS_SET_DEFAULT: Final[int]
IPP_OP_DEACTIVATE_PRINTER: Final[int]
IPP_OP_DISABLE_PRINTER: Final[int]
IPP_OP_ENABLE_PRINTER: Final[int]
IPP_OP_GET_JOBS: Final[int]
IPP_OP_GET_JOB_ATTRIBUTES: Final[int]
IPP_OP_GET_NOTIFICATIONS: Final[int]
IPP_OP_GET_PRINTER_ATTRIBUTES: Final[int]
IPP_OP_GET_PRINTER_SUPPORTED_VALUES: Final[int]
IPP_OP_GET_PRINT_SUPPORT_FILES: Final[int]
IPP_OP_GET_RESOURCES: Final[int]
IPP_OP_GET_RESOURCE_ATTRIBUTES: Final[int]
IPP_OP_GET_RESOURCE_DATA: Final[int]
IPP_OP_GET_SUBSCRIPTIONS: Final[int]
IPP_OP_HOLD_JOB: Final[int]
IPP_OP_HOLD_NEW_JOBS: Final[int]
IPP_OP_IDENTIFY_PRINTER: Final[int]
IPP_OP_PAUSE_PRINTER: Final[int]
IPP_OP_PAUSE_PRINTER_AFTER_CURRENT_JOB: Final[int]
IPP_OP_PRINT_JOB: Final[int]
IPP_OP_PRINT_URI: Final[int]
IPP_OP_PROMOTE_JOB: Final[int]
IPP_OP_PURGE_JOBS: Final[int]
IPP_OP_RELEASE_HELD_NEW_JOBS: Final[int]
IPP_OP_RELEASE_JOB: Final[int]
IPP_OP_RENEW_SUBSCRIPTION: Final[int]
IPP_OP_REPROCESS_JOB: Final[int]
IPP_OP_RESTART_JOB: Final[int]
IPP_OP_RESTART_PRINTER: Final[int]
IPP_OP_RESUBMIT_JOB: Final[int]
IPP_OP_RESUME_JOB: Final[int]
IPP_OP_RESUME_PRINTER: Final[int]
IPP_OP_SCHEDULE_JOB_AFTER: Final[int]
IPP_OP_SEND_DOCUMENT: Final[int]
IPP_OP_SEND_HARDCOPY_DOCUMENT: Final[int]
IPP_OP_SEND_NOTIFICATIONS: Final[int]
IPP_OP_SEND_URI: Final[int]
IPP_OP_SET_JOB_ATTRIBUTES: Final[int]
IPP_OP_SET_PRINTER_ATTRIBUTES: Final[int]
IPP_OP_SHUTDOWN_PRINTER: Final[int]
IPP_OP_STARTUP_PRINTER: Final[int]
IPP_OP_SUSPEND_CURRENT_JOB: Final[int]
IPP_OP_VALIDATE_DOCUMENT: Final[int]
IPP_OP_VALIDATE_JOB: Final[int]
IPP_ORIENT_LANDSCAPE: Final[int]
IPP_ORIENT_PORTRAIT: Final[int]
IPP_ORIENT_REVERSE_LANDSCAPE: Final[int]
IPP_ORIENT_REVERSE_PORTRAIT: Final[int]
IPP_PKI_ERROR: Final[int]
IPP_PORTRAIT: Final[int]
IPP_PRINTER_BUSY: Final[int]
IPP_PRINTER_IDLE: Final[int]
IPP_PRINTER_IS_DEACTIVATED: Final[int]
IPP_PRINTER_PROCESSING: Final[int]
IPP_PRINTER_STOPPED: Final[int]
IPP_PRINT_SUPPORT_FILE_NOT_FOUND: Final[int]
IPP_QUALITY_DRAFT: Final[int]
IPP_QUALITY_HIGH: Final[int]
IPP_QUALITY_NORMAL: Final[int]
IPP_REDIRECTION_OTHER_SITE: Final[int]
IPP_REQUEST_ENTITY: Final[int]
IPP_REQUEST_VALUE: Final[int]
IPP_RES_PER_CM: Final[int]
IPP_RES_PER_INCH: Final[int]
IPP_REVERSE_LANDSCAPE: Final[int]
IPP_REVERSE_PORTRAIT: Final[int]
IPP_SERVICE_UNAVAILABLE: Final[int]
IPP_STATE_ATTRIBUTE: Final[int]
IPP_STATE_DATA: Final[int]
IPP_STATE_ERROR: Final[int]
IPP_STATE_HEADER: Final[int]
IPP_STATE_IDLE: Final[int]
IPP_STATUS_ERROR_ATTRIBUTES_NOT_SETTABLE: Final[int]
IPP_STATUS_ERROR_ATTRIBUTES_OR_VALUES: Final[int]
IPP_STATUS_ERROR_BAD_REQUEST: Final[int]
IPP_STATUS_ERROR_BUSY: Final[int]
IPP_STATUS_ERROR_CHARSET: Final[int]
IPP_STATUS_ERROR_COMPRESSION_ERROR: Final[int]
IPP_STATUS_ERROR_COMPRESSION_NOT_SUPPORTED: Final[int]
IPP_STATUS_ERROR_CONFLICTING: Final[int]
IPP_STATUS_ERROR_CUPS_AUTHENTICATION_CANCELED: Final[int]
IPP_STATUS_ERROR_CUPS_PKI: Final[int]
IPP_STATUS_ERROR_CUPS_UPGRADE_REQUIRED: Final[int]
IPP_STATUS_ERROR_DEVICE: Final[int]
IPP_STATUS_ERROR_DOCUMENT_ACCESS: Final[int]
IPP_STATUS_ERROR_DOCUMENT_FORMAT_ERROR: Final[int]
IPP_STATUS_ERROR_DOCUMENT_FORMAT_NOT_SUPPORTED: Final[int]
IPP_STATUS_ERROR_FORBIDDEN: Final[int]
IPP_STATUS_ERROR_GONE: Final[int]
IPP_STATUS_ERROR_IGNORED_ALL_NOTIFICATIONS: Final[int]
IPP_STATUS_ERROR_IGNORED_ALL_SUBSCRIPTIONS: Final[int]
IPP_STATUS_ERROR_INTERNAL: Final[int]
IPP_STATUS_ERROR_JOB_CANCELED: Final[int]
IPP_STATUS_ERROR_MULTIPLE_JOBS_NOT_SUPPORTED: Final[int]
IPP_STATUS_ERROR_NOT_ACCEPTING_JOBS: Final[int]
IPP_STATUS_ERROR_NOT_AUTHENTICATED: Final[int]
IPP_STATUS_ERROR_NOT_AUTHORIZED: Final[int]
IPP_STATUS_ERROR_NOT_FOUND: Final[int]
IPP_STATUS_ERROR_NOT_POSSIBLE: Final[int]
IPP_STATUS_ERROR_OPERATION_NOT_SUPPORTED: Final[int]
IPP_STATUS_ERROR_PRINTER_IS_DEACTIVATED: Final[int]
IPP_STATUS_ERROR_PRINT_SUPPORT_FILE_NOT_FOUND: Final[int]
IPP_STATUS_ERROR_REQUEST_ENTITY: Final[int]
IPP_STATUS_ERROR_REQUEST_VALUE: Final[int]
IPP_STATUS_ERROR_SERVICE_UNAVAILABLE: Final[int]
IPP_STATUS_ERROR_TEMPORARY: Final[int]
IPP_STATUS_ERROR_TIMEOUT: Final[int]
IPP_STATUS_ERROR_TOO_MANY_SUBSCRIPTIONS: Final[int]
IPP_STATUS_ERROR_URI_SCHEME: Final[int]
IPP_STATUS_ERROR_VERSION_NOT_SUPPORTED: Final[int]
IPP_STATUS_OK: Final[int]
IPP_STATUS_OK_BUT_CANCEL_SUBSCRIPTION: Final[int]
IPP_STATUS_OK_CONFLICTING: Final[int]
IPP_STATUS_OK_EVENTS_COMPLETE: Final[int]
IPP_STATUS_OK_IGNORED_NOTIFICATIONS: Final[int]
IPP_STATUS_OK_IGNORED_OR_SUBSTITUTED: Final[int]
IPP_STATUS_OK_IGNORED_SUBSCRIPTIONS: Final[int]
IPP_STATUS_OK_TOO_MANY_EVENTS: Final[int]
IPP_STATUS_REDIRECTION_OTHER_SITE: Final[int]
IPP_TAG_BOOLEAN: Final[int]
IPP_TAG_CHARSET: Final[int]
IPP_TAG_ENUM: Final[int]
IPP_TAG_INTEGER: Final[int]
IPP_TAG_JOB: Final[int]
IPP_TAG_KEYWORD: Final[int]
IPP_TAG_LANGUAGE: Final[int]
IPP_TAG_MIMETYPE: Final[int]
IPP_TAG_NAME: Final[int]
IPP_TAG_OPERATION: Final[int]
IPP_TAG_PRINTER: Final[int]
IPP_TAG_RANGE: Final[int]
IPP_TAG_STRING: Final[int]
IPP_TAG_TEXT: Final[int]
IPP_TAG_URI: Final[int]
IPP_TAG_ZERO: Final[int]
IPP_TEMPORARY_ERROR: Final[int]
IPP_TIMEOUT: Final[int]
IPP_TOO_MANY_SUBSCRIPTIONS: Final[int]
IPP_UPGRADE_REQUIRED: Final[int]
IPP_URI_SCHEME: Final[int]
IPP_VERSION_NOT_SUPPORTED: Final[int]
PPD_CONFORM_RELAXED: Final[int]
PPD_CONFORM_STRICT: Final[int]
PPD_ORDER_ANY: Final[int]
PPD_ORDER_DOCUMENT: Final[int]
PPD_ORDER_EXIT: Final[int]
PPD_ORDER_JCL: Final[int]
PPD_ORDER_PAGE: Final[int]
PPD_ORDER_PROLOG: Final[int]
PPD_UI_BOOLEAN: Final[int]
PPD_UI_PICKMANY: Final[int]
PPD_UI_PICKONE: Final[int]

@final
class Attribute:
    """
    PPD attribute
    =============

      A PPD attribute.

    @type name: string
    @ivar name: attribute name
    @type spec: string
    @ivar spec: specifier string (if any)
    @type text: string
    @ivar text: human-readable text (if any)
    @type value: string
    @ivar value: attribute value
    """
    @property
    def name(self) -> str:
        """name"""
        ...
    @property
    def spec(self) -> str:
        """spec"""
        ...
    @property
    def text(self) -> str:
        """text"""
        ...
    @property
    def value(self) -> str:
        """value"""
        ...
    def __init__(self, *args: Unused) -> None: ...

@final
class Connection:
    """
    CUPS connection
    ===============

      A connection to the CUPS server.  Before it is created the 
      connection server and username should be set using 
      L{cups.setServer} and L{cups.setUser}; otherwise the defaults will 
      be used.  When a Connection object is instantiated it results in a 
      call to the libcups function httpConnectEncrypt().

      The constructor takes optional arguments host, port, and encryption, 
      which default to the values of L{cups.getServer}(), 
      L{cups.getPort}(), and L{cups.getEncryption}().
    """
    def __init__(self, host: str = ..., port: int = ..., encryption: int = ...) -> None: ...
    def acceptJobs(self, name: str, /) -> None:
        """
        acceptJobs(name) -> None

        Cause printer to accept jobs.
        @type name: string
        @param name: queue name
        @raise IPPError: IPP problem
        """
        ...

    @overload
    def addPrinter(self, name: str, filename: str = ..., *, info: str = ..., location: str = ..., device: str = ...) -> None:
        """
        addPrinter(name) -> None

        Add or adjust a print queue.  Several parameters can select which
        PPD to use (filename, ppdname, and ppd) but only one may be
        given.

        @type filename: string
        @keyword filename: local filename of PPD file
        @type ppdname: string
        @keyword ppdname: filename from L{getPPDs}
        @type info: string
        @keyword info: human-readable information about the printer
        @type location: string
        @keyword location: human-readable printer location
        @type device: string
        @keyword device: device URI string
        @type ppd: L{cups.PPD} instance
        @keyword ppd: PPD object
        @raise IPPError: IPP problem
        """
        ...
    @overload
    def addPrinter(self, name: str, *, ppdname: str = ..., info: str = ..., location: str = ..., device: str = ...) -> None:
        """
        addPrinter(name) -> None

        Add or adjust a print queue.  Several parameters can select which
        PPD to use (filename, ppdname, and ppd) but only one may be
        given.

        @type filename: string
        @keyword filename: local filename of PPD file
        @type ppdname: string
        @keyword ppdname: filename from L{getPPDs}
        @type info: string
        @keyword info: human-readable information about the printer
        @type location: string
        @keyword location: human-readable printer location
        @type device: string
        @keyword device: device URI string
        @type ppd: L{cups.PPD} instance
        @keyword ppd: PPD object
        @raise IPPError: IPP problem
        """
        ...
    @overload
    def addPrinter(self, name: str, *, info: str = ..., location: str = ..., device: str = ..., ppd: PPD = ...) -> None:
        """
        addPrinter(name) -> None

        Add or adjust a print queue.  Several parameters can select which
        PPD to use (filename, ppdname, and ppd) but only one may be
        given.

        @type filename: string
        @keyword filename: local filename of PPD file
        @type ppdname: string
        @keyword ppdname: filename from L{getPPDs}
        @type info: string
        @keyword info: human-readable information about the printer
        @type location: string
        @keyword location: human-readable printer location
        @type device: string
        @keyword device: device URI string
        @type ppd: L{cups.PPD} instance
        @keyword ppd: PPD object
        @raise IPPError: IPP problem
        """
        ...

    def addPrinterOptionDefault(self, name: str, option: str, value: str | int | Sequence[str | int], /) -> None:
        """
        addPrinterOptionDefault(name, option, value) -> None

        Set a network default option.  Jobs submitted to the named queue 
        will have the job option added if it is not already present in the 
        job.  This works with CUPS servers of at least version 1.2.

        @type name: string
        @param name: queue name
        @type option: string
        @param option: option name, for example 'job-priority'
        @type value: string
        @param value: option value as a string
        @raise IPPError: IPP problem
        """
        ...
    def addPrinterToClass(self, name: str, _class: str, /) -> None:
        """
        addPrinterToClass(name, class) -> None

        Add a printer to a class.  If the class does not yet exist, 
        it is created.

        @type name: string
        @param name: queue name
        @type class: string
        @param class: class name
        @raise IPPError: IPP problem
        """
        ...
    def adminExportSamba(self, name: str, server: str, user: str, password: str, /):
        """
        adminExportSamba(name, samba_server, samba_username,
                         samba_password) -> None

        Export a printer to Samba.

        @type name: string
        @param name: queue name
        @type samba_server: string
        @param samba_server: samba server
        @type samba_username: string
        @param samba_username: samba username
        @type samba_password: string
        @param samba_password: samba password
        @raise IPPError: IPP problem
        """
        ...
    def adminGetServerSettings(self) -> dict[str, str]:
        """
        adminGetServerSettings() -> dict

        Get server settings.

        @return: dict representing server settings; keywords include 
        L{CUPS_SERVER_DEBUG_LOGGING}, L{CUPS_SERVER_REMOTE_ADMIN}, 
        L{CUPS_SERVER_REMOTE_PRINTERS}, L{CUPS_SERVER_SHARE_PRINTERS}, 
        L{CUPS_SERVER_USER_CANCEL_ANY}
        @see: L{adminSetServerSettings}
        @raise IPPError: IPP problem
        """
        ...
    def adminSetServerSettings(self, settings: dict[str, str], /) -> None:
        """
        adminSetServerSettings(settings) -> None

        Set server settings.

        @type settings: dict
        @param settings: dict of server settings
        @see: L{adminGetServerSettings}
        @raise IPPError: IPP problem
        """
        ...
    def authenticateJob(self, jobid: int, auth_info: list[str] = ..., /) -> None:
        """
        authenticateJob(jobid, auth_info=None) -> None

        @type jobid: integer
        @param jobid: job ID to authenticate
        @type auth_info: optional string list
        @param auth_info: authentication details
        @raise IPPError: IPP problem
        """
        ...

    @overload
    def cancelAllJobs(self, name: str, *, my_jobs: bool = False, purge_jobs: bool = True) -> None:
        """
        cancelAllJobs(name=None, uri=None, my_jobs=False, purge_jobs=True) -> None

        @type name: string
        @param name: queue name
        @type uri: string
        @param uri: printer URI
        @type my_jobs: boolean
        @param my_jobs: whether to restrict operation to jobs owned by 
        the current CUPS user (as set by L{cups.setUser}).
        @type purge_jobs: boolean
        @param purge_jobs: whether to remove data and control files
        @raise IPPError: IPP problem
        """
        ...
    @overload
    def cancelAllJobs(self, *, uri: str, my_jobs: bool = False, purge_jobs: bool = True) -> None:
        """
        cancelAllJobs(name=None, uri=None, my_jobs=False, purge_jobs=True) -> None

        @type name: string
        @param name: queue name
        @type uri: string
        @param uri: printer URI
        @type my_jobs: boolean
        @param my_jobs: whether to restrict operation to jobs owned by 
        the current CUPS user (as set by L{cups.setUser}).
        @type purge_jobs: boolean
        @param purge_jobs: whether to remove data and control files
        @raise IPPError: IPP problem
        """
        ...

    def cancelJob(self, job_id: int, purge_job: bool = False) -> None:
        """
        cancelJob(jobid, purge_job=False) -> None

        @type jobid: integer
        @param jobid: job ID to cancel
        @type purge_job: boolean
        @param purge_job: whether to remove data and control files
        @raise IPPError: IPP problem
        """
        ...
    def cancelSubscription(self, id: int, /) -> None:
        """
        cancelSubscription(id) -> None

        Cancel a subscription.

        @type id: integer
        @param id: subscription ID
        @raise IPPError: IPP problem
        """
        ...
    def createJob(self, printer: str, title: str, options: dict[str, str]) -> int:
        """
        createJob(printer, title, options) -> integer

        Create an empty job for streaming.

        @type printer: string
        @param printer: queue name
        @type title: string
        @param title: title of the print job
        @type options: dict
        @param options: dict of options
        @return: job ID
        @raise IPPError: IPP problem
        """
        ...
    def createSubscription(
        self,
        uri: str,
        events: list[str] = ...,
        job_id: int = ...,
        recipient_uri: str = ...,
        lease_duration: int = ...,
        time_interval: int = ...,
        user_data: str = ...,
    ) -> int:
        """
        createSubscription(uri, events=[], job_id=-1, recipient_uri=,
                           lease_duration=-1, time_interval=-1,
                           user_data=) -> integer

        Create a subscription.

        @type uri: string
        @param uri: URI for object
        @type events: string list
        @keyword events: events to receive notifications for
        @type job_id: integer
        @keyword job_id: job ID to receive notifications for
        @type recipient_uri: string
        @keyword recipient_uri: URI for notifications recipient
        @type lease_duration: integer
        @keyword lease_duration: lease duration in seconds
        @type time_interval: integer
        @keyword time_interval: time interval
        @type user_data: string
        @keyword user_data: user data to receive with notifications
        @return: subscription ID
        @raise IPPError: IPP problem
        """
        ...
    def deleteClass(self, _class: str, /) -> None:
        """
        deleteClass(class) -> None

        Delete a class.

        @type class: string
        @param class: class name
        @raise IPPError: IPP problem
        """
        ...
    def deletePrinter(self, name: str, /) -> None:
        """
        deletePrinter(name) -> None

        Delete a printer.

        @type name: string
        @param name: queue name
        @raise IPPError: IPP problem
        """
        ...
    def deletePrinterFromClass(self, name: str, _class: str, /) -> None:
        """
        deletePrinterFromClass(name, class) -> None

        Remove a printer from a class.  If the class would be left empty, 
        it is removed.

        @type name: string
        @param name: queue name
        @type class: string
        @param class: class name
        @raise IPPError: IPP problem
        """
        ...
    def deletePrinterOptionDefault(self, name: str, option: str, /) -> None:
        """
        deletePrinterOptionDefault(name, option) -> None

        Removes a network default option.  See L{addPrinterOptionDefault}.

        @type name: string
        @param name: queue name
        @type option: string
        @param option: option name, for example 'job-priority'
        @raise IPPError: IPP problem
        """
        ...
    def disablePrinter(self, name: str, reason: str = ...) -> None:
        """
        disablePrinter(name) -> None

        Disable printer.  This prevents the printer from processing its 
        job queue.

        @type name: string
        @param name: queue name
        @type reason: string
        @keyword reason: optional human-readable reason for disabling the 
        printer
        @raise IPPError: IPP problem
        """
        ...
    def enablePrinter(self, name: str, /) -> None:
        """
        enablePrinter(name) -> None

        Enable printer.  This allows the printer to process its job queue.

        @type name: string
        @param name: queue name
        @raise IPPError: IPP problem
        """
        ...
    def finishDocument(self, printer: str) -> int:
        """
        finishDocument(printer) -> integer

        Finish sending a document.

        @type printer: string
        @param printer: queue name
        @return: HTTP status
        @raise IPPError: IPP problem
        """
        ...
    def getClasses(self) -> dict[str, str | list[str]]:
        """
        getClasses() -> dict

        @return: a dict, indexed by name, of objects representing
        classes.  Each class object is either a string, in which case it
        is for the remote class; or a list, in which case it is a list of
        queue names.
        @raise IPPError: IPP problem
        """
        ...
    def getDefault(self) -> str | None:
        """
        getDefault() -> string or None

        Get the system default printer.

        @return: default printer name or None
        """
        ...
    def getDests(self) -> dict[tuple[str, str] | tuple[None, None], Dest]:
        """
        getDests() -> dict

        @return: a dict representing available destinations.  Each 
        dictionary key is a pair of (queue, instance) strings, and the 
        dictionary value is a L{cups.Dest} object.  In addition to the 
        available destinations, a special dictionary key (None,None) is 
        provided for looking up the default destination; this destination 
        will also be available under its own key.
        @raise IPPError: IPP problem
        """
        ...
    def getDevices(
        self, limit: int = 0, exclude_schemes: list[str] = ..., include_schemes: list[str] = ..., timeout: int = 0
    ) -> dict[str, _CupsDevice]:
        """
        getDevices(limit=0, exclude_schemes=None, include_schemes=None) -> dict

        @type limit: integer
        @param limit: maximum number of devices to return
        @type exclude_schemes: string list
        @param exclude_schemes: URI schemes to exclude
        @type include_schemes: string list
        @param include_schemes: URI schemes to include
        @return: a dict, indexed by device URI, of dicts representing
        devices, indexed by attribute.
        @raise IPPError: IPP problem
        """
        ...
    def getDocument(self, printer_uri: str, job_id: int, document_number: int, /) -> _CupsDocument:
        """
        getDocument(printer_uri, job_id, document_number) -> dict

        Fetches the job document and stores it in a temporary file.

        @type printer_uri: string
        @param printer_uri: the printer-uri for the printer
        @type job_id: integer
        @param job_id: the job ID
        @type document_number: integer
        @param document_number: the document number to retrieve
        @return: a dict with the following keys:  'file' (string), temporary filename holding the job document;  'document-format' (string), its MIME type.  There may also be a  'document-name' key, in which case this is for the document name.
        @raise RuntimeError: Not supported in libcups until 1.4
        @raise IPPError: IPP problem
        """
        ...

    @overload
    def getFile(self, resource: str, filename: str = ...) -> None:
        """
        getFile(resource, filename=None, fd=-1, file=None) -> None

        Fetch a CUPS server resource to a local file.

        This is for obtaining CUPS server configuration files and 
        log files.

        @type resource: string
        @param resource: resource name
        @type filename: string
        @param filename: name of local file for storage
        @type fd: int
        @param fd: file descriptor of local file
        @type file: file
        @param file: Python file object for local file
        @raise HTTPError: HTTP problem
        """
        ...
    @overload
    def getFile(self, resource: str, *, fd: int) -> None:
        """
        getFile(resource, filename=None, fd=-1, file=None) -> None

        Fetch a CUPS server resource to a local file.

        This is for obtaining CUPS server configuration files and 
        log files.

        @type resource: string
        @param resource: resource name
        @type filename: string
        @param filename: name of local file for storage
        @type fd: int
        @param fd: file descriptor of local file
        @type file: file
        @param file: Python file object for local file
        @raise HTTPError: HTTP problem
        """
        ...
    @overload
    def getFile(self, resource: str, *, file: _FileOrFd) -> None:
        """
        getFile(resource, filename=None, fd=-1, file=None) -> None

        Fetch a CUPS server resource to a local file.

        This is for obtaining CUPS server configuration files and 
        log files.

        @type resource: string
        @param resource: resource name
        @type filename: string
        @param filename: name of local file for storage
        @type fd: int
        @param fd: file descriptor of local file
        @type file: file
        @param file: Python file object for local file
        @raise HTTPError: HTTP problem
        """
        ...

    def getJobAttributes(self, job_id: int, requested_attributes: list[str] = ...) -> _CupsJobWithAttributeInfo:
        """
        getJobAttributes(jobid, requested_attributes=None) -> dict

        Fetch job attributes.
        @type jobid: integer
        @param jobid: job ID
        @type requested_attributes: string list
        @param requested_attributes: list of requested attribute names
        @return: a dict representing job attributes.
        @raise IPPError: IPP problem
        """
        ...
    def getJobs(
        self,
        which_jobs: Literal["completed", "not-completed", "all"] = "not-completed",
        my_jobs: bool = False,
        limit: int = ...,
        first_job_id: int = ...,
        requested_attributes: list[str] = ["job-id", "job-uri"],
    ) -> dict[int, _CupsJob]:
        """
        getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1, requested_attributes=None) -> dict
        Fetch a list of jobs.
        @type which_jobs: string
        @param which_jobs: which jobs to fetch; possible values: 
        'completed', 'not-completed', 'all'
        @type my_jobs: boolean
        @param my_jobs: whether to restrict the returned jobs to those 
        owned by the current CUPS user (as set by L{cups.setUser}).
        @return: a dict, indexed by job ID, of dicts representing job
        attributes.
        @type limit: integer
        @param limit: maximum number of jobs to return
        @type first_job_id: integer
        @param first_job_id: lowest job ID to return
        @type requested_attributes: string list
        @param requested_attributes: list of requested attribute names
        @raise IPPError: IPP problem
        """
        ...
    def getNotifications(self, subscription_ids: list[int], sequence_numbers: list[int] = ...) -> _CupsNotifications:
        """
        getNotifications(subscription_ids) -> list

        Get notifications for subscribed events.

        @type subscription_ids: integer list
        @param subscription_ids: list of subscription IDs to receive 
        notifications for
        @return: list of dicts, each representing an event
        @raise IPPError: IPP problem
        """
        ...
    def getPPD(self, name: str, /) -> str:
        """
        getPPD(name) -> string

        Fetch a printer's PPD.

        @type name: string
        @param name: queue name
        @return: temporary PPD file name
        @raise IPPError: IPP problem
        """
        ...
    def getPPD3(self, name: str, modtime: float = ..., filename: str = ...) -> tuple[int, float, str]:
        """
        getPPD3(name[, modtime, filename]) -> (status,modtime,filename)

        Fetch a printer's PPD if it is newer.

        @type name: string
        @param name: queue name
        @type modtime: float
        @param modtime: modification time of existing file
        @type filename: string
        @param filename: filename of existing file
        @return: tuple of HTTP status, modification time, and filename
        """
        ...
    def getPPDs(
        self,
        limit: int = ...,
        exclude_schemes: list[str] = ...,
        include_schemes: list[str] = ...,
        ppd_natural_language: str = ...,
        ppd_device_id: str = ...,
        ppd_make: str = ...,
        ppd_make_and_model: str = ...,
        ppd_model_number: int = ...,
        ppd_product: str = ...,
        ppd_psversion: str = ...,
        ppd_type: str = ...,
    ) -> dict[str, _CupsPPD]:
        """
        getPPDs(limit=0, exclude_schemes=None, include_schemes=None, 
        ppd_natural_language=None, ppd_device_id=None, ppd_make=None, 
        ppd_make_and_model=None, ppd_model_number=-1, ppd_product=None, 
        ppd_psversion=None, ppd_type=None) -> dict

        @type limit: integer
        @param limit: maximum number of PPDs to return
        @type exclude_schemes: string list
        @param exclude_schemes: list of PPD schemes to exclude
        @type include_schemes: string list
        @param include_schemes: list of PPD schemes to include
        @type ppd_natural_language: string
        @param ppd_natural_language: required language
        @type ppd_device_id: string
        @param ppd_device_id: IEEE 1284 Device ID to match against
        @type ppd_make: string
        @param ppd_make: required printer manufacturer
        @type ppd_make_and_model: string
        @param ppd_make_and_model: required make and model
        @type ppd_model_number: integer
        @param ppd_model_number: model number required (from cupsModelNumber 
        in PPD file)
        @type ppd_product: string
        @param ppd_product: required PostScript product string (Product)
        @type ppd_psversion: string
        @param ppd_psversion: required PostScript version (PSVersion)
        @type ppd_type: string
        @param ppd_type: required type of PPD. Valid values are fax; pdf; 
        postscript; raster; unknown.
        @return: a dict, indexed by PPD name, of dicts representing
        PPDs, indexed by attribute.
        @raise IPPError: IPP problem
        """
        ...
    def getPPDs2(
        self,
        limit: int = ...,
        exclude_schemes: list[str] = ...,
        include_schemes: list[str] = ...,
        ppd_natural_language: str = ...,
        ppd_device_id: str = ...,
        ppd_make: str = ...,
        ppd_make_and_model: str = ...,
        ppd_model_number: int = ...,
        ppd_product: str = ...,
        ppd_psversion: str = ...,
        ppd_type: str = ...,
    ) -> dict[str, _CupsPPD2]:
        """
        getPPDs2(limit=0, exclude_schemes=None, include_schemes=None, 
        ppd_natural_language=None, ppd_device_id=None, ppd_make=None, 
        ppd_make_and_model=None, ppd_model_number=-1, ppd_product=None, 
        ppd_psversion=None, ppd_type=None) -> dict

        @type limit: integer
        @param limit: maximum number of PPDs to return
        @type exclude_schemes: string list
        @param exclude_schemes: list of PPD schemes to exclude
        @type include_schemes: string list
        @param include_schemes: list of PPD schemes to include
        @type ppd_natural_language: string
        @param ppd_natural_language: required language
        @type ppd_device_id: string
        @param ppd_device_id: IEEE 1284 Device ID to match against
        @type ppd_make: string
        @param ppd_make: required printer manufacturer
        @type ppd_make_and_model: string
        @param ppd_make_and_model: required make and model
        @type ppd_model_number: integer
        @param ppd_model_number: model number required (from cupsModelNumber 
        in PPD file)
        @type ppd_product: string
        @param ppd_product: required PostScript product string (Product)
        @type ppd_psversion: string
        @param ppd_psversion: required PostScript version (PSVersion)
        @type ppd_type: string
        @param ppd_type: required type of PPD. Valid values are fax; pdf; 
        postscript; raster; unknown.
        @return: a dict, indexed by PPD name, of dicts representing
        PPDs, indexed by attribute.  All attribute values are lists.
        @raise IPPError: IPP problem
        """
        ...

    @overload
    def getPrinterAttributes(self, name: str, *, requested_attributes: list[str] = ...) -> _CupsPrinter:
        """
        getPrinterAttributes(name=None, uri=None, requested_attributes=None) -> dict
        Fetch the attributes for a printer, specified either by name or by 
        uri but not both.

        @type name: string
        @param name: queue name
        @type uri: string
        @param uri: queue URI
        @type requested_attributes: string list
        @param requested_attributes: list of requested attribute names
        @return: a dict, indexed by attribute, of printer attributes
        for the specified printer.

        Attributes:
          - 'job-sheets-supported': list of strings
          - 'job-sheets-default': tuple of strings (start, end)
          - 'printer-error-policy-supported': if present, list of strings
          - 'printer-error-policy': if present, string
          - 'printer-op-policy-supported': if present, list of strings
          - 'printer-op-policy': if present, string

        There are other attributes; the exact list of attributes returned 
        will depend on the IPP server.
        @raise IPPError: IPP problem
        """
        ...
    @overload
    def getPrinterAttributes(self, *, uri: str, requested_attributes: list[str] = ...) -> _CupsPrinter:
        """
        getPrinterAttributes(name=None, uri=None, requested_attributes=None) -> dict
        Fetch the attributes for a printer, specified either by name or by 
        uri but not both.

        @type name: string
        @param name: queue name
        @type uri: string
        @param uri: queue URI
        @type requested_attributes: string list
        @param requested_attributes: list of requested attribute names
        @return: a dict, indexed by attribute, of printer attributes
        for the specified printer.

        Attributes:
          - 'job-sheets-supported': list of strings
          - 'job-sheets-default': tuple of strings (start, end)
          - 'printer-error-policy-supported': if present, list of strings
          - 'printer-error-policy': if present, string
          - 'printer-op-policy-supported': if present, list of strings
          - 'printer-op-policy': if present, string

        There are other attributes; the exact list of attributes returned 
        will depend on the IPP server.
        @raise IPPError: IPP problem
        """
        ...

    def getPrinters(self) -> dict[str, _CupsPrinterSimple]:
        """
        getPrinters() -> dict

        @return: a dict, indexed by name, of dicts representing
        queues, indexed by attribute.
        @raise IPPError: IPP problem
        """
        ...
    def getServerPPD(self, ppd_name: str, /) -> str:
        """
        getServerPPD(ppd_name) -> string

        Fetches the named PPD and stores it in a temporary file.

        @type ppd_name: string
        @param ppd_name: the ppd-name of a PPD
        @return: temporary filename holding the PPD
        @raise RuntimeError: Not supported in libcups until 1.3
        @raise IPPError: IPP problem
        """
        ...
    def getSubscriptions(self, uri: str, my_subscriptions: bool = False, job_id: int = ...) -> list[_CupsSubscription]:
        """
        getSubscriptions(uri) -> integer list

        Get subscriptions.

        @type uri: string
        @param uri: URI for object
        @type my_subscriptions: boolean
        @keyword my_subscriptions: only return subscriptions belonging to 
        the current user (default False)
        @type job_id: integer
        @keyword job_id: only return subscriptions relating to this job
        @return: list of subscriptions
        @raise IPPError: IPP problem
        """
        ...

    @overload
    def moveJob(self, printer_uri: str, job_id: int, job_printer_uri: str) -> None:
        """
        moveJob(printer_uri=None, job_id=-1, job_printer_uri) -> None

        Move a job specified by printer_uri and jobid (only one need be given)
        to the printer specified by job_printer_uri.

        @type job_id: integer
        @param job_id: job ID to move
        @type printer_uri: string
        @param printer_uri: printer to move job(s) from
        @type job_printer_uri: string
        @param job_printer_uri: printer to move job(s) to
        @raise IPPError: IPP problem
        """
        ...
    @overload
    def moveJob(self, printer_uri: str, *, job_printer_uri: str) -> None:
        """
        moveJob(printer_uri=None, job_id=-1, job_printer_uri) -> None

        Move a job specified by printer_uri and jobid (only one need be given)
        to the printer specified by job_printer_uri.

        @type job_id: integer
        @param job_id: job ID to move
        @type printer_uri: string
        @param printer_uri: printer to move job(s) from
        @type job_printer_uri: string
        @param job_printer_uri: printer to move job(s) to
        @raise IPPError: IPP problem
        """
        ...
    @overload
    def moveJob(self, *, job_id: int, job_printer_uri: str) -> None:
        """
        moveJob(printer_uri=None, job_id=-1, job_printer_uri) -> None

        Move a job specified by printer_uri and jobid (only one need be given)
        to the printer specified by job_printer_uri.

        @type job_id: integer
        @param job_id: job ID to move
        @type printer_uri: string
        @param printer_uri: printer to move job(s) from
        @type job_printer_uri: string
        @param job_printer_uri: printer to move job(s) to
        @raise IPPError: IPP problem
        """
        ...

    def printFile(self, printer: str, filename: str, title: str, options: dict[str, str]) -> int:
        """
        printFile(printer, filename, title, options) -> integer

        Print a file.

        @type printer: string
        @param printer: queue name
        @type filename: string
        @param filename: local file path to the document
        @type title: string
        @param title: title of the print job
        @type options: dict
        @param options: dict of options
        @return: job ID
        @raise IPPError: IPP problem
        """
        ...
    def printFiles(self, printer: str, filenames: list[str], title: str, options: dict[str, str]) -> int:
        """
        printFiles(printer, filenames, title, options) -> integer

        Print a list of files.

        @type printer: string
        @param printer: queue name
        @type filenames: list
        @param filenames: list of local file paths to the documents
        @type title: string
        @param title: title of the print job
        @type options: dict
        @param options: dict of options
        @return: job ID
        @raise IPPError: IPP problem
        """
        ...
    def printTestPage(self, name: str) -> int:
        """
        printTestPage(name) -> job ID

        Print a test page.

        @type name: string
        @param name: queue name
        @type file: string
        @keyword file: input file (default is CUPS test page)
        @type title: string
        @keyword title: job title (default 'Test Page')
        @type format: string
        @keyword format: document format (default 'application/postscript')
        @type user: string
        @keyword user: user to submit the job as
        @raise IPPError: IPP problem
        """
        ...

    @overload
    def putFile(self, resource: str, filename: str) -> None:
        """
        putFile(resource, filename=None, fd=-1, file=None) -> None

        This is for uploading new configuration files for the CUPS 
        server.  Note: L{adminSetServerSettings} is a way of 
        adjusting server settings without needing to parse the 
        configuration file.
        @type resource: string
        @param resource: resource name
        @type filename: string
        @param filename: name of local file to upload
        @type fd: int
        @param fd: file descriptor of local file
        @type file: file
        @param file: Python file object for local file
        @raise HTTPError: HTTP problem
        """
        ...
    @overload
    def putFile(self, resource: str, *, fd: int) -> None:
        """
        putFile(resource, filename=None, fd=-1, file=None) -> None

        This is for uploading new configuration files for the CUPS 
        server.  Note: L{adminSetServerSettings} is a way of 
        adjusting server settings without needing to parse the 
        configuration file.
        @type resource: string
        @param resource: resource name
        @type filename: string
        @param filename: name of local file to upload
        @type fd: int
        @param fd: file descriptor of local file
        @type file: file
        @param file: Python file object for local file
        @raise HTTPError: HTTP problem
        """
        ...
    @overload
    def putFile(self, resource: str, *, file: _FileOrFd) -> None:
        """
        putFile(resource, filename=None, fd=-1, file=None) -> None

        This is for uploading new configuration files for the CUPS 
        server.  Note: L{adminSetServerSettings} is a way of 
        adjusting server settings without needing to parse the 
        configuration file.
        @type resource: string
        @param resource: resource name
        @type filename: string
        @param filename: name of local file to upload
        @type fd: int
        @param fd: file descriptor of local file
        @type file: file
        @param file: Python file object for local file
        @raise HTTPError: HTTP problem
        """
        ...

    def rejectJobs(self, name: str, reason: str = ...) -> None:
        """
        rejectJobs(name)

        Cause printer to reject jobs.

        @type name: string
        @param name: queue name
        @type reason: string
        @keyword reason: optional human-readable reason for rejecting jobs
        @raise IPPError: IPP problem
        """
        ...
    def renewSubscription(self, id: int, lease_duration: int = ...) -> None:
        """
        renewSubscription(id, lease_duration=-1) -> None

        Renew a subscription.

        @type id: integer
        @param id: subscription ID
        @type lease_duration: integer
        @param lease_duration: lease duration in seconds
        @raise IPPError: IPP problem
        """
        ...
    def restartJob(self, job_id: int, job_hold_until: str = ...) -> None:
        """
        restartJob(job_id, job_hold_until=None) -> None

        Restart a job.

        @type job_id: integer
        @param job_id: job ID to restart
        @type job_hold_until: string
        @param job_hold_until: new job-hold-until value for job
        @raise IPPError: IPP problem
        """
        ...
    def setDefault(self, name: str, /) -> None:
        """
        setDefault(name) -> None

        Set the system default printer.  Note that this can be over-ridden 
        on a per-user basis using the lpoptions command.

        @type name: string
        @param name: queue name
        @raise IPPError: IPP problem
        """
        ...
    def setJobHoldUntil(self, job_id: int, job_hold_until: str, /) -> None:
        """
        setJobHoldUntil(jobid, job_hold_until) -> None

        Specifies when a job should be printed.
        @type jobid: integer
        @param jobid: job ID to adjust
        @type job_hold_until: string
        @param job_hold_until: when to print the job; examples: 'hold', 
        'immediate', 'restart', resume'
        @raise IPPError: IPP problem
        """
        ...
    def setPrinterDevice(self, name: str, device_uri: str, /) -> None:
        """
        setPrinterDevice(name, device_uri) -> None

        Set the device URI for a printer.

        @type name: string
        @param name: queue name
        @type device_uri: string
        @param device_uri: device URI
        @raise IPPError: IPP problem
        """
        ...
    def setPrinterErrorPolicy(self, name: str, policy: str, /) -> None:
        """
        setPrinterErrorPolicy(name, policy) -> None

        Set the printer's error policy.

        @type name: string
        @param name: queue name
        @type policy: string
        @param policy: policy name; supported policy names can be found 
        by using the L{getPrinterAttributes} function and looking for the 
        'printer-error-policy-supported' attribute
        @raise IPPError: IPP problem
        """
        ...
    def setPrinterInfo(self, name: str, info: str, /) -> None:
        """
        setPrinterInfo(name, info) -> None

        Set the human-readable information about a printer.

        @type name: string
        @param name: queue name
        @type info: string
        @param info: human-readable information about the printer
        @raise IPPError: IPP problem
        """
        ...
    def setPrinterJobSheets(self, name: str, start: str, end: str, /) -> None:
        """
        setPrinterJobSheets(name, start, end) -> None

        Specifies job sheets for a printer.

        @type name: string
        @param name: queue name
        @type start: string
        @param start: name of a sheet to print before each job
        @type end: string
        @param end: name of a sheet to print after each job
        @raise IPPError: IPP problem
        """
        ...
    def setPrinterLocation(self, name: str, location: str, /) -> None:
        """
        setPrinterLocation(name, location) -> None

        Set the human-readable printer location

        @type name: string
        @param name: queue name
        @type location: string
        @param location: human-readable printer location
        @raise IPPError: IPP problem
        """
        ...
    def setPrinterOpPolicy(self, name: str, policy: str, /) -> None:
        """
        setPrinterOpPolicy(name, policy) -> None

        Set the printer's operation policy.

        @type name: string
        @param name: queue name
        @type policy: string
        @param policy: policy name; supported policy names can be found 
        by using the L{getPrinterAttributes} function and looking for the 
        'printer-op-policy-supported' attribute
        @raise IPPError: IPP problem
        """
        ...
    def setPrinterShared(self, name: str, shared: bool, /) -> None:
        """
        setPrinterShared(name, shared) -> None

        Set whether a printer is shared with other people.  This works 
        with CUPS servers of at least version 1.2, by setting the 
        printer-is-shared printer attribute.

        @type name: string
        @param name: queue name
        @type shared: boolean
        @param shared: whether printer should be shared
        @raise IPPError: IPP problem
        """
        ...
    def setPrinterUsersAllowed(self, name: str, allowed: list[str], /) -> None:
        """
        setPrinterUsersAllowed(name, allowed) -> None

        Set the list of users allowed to use a printer.  This works 
        with CUPS server of at least version 1.2, by setting the 
        requesting-user-name-allowed printer attribute.

        @type name: string
        @param name: queue name
        @type allowed: string list
        @param allowed: list of allowed users; ['all'] 
        means there will be no user-name restriction.
        @raise IPPError: IPP problem
        """
        ...
    def setPrinterUsersDenied(self, name: str, denied: list[str], /) -> None:
        """
        setPrinterUsersDenied(name, denied) -> None

        Set the list of users denied the use of a printer.  This works 
        with CUPS servers of at least version 1.2, by setting the 
        requesting-user-name-denied printer attribute.

        @type name: string
        @param name: queue name
        @type denied: string list
        @param denied: list of denied users; ['none'] 
        means there will be no user-name restriction.
        @raise IPPError: IPP problem
        """
        ...
    def startDocument(self, printer: str, job_id: int, doc_name: str, format: str, last_document: bool) -> int:
        """
        startDocument(printer, job_id, doc_name, format, last_document) -> integer

        Add a document to a job created with createJob.

        @type printer: string
        @param printer: queue name
        @type job_id: integer
        @param job_id: job ID to create document
        @type doc_name: string
        @param doc_name: name of the document
        @type format: string
        @param format: MIME type
        @type last_document: integer
        @param last_document: 1 for last document of job, 0 otherwise
        @return: HTTP status
        @raise IPPError: IPP problem
        """
        ...
    def writeRequestData(self, buffer: bytes, length: int) -> int:
        """
        writeRequestData(buffer, length) -> integer

        Write data after an IPP request.

        @type buffer: string
        @param buffer: bytes to write
        @type length: integer
        @param length: number of bytes to write
        @return: HTTP status
        @raise IPPError: IPP problem
        """
        ...

@final
class Constraint:
    """
    PPD constraint
    ==============

      A PPD constraint.

    @type option1: string
    @ivar option1: first option keyword
    @type choice1: string
    @ivar choice1: first option choice
    @type option2: string
    @ivar option2: second option keyword
    @type choice2: string
    @ivar choice2: secondoption choice
    """
    @property
    def choice1(self) -> str:
        """choice1"""
        ...
    @property
    def choice2(self) -> str:
        """choice2"""
        ...
    @property
    def option1(self) -> str:
        """option1"""
        ...
    @property
    def option2(self) -> str:
        """option2"""
        ...
    def __init__(self, *args: Unused) -> None: ...

@final
class Dest:
    """
    CUPS destination
    ================

      A destination print queue, as returned by L{Connection.getDests}.

    @type name: string
    @ivar name: destination queue name
    @type instance: string
    @ivar instance: destination instance name
    @type is_default: boolean
    @ivar is_default: whether this is the default destination
    @type options: dict
    @ivar options: string:string dict of default options for this 
    destination, indexed by option name
    """
    @property
    def instance(self) -> str | None:
        """instance"""
        ...
    @property
    def is_default(self) -> bool:
        """is_default"""
        ...
    @property
    def name(self) -> str:
        """name"""
        ...
    @property
    def options(self) -> dict[str, str]:
        """options"""
        ...
    def __init__(self, *args: Unused) -> None: ...

@final
class Group:
    """
    PPD option group
    ================

      A PPD option group.

    @type text: string
    @ivar text: user-presentable group name
    @type name: string
    @ivar name: unique group name
    @type options: L{Option} list
    @ivar options: list of options in the group
    @type subgroups: L{Group} list
    @ivar subgroups: list of subgroups in the group
    """
    @property
    def name(self) -> str:
        """name"""
        ...
    @property
    def options(self) -> list[Option]:
        """options"""
        ...
    @property
    def subgroups(self) -> list[Group]:
        """subgroups"""
        ...
    @property
    def text(self) -> str:
        """text"""
        ...
    def __init__(self, *args: Unused) -> None: ...

class HTTPError(Exception):
    """
    This exception is raised when an HTTP problem has occurred.  It 
    provides an integer HTTP status code.

    Use it like this::
      try:
        ...
      except cups.HTTPError as (status):
        print 'HTTP status is %d' % status
    """
    ...

@final
class IPPAttribute:
    """
    IPP Attribute
    =============
      An IPP attribute.

    @type group_tag: int
    @ivar group_tag: IPP group tag
    @type value_tag: int
    @ivar value_tag: IPP value tag
    @type values: list
    @ivar value: list of values
    """
    @property
    def group_tag(self) -> int:
        """IPP group tag"""
        ...
    @property
    def name(self) -> str:
        """IPP attribute name"""
        ...
    @property
    def value_tag(self) -> int:
        """IPP value tag"""
        ...
    @property
    def values(self) -> list[int | str | bool]:
        """List of values"""
        ...
    def __init__(self, group_tag: int, value_tag: int, name: str, value: str = ..., /) -> None: ...

class IPPError(Exception):
    """
    This exception is raised when an IPP error has occurred.  It 
    provides an integer IPP status code, and a human-readable string 
    describing the error.

    Use it like this::
      try:
        ...
      except cups.IPPError as (status, description):
        print 'IPP status is %d' % status
        print 'Meaning:', description
    """
    ...

@final
class IPPRequest:
    """
    IPP Request
    ===========
      An IPP request.  The constructor takes an optional argument of the
    operation code.
    """
    @property
    def attributes(self) -> list[IPPAttribute]:
        """IPP request attributes"""
        ...
    @property
    def operation(self) -> int:
        """IPP request operation"""
        ...

    @property
    def state(self) -> int:
        """IPP request transfer state"""
        ...
    @state.setter
    def state(self, value: int) -> None:
        """IPP request transfer state"""
        ...

    @property
    def statuscode(self) -> int:
        """IPP response status code"""
        ...
    @statuscode.setter
    def statuscode(self, value: int) -> None:
        """IPP response status code"""
        ...

    def __init__(self, op: int = ..., /) -> None: ...
    def add(self, attr: IPPAttribute, /) -> IPPAttribute:
        """
        add(attr) -> IPPAttribute

        @type attr: IPPAttribute
        @param attr: Attribute to add to the request
        @return: IPP request attribute
        """
        ...
    def addSeparator(self) -> IPPAttribute:
        """
        addSeparator() -> IPPAttribute

        @return: IPP request attribute
        """
        ...
    def readIO(self, read_fn: Callable[[int], int], blocking: bool = True) -> int:
        """
        readIO(read_fn, blocking=True) -> IPP state

        @type read_fn: Callable function
        @param read_fn: A callback, taking a single integer argument for
        'size', for reading IPP data
        @type blocking: Boolean
        @param blocking: whether to continue reading until a complete
        request is read
        @return: IPP state value
        """
        ...
    def writeIO(self, write_fn: Callable[[bytes], int], blocking: bool = True) -> int:
        """
        writeIO(write_fn, blocking=True) -> IPP state

        @type write_fn: Callable function
        @param write_fn: A callback, taking a bytes object, for writing
        IPP data
        @type blocking: Boolean
        @param blocking: whether to continue reading until a complete
        request is written
        @return: IPP state value
        """
        ...

@final
class Option:
    """
    PPD option
    ==========
      A PPD option.

    @type conflicted: boolean
    @ivar conflicted: whether this option is in conflict
    @type keyword: string
    @ivar keyword: the option keyword e.g. Duplex
    @type defchoice: string
    @ivar defchoice: the default option choice
    @type text: string
    @ivar text: the user-presentable option name e.g. Double-sided printing
    @type ui: integer
    @ivar ui: the option type; one of L{PPD_UI_BOOLEAN}, 
    L{PPD_UI_PICKONE}, L{PPD_UI_PICKMANY}
    @type choices: list
    @ivar choices: list of the option's choices
    """
    @property
    def choices(self) -> list[_CupsOptionChoice]:
        """choices"""
        ...
    @property
    def conflicted(self) -> bool:
        """Whether this option is in conflict"""
        ...
    @property
    def defchoice(self) -> str:
        """defchoice"""
        ...
    @property
    def keyword(self) -> str:
        """keyword"""
        ...
    @property
    def text(self) -> str:
        """text"""
        ...
    @property
    def ui(self) -> int:
        """ui"""
        ...
    def __init__(self, *args: Unused) -> None: ...

@final
class PPD:
    """
    PPD file
    ========
      A PPD file.

    @type constraints: L{Constraint} list
    @ivar constraints: list of constraints
    @type attributes: L{Attribute} list
    @ivar attributes: list of attributes
    @type optionGroups: L{Group} list
    @ivar optionGroups: list of PPD option groups
    """
    @property
    def attributes(self) -> list[Attribute]:
        """List of attributes"""
        ...
    @property
    def constraints(self) -> list[Constraint]:
        """List of constraints"""
        ...
    @property
    def optionGroups(self) -> list[Group]:
        """List of PPD option groups"""
        ...
    def __init__(self, filename: str, /) -> None: ...
    def conflicts(self) -> int:
        """
        conflicts() -> integer

        @return: number of conflicts.
        """
        ...
    def emit(self, file: _FileOrFd, section: int, /) -> None:
        """
        emit(file, section) -> None

        Output marked options for section to a file.
        @type file: file
        @param file: file object
        @type section: integer
        @param section: section id
        """
        ...
    def emitAfterOrder(self, file: _FileOrFd, section: int, limit: int, min_order: float, /) -> None:
        """
        emitAfterOrder(file, section, limit, min_order) -> None

        Output marked options for section to a file.
        @type file: file
        @param file: file object
        @type section: integer
        @param section: section id
        @type limit: integer
        @param limit: non-zero to use min_order
        @type min_order: float
        @param min_order: minimum order dependency
        """
        ...
    def emitFd(self, fd: int, section: int, /) -> None:
        """
        emitFd(fd, section) -> None

        Output marked options for section to a file descriptor.
        @type fd: integer
        @param fd: file descriptor
        @type section: integer
        @param section: section id
        """
        ...
    def emitJCL(self, file: _FileOrFd, job_id: int, user: str, title: str, /) -> None:
        """
        emitJCL(file, job_id, user, title) -> None

        Emit code for JCL options to a file.
        @type file: file object
        @param file: file
        @type job_id: integer
        @param job_id: job id
        @type user: string
        @param user: user name on job
        @type title: string
        @param title: title of job
        """
        ...
    def emitJCLEnd(self, file: _FileOrFd, /) -> None:
        """
        emitJCLEnd(file) -> None

        Emit JCLEnd code to a file.
        @type file: file object
        @param file: file
        """
        ...
    def emitString(self, section: int, min_order: float, /) -> str:
        """
        emitString(section, min_order) -> string

        Return a string with the marked options for section, with at least min_order order dependency.
        @type section: integer
        @param section: section id
        @type min_order: float
        @param min_order: minimum order dependency
        @return: string containing emitted postscript
        """
        ...
    def findAttr(self, name: str, spec: str = ...) -> Attribute | None:
        """
        findAttr(name)

        @type name: string
        @param name: attribute name
        @type spec: string
        @keyword spec: specifier string (optional)
        @rtype: L{Attribute} or None
        @return: matching attribute, or None if not found.
        """
        ...
    def findNextAttr(self, name: str, spec: str = ...) -> Attribute | None:
        """
        findNextAttr(name)

        @type name: string
        @param name: attribute name
        @type spec: string
        @keyword spec: specifier string (optional)
        @rtype: L{Attribute} or None
        @return: next matching attribute, or None if not found.
        """
        ...
    def findOption(self, name: str, /) -> Option | None:
        """
        findOption(name)

        @type name: string
        @param name: option keyword
        @rtype: L{Option} or None
        @return: named option, or None if not found.
        """
        ...
    def localize(self) -> None:
        """
        localize() -> None

        Localize PPD to the current locale.
        """
        ...
    def localizeIPPReason(self, reason: str, scheme: str = ...) -> str | None:
        """
        localizeIPPReason(reason, scheme) -> string or None

        Localize IPP reason to the current locale.
        """
        ...
    def localizeMarkerName(self, name: str, /) -> str | None:
        """
        localizeMarkerName(name) -> string or None

        Localize marker name to the current locale.
        """
        ...
    def markDefaults(self) -> None:
        """
        markDefaults() -> None

        Set (mark) all options to their default choices.
        """
        ...
    def markOption(self, option: str, choice: str, /) -> int:
        """
        markOption(option, choice) -> integer

        Set an option to a particular choice.

        @type option: string
        @param option: option keyword
        @type choice: string
        @param choice: option choice
        @return: number of conflicts
        """
        ...
    def nondefaultsMarked(self) -> bool:
        """
        nondefaultsMarked() -> boolean

        Returns true if any non-default option choices are marked.
        """
        ...
    def writeFd(self, fd: int, /) -> None:
        """
        writeFd(fd) -> None

        Write PPD file, with marked choices as defaults, to file
        descriptor.

        @type fd: integer
        @param fd: open file descriptor
        """
        ...

def connectDest(
    dest: Dest, cb: Callable[[_T, int, Dest], Literal[0, 1]], flags: int = 0, msec: int = -1, user_data: _T = ...
) -> tuple[Connection, str]:
    """
    connectDest(dest,cb,flags=0,msec=-1,user_data=None) -> (conn, resource)

    @type dest: Dest object
    @param dest: destination to connect to
    @type cb: callable
    @param cb: callback function, given user_data, dest flags, and dest.
    Should return 1 to continue enumeration and 0 to cancel.
    @type flags: integer
    @param flags: enumeration flags
    @type msec: integer
    @param msec: timeout, or -1 for no timeout
    @type user_data: object
    @param user_data: user data to pass to callback function
    @return: a 2-tuple of the Connection object and the HTTP resource.
    """
    ...
def enumDests(
    cb: Callable[[_T, int, Dest], Literal[0, 1]],
    flags: int = 0,
    msec: int = -1,
    type: int = 0,
    mask: int = 0,
    user_data: _T = ...,
) -> None:
    """
    enumDests(cb,flags=0,msec=-1,type=0,mask=0,user_data=None) -> None

    @type cb: callable
    @param cb: callback function, given user_data, dest flags, and dest.
    Should return 1 to continue enumeration and 0 to cancel.
    @type flags: integer
    @param flags: enumeration flags
    @type msec: integer
    @param msec: timeout, or -1 for no timeout
    @type type: integer
    @param type: bitmask of printer types to return
    @type mask: integer
    @param mask: bitmask of type bits to examine
    @type user_data: object
    @param user_data: user data to pass to callback function
    """
    ...
def getEncryption() -> int:
    """
    getEncryption() -> integer

    Get encryption policy.
    @see: L{setEncryption}
    """
    ...
def getPort() -> int:
    """
    getPort() -> integer

    @return: IPP port to connect to.
    """
    ...
def getServer() -> str:
    """
    getServer() -> string

    @return: server to connect to.
    """
    ...
def getUser() -> str:
    """
    getUser() -> string

    @return: user to connect as.
    """
    ...
def ippErrorString(status_code: int, /) -> str:
    """
    ippErrorString(statuscode) -> name

    @type statuscode: integer
    @param statuscode: IPP Request status code
    @return: a string describing the status code
    """
    ...
def ippOpString(op: int, /) -> str:
    """
    ippOpString(op) -> name

    @type op: integer
    @param op: IPP Request operation
    @return: a string representing the operation name
    """
    ...
def modelSort(s1: str, s2: str, /) -> Literal[-1, 0, 1]:
    """
    modelSort(s1,s2) -> integer

    Sort two model strings.

    @type s1: string
    @param s1: first string
    @type s2: string
    @param s2: second string
    @return: strcmp-style comparison result
    """
    ...
def ppdSetConformance(level: int, /) -> None:
    """
    ppdSetConformance(level) -> None

    Set PPD conformance level.

    @type level: integer
    @param level: PPD_CONFORM_RELAXED or PPD_CONFORM_STRICT
    """
    ...
def require(version: str, /) -> None:
    """
    require(version) -> None

    Require pycups version.

    @type version: string
    @param version: minimum pycups version required
    @raise RuntimeError: requirement not met
    """
    ...
def setEncryption(policy: int, /) -> None:
    """
    setEncryption(policy) -> None

    Set encryption policy.

    @type policy: integer
    @param policy: L{HTTP_ENCRYPT_ALWAYS}, L{HTTP_ENCRYPT_IF_REQUESTED}, 
    L{HTTP_ENCRYPT_NEVER}, or L{HTTP_ENCRYPT_REQUIRED}
    """
    ...
def setPasswordCB(fn: Callable[[str], str | None], /) -> None:
    """
    setPasswordCB(fn) -> None

    Set password callback function.  This Python function will be called 
    when a password is required.  It must take one string parameter 
    (the password prompt) and it must return a string (the password), or 
    None to abort the operation.

    @type fn: callable object
    @param fn: callback function
    """
    ...

@overload
def setPasswordCB2(fn: Callable[[str, Connection, str, str], str | None] | None, /) -> None:
    """
    setPasswordCB2(fn, context=None) -> None

    Set password callback function.  This Python function will be called 
    when a password is required.  It must take parameters of type string 
    (the password prompt), instance (the cups.Connection), string (the 
    HTTP method), string (the HTTP resource) and, optionally, the user-
    supplied context.  It must return a string (the password), or None 
    to abort the operation.

    @type fn: callable object, or None for default handler
    @param fn: callback function
    """
    ...
@overload
def setPasswordCB2(fn: Callable[[str, Connection, str, str, _T], str | None], context: _T = ..., /) -> None:
    """
    setPasswordCB2(fn, context=None) -> None

    Set password callback function.  This Python function will be called 
    when a password is required.  It must take parameters of type string 
    (the password prompt), instance (the cups.Connection), string (the 
    HTTP method), string (the HTTP resource) and, optionally, the user-
    supplied context.  It must return a string (the password), or None 
    to abort the operation.

    @type fn: callable object, or None for default handler
    @param fn: callback function
    """
    ...

def setPort(port: int, /) -> None:
    """
    setPort(port) -> None

    Set IPP port to connect to.

    @type port: integer
    @param port: IPP port
    """
    ...
def setServer(server: str, /) -> None:
    """
    setServer(server) -> None

    Set server to connect to.

    @type server: string
    @param server: server hostname
    """
    ...
def setUser(user: str, /) -> None:
    """
    setUser(user) -> None

    Set user to connect as.

    @type user: string
    @param user: username
    """
    ...
