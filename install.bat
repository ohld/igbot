TITLE instabot install
CLS
@ECHO OFF

path c:\Program Files\Git\cmd;%PATH%
path C:\Python27;%PATH%
path C:\Python27\Scripts;%PATH%

 pip install -r requirements.txt
 print "Please close this window requirements are now installed"
 pause 