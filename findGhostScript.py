import _winreg

program_to_found = 'Software\\GPL Ghostscript'

try:
   h_key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, program_to_found)
   try:
       gs_version = _winreg.EnumKey(h_key, 0)
       h_subkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, program_to_found+'\\'+gs_version)
       gs_dll = (_winreg.EnumValue(h_subkey,0))[1]
       print("Ghostscript %s is installed in: %s" % (gs_version, gs_dll.replace('gsdll32.dll', '')))
   except OSError:
       print("Ghostscript insn't correctly installed!! ")
except IOError:
   print("Ghostsript not found!! ")
