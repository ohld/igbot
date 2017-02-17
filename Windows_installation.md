# How to install and run the script on Windows?

 * Make sure that you have python installed. [Here](https://www.howtogeek.com/197947/how-to-install-python-on-windows/) is a quite good tutorial.
 * Install `setuptools` if not installed yet
 ``` bash
 curl https://bootstrap.pypa.io/ez_setup.py | python
 ```
 * Install `pip` if not installed yet
 ``` bash
 curl https://bootstrap.pypa.io/get-pip.py | python
 ```
 * Unarchive and go to examples folder.
 * Press right click mouse and **Open command window**.
 * Print
 ```
pip install -U instabot
 ```
 * Download the repository:
```
git clone https://github.com/ohld/instabot
```
 or download a zip file with the Instabot [from the main page](https://github.com/ohld/instabot).

* Move to the examples folder
```
cd instabot\examples
```
* Run any example you wish with *python*. For example:
```
python follow_user_followers.py 352300017
```
