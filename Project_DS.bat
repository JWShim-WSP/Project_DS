@ECHO OFF
cd D:\Django\BST-Project\Project_DS

call d:\django\BST-Project\Scripts\activate.bat

start "python.exe" "d:\django\BST-Project\scripts\python.exe" manage.py runserver 8001

start "msedge.exe" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" 127.0.0.1:8001


