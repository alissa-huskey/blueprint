"""new-project -- create a new project."""

from enum import Enum
from pathlib import Path

from more_itertools import first

__version__ = "0.0.1"

ROOT = Path(__file__).parent.parent


class SysExit(Enum):
    """BSD Preferred exit codes."""

    GENERIC     = ( 1, "Error")
    USAGE       = (64, "Command line usage error")
    DATAERR     = (65, "User data format error")
    NOINPUT     = (66, "Cannot open user input file")
    NOHOST      = (68, "Host name unknown")
    UNAVAILABLE = (69, "Service unavailable")
    SOFTWARE    = (70, "Internal software error")
    OSERR       = (71, "OS error")
    OSFILE      = (72, "Critical OS file missing")
    CANTCREAT   = (73, "Can't create output file")
    IOERR       = (74, "Input/output error")
    TEMPFAIL    = (75, "Temp failure; user is invited to retry")
    PROTOCOL    = (76, "Remote error in protocol")
    NOPERM      = (77, "Permission denied")
    CONFIG      = (78, "Configuration error")

    def __init__(self, status, desc):
        """Set status, desc, and make enable lookup via status."""
        self.status, self.desc = status, desc
        self._value_ = self.status
        self._member_map_[status] = self

    def __int__(self):
        """Convert to int is status."""
        return self.status


class NewProjectError(BaseException):
    """Base class for project exceptions."""

    status: SysExit = SysExit.GENERIC

    @property
    def message(self):
        """Human readable exception message."""
        return first(self.args, self.default_message)

    @property
    def default_message(self):
        """Message from the exit code."""
        return self.status.desc


class UserError(NewProjectError):
    """Any kind of user error."""

    status: SysExit = SysExit.USAGE


class AccessError(UserError):
    """Unable to access something on the filesystem.

    Such as if the file/directory does not exist, already exists permission
    problems, etc. (Pretty much anything under the builtin OSError caused by
    the user.)
    """

    status: SysExit = SysExit.OSERR


class ProgramError(NewProjectError):
    """An error in the programs code code."""

    status: SysExit = SysExit.SOFTWARE

#  class SetupError(UserError): # for config/environment issues maybe?
