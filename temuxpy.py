import os 
import shutil 
import subprocess
serial = "127.0.0.1:5560"
adb = shutil.which('adb')
folder=os.sep.join(__file__.split(os.sep)[:-1])
allpythonfiles=[ os.path.join(folder,f) for f in os.listdir(folder) if f.endswith('.py') or f.endswith('.pyx') ]
subprocess.run([adb, "-s", serial, "shell"], input=b"mkdir /sdcard/tpy")
for f in allpythonfiles:
    subprocess.run([adb,'-s',serial, "push", f, "/sdcard/tpy"])
#subprocess.run([adb,'push','temux.py',folder])