#!@@PYTHONEXE@@
# EASY-INSTALL-ENTRY-SCRIPT: 'RunSnakeRun==2.0.4','gui_scripts','runsnake'
__requires__ = 'RunSnakeRun==2.0.4'
import sys
from pkg_resources import load_entry_point

sys.exit(
   load_entry_point('RunSnakeRun==2.0.4', 'gui_scripts', 'runsnake')()
)
