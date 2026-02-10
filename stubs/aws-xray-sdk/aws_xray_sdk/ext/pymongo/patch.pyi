class XrayCommandListener:
    """
    A listener that traces all pymongo db commands to AWS Xray.
    Creates a subsegment for each mongo db conmmand.

    name: 'mydb@127.0.0.1:27017'
    records all available information provided by pymongo,
    except for `command` and `reply`. They may contain business secrets.
    If you insist to record them, specify `record_full_documents=True`.
    """
    record_full_documents: bool
    def __init__(self, record_full_documents: bool) -> None: ...
    def started(self, event) -> None: ...
    def succeeded(self, event) -> None: ...
    def failed(self, event) -> None: ...

def patch(record_full_documents: bool = False) -> None: ...
