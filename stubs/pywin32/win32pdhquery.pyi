r"""
Performance Data Helper (PDH) Query Classes

Wrapper classes for end-users and high-level access to the PDH query
mechanisms.  PDH is a win32-specific mechanism for accessing the
performance data made available by the system.  The Python for Windows
PDH module does not implement the "Registry" interface, implementing
the more straightforward Query-based mechanism.

The basic idea of a PDH Query is an object which can query the system
about the status of any number of "counters."  The counters are paths
to a particular piece of performance data.  For instance, the path
'\Memory\Available Bytes' describes just about exactly what it says
it does, the amount of free memory on the default computer expressed
in Bytes.  These paths can be considerably more complex than this,
but part of the point of this wrapper module is to hide that
complexity from the end-user/programmer.

EXAMPLE: A more complex Path
    '\\RAISTLIN\PhysicalDisk(_Total)\Avg. Disk Bytes/Read'
    Raistlin --> Computer Name
    PhysicalDisk --> Object Name
    _Total --> The particular Instance (in this case, all instances, i.e. all drives)
    Avg. Disk Bytes/Read --> The piece of data being monitored.

EXAMPLE: Collecting Data with a Query
    As an example, the following code implements a logger which allows the
    user to choose what counters they would like to log, and logs those
    counters for 30 seconds, at two-second intervals.

    query = Query()
    query.addcounterbybrowsing()
    query.collectdatafor(30,2)

    The data is now stored in a list of lists as:
    query.curresults

    The counters(paths) which were used to collect the data are:
    query.curpaths

    You can use the win32pdh.ParseCounterPath(path) utility function
    to turn the paths into more easily read values for your task, or
    write the data to a file, or do whatever you want with it.

OTHER NOTABLE METHODS:
    query.collectdatawhile(period) # start a logging thread for collecting data
    query.collectdatawhile_stop() # signal the logging thread to stop logging
    query.collectdata() # run the query only once
    query.addperfcounter(object, counter, machine=None) # add a standard performance counter
    query.addinstcounter(object, counter,machine=None,objtype = 'Process',volatile=1,format = win32pdh.PDH_FMT_LONG) # add a possibly volatile counter

### Known bugs and limitations ###
Due to a problem with threading under the PythonWin interpreter, there
will be no data logged if the PythonWin window is not the foreground
application.  Workaround: scripts using threading should be run in the
python.exe interpreter.

The volatile-counter handlers are possibly buggy, they haven't been
tested to any extent.  The wrapper Query makes it safe to pass invalid
paths (a -1 will be returned, or the Query will be totally ignored,
depending on the missing element), so you should be able to work around
the error by including all possible paths and filtering out the -1's.

There is no way I know of to stop a thread which is currently sleeping,
so you have to wait until the thread in collectdatawhile is activated
again.  This might become a problem in situations where the collection
period is multiple minutes (or hours, or whatever).

Should make the win32pdh.ParseCounter function available to the Query
classes as a method or something similar, so that it can be accessed
by programmes that have just picked up an instance from somewhere.

Should explicitly mention where QueryErrors can be raised, and create a
full test set to see if there are any uncaught win32api.error's still
hanging around.

When using the python.exe interpreter, the addcounterbybrowsing-
generated browser window is often hidden behind other windows.  No known
workaround other than Alt-tabing to reach the browser window.

### Other References ###
The win32pdhutil module (which should be in the %pythonroot%/win32/lib
directory) provides quick-and-dirty utilities for one-off access to
variables from the PDH.  Almost everything in that module can be done
with a Query object, but it provides task-oriented functions for a
number of common one-off tasks.

If you can access the MS Developers Network Library, you can find
information about the PDH API as MS describes it.  For a background article,
try:
https://web.archive.org/web/20040926110045/http://msdn.microsoft.com:80/library/en-us/dnperfmo/html/msdn_pdhlib.asp

The reference guide for the PDH API was last spotted at:
https://learn.microsoft.com/en-us/windows/win32/perfctrs/using-the-pdh-functions-to-consume-counter-data


In general the Python version of the API is just a wrapper around the
Query-based version of this API (as far as I can see), so you can learn what
you need to from there.  From what I understand, the MSDN Online
resources are available for the price of signing up for them.  I can't
guarantee how long that's supposed to last. (Or anything for that
matter).
http://premium.microsoft.com/isapi/devonly/prodinfo/msdnprod/msdnlib.idc?theURL=/msdn/library/sdkdoc/perfdata_4982.htm

The eventual plan is for my (Mike Fletcher's) Starship account to include
a section on NT Administration, and the Query is the first project
in this plan.  There should be an article describing the creation of
a simple logger there, but the example above is 90% of the work of
that project, so don't sweat it if you don't find anything there.
(currently the account hasn't been set up).
https://web.archive.org/web/19980422204546/http://starship.skyport.net/crew/mcfletch/

If you need to contact me immediately, (why I can't imagine), you can
email me at mcfletch@golden.net, or just post your question to the
Python newsgroup with a catchy subject line.
news:comp.lang.python

### Other Stuff ###
The Query classes are by Mike Fletcher, with the working code
being corruptions of Mark Hammonds win32pdhutil module.

Use at your own risk, no warranties, no guarantees, no assurances,
if you use it, you accept the risk of using it, etceteras.
"""

from win32.lib.win32pdhquery import *
