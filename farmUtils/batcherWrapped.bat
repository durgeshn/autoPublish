@echo off
set "pyFile=%~dp0autoPublishOnFarmNew.py"

mountvol I: /D
net use I: /DELETE
net use I: \\stor\py /PERSISTENT:YES
cd I:\
I:
I:\Python27\python.exe %pyFile% %1 %2 %3
cd D:\
D:
mountvol I: /D
net use I: /DELETE