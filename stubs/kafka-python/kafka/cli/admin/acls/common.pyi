from argparse import ArgumentParser, Namespace

from kafka.admin._acls import ACL, ACLFilter

def add_acl_filter_args(parser: ArgumentParser) -> None:
    """Add arguments for building an ACLFilter (used by describe and delete)."""
    ...
def add_acl_args(parser: ArgumentParser, required: bool = False) -> None:
    """Add arguments for building a concrete ACL (used by create)."""
    ...
def acl_filter_from_args(args: Namespace) -> ACLFilter:
    """Build an ACLFilter from parsed CLI arguments."""
    ...
def acl_from_args(args: Namespace) -> ACL:
    """Build an ACL from parsed CLI arguments."""
    ...
