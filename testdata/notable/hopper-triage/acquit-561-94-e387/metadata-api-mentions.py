import os
# API declarations, quoted examples and member references do not call APIs.
api_names = ['GetNamedSecurityInfoW', 'SetNamedSecurityInfoW', 'SetFileTime']
setter = os.setxattr
kernel.SetFileTime.argtypes = []
example = 'os.fchown(fd, uid, gid); os.removexattr(fd, name)'
