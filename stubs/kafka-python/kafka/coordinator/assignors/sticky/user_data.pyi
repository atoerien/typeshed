from kafka.protocol.api_data import ApiData

class StickyAssignorUserData(ApiData):
    """
    Notes from json schema:
      // StickyAssignor currently always encodes with version 1.
      // To decode, versions are attempted in reverse order until one succeeds.
      // If no decoding is possible, the assignor ignores the previous user data.

      // Version 1 added the "generation" field
    """
    def __init__(self, *args, **kw) -> None: ...
    # TODO: Reflect TopicPartition, generation, previous_assignment attributes
    def __getattr__(self, name: str): ...  # incomplete class
