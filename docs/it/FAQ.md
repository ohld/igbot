# Domande frequenti su Instabot.

### Come installo il bot?

L'installazione dipende dal tuo sistema operativo. [Installazione per Windows](/docs/it/Installation_on_Windows.md). [Installazione su Unix](/docs/it/Installation_on_Unix.md) (Linux, MacOS).

Tutto il lavoro del bot viene gestito dalla riga di comando (terminal / CMD). Non ti spaventare, non c'è nulla di complicato.

### Come faccio partire il bot?

Per prima cosa devi installarlo. Poi naviga nella cartella "examples" e lancia uno qualsiasi degli script con la liena di comando, per esempio:


``` python
python multi_script_CLI.py
```

Se lo script necessita che siano passati dei parametri per funzionare, per esempio, una lista di hashtag per mettere "mi piace", allora lo script te lo mostrerà. Nell'esempio, lo script like_hahstag.py, mostrerà a schermo: 
```
Usage: Pass hashtags to like
Example: python like_hashtags.py dog cat
```

Diventa quindi molto intuitivo come lavorare con questo script. Per esempio, se vuoi mettere like agli ultimi media pubblicati con l'hashtag **#cat** or **#dog**, allora scrivi nel terminale:
``` python
python like_hashtags.py cat dog
```

### Dove inserisco Password e Username del mio account Instagram?

Non vengono specificati per nulla: Il bot stesso li chiederà la prima volta che viene avviato. Verranno poi salvati nel file secret.txt
e verranno quindi recuperati facilmente dal file. Puoi anche passarli allo script manualmente, alla funzione login():
``` python
bot.login(username=«my_username», password=«my_password»)
```

Inoltre, quando avvii lo script per la prima volta, potrai aggiungere diversi account ad Instabot. Nei futuri accessi, se specifichi più di un account, prima di ogni avvio, avrai la possibilità di scegliere l'account con cui lavorare.

### Quando inserisco la password, non si vede! Che posso fare?

La password non viene mostrata in modo che non possa essere rubata da qualcuno che ti spia alle spalle. Non ti preoccupare, è stata inserita correttamente. Se accidentalmente hai inserito la password errata, la prossima volta che esegui lo script, se la password non è corretta, ti verrà chiesto di inserire di nuovo.

### Quando inserisco login e password per il mio account Instagram, dove vanno a finire? Sono trasmesse a qualche host remoto?

Login e password vengono salvati in locale nel file secret.txt. Non vengono trasmessi da nessuna parte.

### Il mio account è a rischio di essere banato?

Instabot ha limiti sia sul numero di follow / like / commenti e così via su base giornaliera, sia sulla frequenza delle richieste - per esempio, non seguire persone troppo rapidamente. Instabot ha già dei suoi limiti, che garantiscono un utilizzo sicuro. È possibile impostare i propri valori, ma fai attenzione. 
Ulteriori dettagli su questo possono essere letti qui (TODO --> fare una pagina con una descrizione di questi parametri e come modificare). Il bot salva il numero di like / follow / unfollow e così via. E li azzera una volta al giorno.

### Esiste la possibilità di accelerare il processo, una volta per tutte? Rimane un approccio sicuro?

Ci sono parametri all'interno di `instabot.Bot ()`. Se lanci __milti_script_CLI__ , aperto con un editor di testo, puoi trovare  il parametro __unfollow_delay = 30__ qui, cambialo con ciò che preferisci. Similmente, puoi cambiare altri parametri nello stesso modo. Ma attenzione, potrebbe essere pericoloso.

Sarai d'accordo con me che se fai partire degli un-follow da 100 persone al secondo, sarai sicuramente bannato. I limiti dipendono dall'età e dalla dimensione dell'account, per cui il loro setup  è l'attività di tutti. I valori dati come impostazione predefinita in Instabot sono sicuri per _la maggior parte degli account_. Nessuno è stato bannato a causa di questi settaggi di default.

### I want the bot to unsubscribe from accounts that did not respond with a mutual subscription.

For your task, the already written script, which lies in the examples folder: unfollow_non_followes.py, is suitable. Просто перейдите папку с этим скриптом на вашем компьютере и выполните в терминале. 
``` python
python unfollow_non_followers.py
```

### I want the bot to put the likes of posts with hashtags, which I will list.

Everything again is very simple! Run the example like_hashtags.py, for example, like this:
``` python
python like_hashtags.py dog cat
```

### Too many scripts! Is there anything in one bottle?

There is. Thanks to the efforts of our community, a very cool script was written. You can find it under the name [multi_script_CLI.py](/examples/multi_script_CLI.py). He is in English, but I think everything will be clear. I strongly advise you to try it!

### How can I organize an auto-posting photo in the Instagram?

For this, we have a daddy in [examples](/examples/autopost). Below on that page you will find how to configure and run auto-hosting.

### AutoPost publishes only a photo or description and a hashtag, too?

Hashtags is the same description - just add them there.

### Can I publish video via autoposting?

Unfortunately no. This would increase the size of the project several times.

### How can I help the project?

Вы можете:
* Put the star in Github. To do this, just click on the star here https://github.com/instagrambot (top right), May need to register (for free).
* Login to [Telegram Group](https://t.me/instabotproject) and help newcomers to understand the installation and configuration of Instabot. 
* Tell us about our project wherever possible. It will be enough to throw off the link: https://instagrambot.github.io.
* You can find bugs and errors found in [Issues](https://github.com/instagrambot/instabot/issues), be sure to attach the _screenshots_ and _commands_ that you entered. This will help correct these errors and make Instabot better!
* Correct these errors if you are a developer. Do this through the Pull request, following the standard PEP8.
* To develop our [site](https://github.com/instagrambot/instagrambot.github.io). We need both a designer and a frontend developer. If you have long wanted to do something from scratch, welcome.
