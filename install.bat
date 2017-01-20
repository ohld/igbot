TITLE instabot install
CLS
@ECHO OFF

path c:\Program Files\Git\cmd;%PATH%
path C:\Python27;%PATH%
path C:\Python27\Scripts;%PATH%

pip install instabot
pip install -r requirements.txt
print "Congradulations You now install with requiments and instabot"
pause 