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

Ci sono parametri all'interno di `instabot.Bot ()`. Se lanci __multi_script_CLI__ , aperto con un editor di testo, puoi trovare  il parametro __unfollow_delay = 30__ qui, cambialo con ciò che preferisci. Similmente, puoi cambiare altri parametri nello stesso modo. Ma attenzione, potrebbe essere pericoloso.

Sarai d'accordo con me che se fai partire degli un-follow da 100 persone al secondo, sarai sicuramente bannato. I limiti dipendono dall'età e dalla dimensione dell'account, per cui il loro setup  è l'attività di tutti. I valori dati come impostazione predefinita in Instabot sono sicuri per _la maggior parte degli account_. Nessuno è stato bannato a causa di questi settaggi di default.

### Vorrei che il bot smettesse di seguire le persone che non mi seguono.

Per questo compito, abbiamo già preparato uno script, che trovi nella cartella ***examples***: __unfollow_non_followers.py__ è perfetto. 
Basta andare alla cartella con lo script sul proprio computer ed eseguire nel terminale.

``` python
python unfollow_non_followers.py
```

### Vorrei che il bot metta like ai post che contengono un hashtag 

Ancora molto semplice: esegui lo script like_hashtags.py, come questo:

``` python
python like_hashtags.py dog cat
```

### Troppi Script! Ce n'è uno che possa riordinarli tutti?

Eccolo. Grazie agli sforzi della community, è stato scritto uno script molto figo. Puoi trovarlo sotto il nome di [multi_script_CLI.py](/examples/multi_script_CLI.py). Scritto in inglese, ma penso che sia molto chiaro. Prova ad usarlo! 

### Come posso organizzare l'autoposting di immagini su Instagram?

Per questo, abbiamo una soluzione nella cartella [examples](/examples/autopost). In fondo alla pagina trovi alcune info su come configurare l'autoposting

### L'AutoPost pubblica solo la foto o anche descrizione e hashtag?

Gli hashtag sono gestiti come le descrizioni.

### Posso pubblicare i video in AutoPost?

Purtroppo no. Questo renderebbe molto complicato il progetto.

### Come posso aiutare il progetto?

Puoi aiutare in questi modi:
* Metti una stella al prgetto in Github qui: https://github.com/instagrambot (in alto a destra). Potresti doverti registrare (gratuitamente)
* Entra nel [Gruppo Telegram](https://t.me/instabotproject) e aiuta i nuovi arrivati a capire l'installazione,e la configurazione di Instabot. 
* Racconta del progetto non appena possibile. è sufficiente diffondere il link: https://instagrambot.github.io.
* Puoi segnalare bugs ed errori nella sezione [Issues](https://github.com/instagrambot/instabot/issues), assicurati di allegare _screenshots_ e _comandi_ che hai inserito. Questo ci aiuterà a correggere questi errori e rendere migliore Instabot
* Correggi questi errori se sei uno sviluppatore. Fallo attraverso delle Pull request, seguendo lo standard PEP8.
* Per sviluppare il nostro [sito](https://github.com/instagrambot/instagrambot.github.io). Abbiamo bisgno sia di designer sia di sviluppatori frontend. Se hai sempre desiderato creare qualcosa dal nulla, contattaci!
