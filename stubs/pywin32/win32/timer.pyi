"""Extension that wraps Win32 Timer functions"""

from win32.lib.pywintypes import error as error

def set_timer(Elapse, TimerFunc, /):
    """
    int = set_timer(milliseconds, callback}
    Creates a timer that executes a callback function
    """
    ...
def kill_timer(timer_id, /):
    """
    boolean = kill_timer(timer_id)
    Stops a timer
    """
    ...

__version__: bytes
