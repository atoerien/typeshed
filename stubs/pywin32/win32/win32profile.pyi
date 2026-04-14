"""Interface to the User Profile Api."""

import _win32typing

def CreateEnvironmentBlock(Token: int, Inherit):
    """Retrieves environment variables for a user"""
    ...
def DeleteProfile(SidString: str, ProfilePath: str | None = ..., ComputerName: str | None = ...) -> None:
    """Remove a user's profile"""
    ...
def ExpandEnvironmentStringsForUser(Token: int, Src: str) -> str:
    """Replaces environment variables in a string with per-user values"""
    ...
def GetAllUsersProfileDirectory() -> str:
    """Retrieve All Users profile directory"""
    ...
def GetDefaultUserProfileDirectory() -> str:
    """Retrieve profile path for Default user"""
    ...
def GetEnvironmentStrings():
    """Retrieves environment variables for current process"""
    ...
def GetProfilesDirectory() -> str:
    """Retrieves directory where user profiles are stored"""
    ...
def GetProfileType():
    """Returns type of current user's profile"""
    ...
def GetUserProfileDirectory(Token: int) -> str:
    """Returns profile directory for a logon token"""
    ...
def LoadUserProfile(hToken: int, ProfileInfo: _win32typing.PyPROFILEINFO) -> _win32typing.PyHKEY:
    """Load user settings for a login token"""
    ...
def UnloadUserProfile(Token: int, Profile: _win32typing.PyHKEY) -> None:
    """Unload profile loaded by LoadUserProfile"""
    ...

PI_APPLYPOLICY: int
PI_NOUI: int
PT_MANDATORY: int
PT_ROAMING: int
PT_TEMPORARY: int
