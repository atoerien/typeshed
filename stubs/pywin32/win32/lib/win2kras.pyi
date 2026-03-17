"""
win2kras used to be an extension module with wrapped the "new" RAS functions in Windows 2000, so win32ras could still be used on NT/etc.
I think in 2021 we can be confident pywin32 is not used on earlier OSs, so that functionality is now in win32ras.

This exists just to avoid breaking old scripts.
"""

RASEAPF_Logon: int
RASEAPF_NonInteractive: int
RASEAPF_Preview: int

def GetEapUserIdentity(phoneBook: str | None, entry: str, flags: int, hwnd=None, /): ...

RASCS_AllDevicesConnected: int
RASCS_AuthAck: int
RASCS_AuthCallback: int
RASCS_AuthChangePassword: int
RASCS_AuthLinkSpeed: int
RASCS_AuthNotify: int
RASCS_AuthProject: int
RASCS_AuthRetry: int
RASCS_Authenticate: int
RASCS_Authenticated: int
RASCS_CallbackComplete: int
RASCS_CallbackSetByCaller: int
RASCS_ConnectDevice: int
RASCS_Connected: int
RASCS_DeviceConnected: int
RASCS_Disconnected: int
RASCS_Interactive: int
RASCS_LogonNetwork: int
RASCS_OpenPort: int
RASCS_PasswordExpired: int
RASCS_PortOpened: int
RASCS_PrepareForCallback: int
RASCS_Projected: int
RASCS_ReAuthenticate: int
RASCS_RetryAuthentication: int
RASCS_StartAuthentication: int
RASCS_WaitForCallback: int
RASCS_WaitForModemReset: int
