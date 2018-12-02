#!C:\Users\Alex\Documents\GitHub\YHack-Project-2018\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'populartimes==2.0','console_scripts','populartimes'
__requires__ = 'populartimes==2.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('populartimes==2.0', 'console_scripts', 'populartimes')()
    )
