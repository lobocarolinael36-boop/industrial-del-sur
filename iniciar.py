import subprocess, sys, os
subprocess.Popen([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "menu.py")])
