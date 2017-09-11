# Come installare e lanciare lo script su UNIX? (Linux, macOS)
* Apri il terminale e digita:
```
pip install -U instabot
git clone https://github.com/instagrambot/instabot
cd instabot/examples
```

* Successivamente puoi avviare uno script di prova come questo.
```
python multi_script_CLI.py
```

## Errori

* Se hai questo errore `pip: command not found` error, prova:
```
sudo easy_install pip
```

* Se hai questo errore `permission denied` dopo `pip install -U instabot`, prova:
```
sudo pip install -U instabot
```
