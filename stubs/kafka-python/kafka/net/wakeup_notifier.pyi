class WakeupNotifier:
    """
    await wakeup(timeout_secs) when either ``timeout_secs`` elapses or
    notify() is called -- whichever first. The notifier is safe to call
    from any thread (it routes through call_soon_threadsafe).

    Level-triggered: notify() arriving while no one is awaiting is latched
    and consumed by the next ``__call__``. This closes a lost-wakeup race
    where a caller's state mutation (e.g. ``cluster._need_update = True``)
    and its ``notify()`` happen between another task's pre-await state
    check and its ``await self._wakeup(...)``. Without latching, the
    notification arrives at the IO thread before the task has registered
    a future to signal, and the task would sleep for the full timeout
    despite work being ready.

    Used by the metadata refresh loop to sleep on its TTL while remaining
    interruptible by external callers (e.g. KafkaProducer / KafkaConsumer
    invoking cluster.request_update() from another thread).
    """
    def __init__(self, net) -> None: ...
    async def __call__(self, timeout_secs=None) -> None: ...
    def notify(self) -> None: ...
