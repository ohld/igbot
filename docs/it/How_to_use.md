# Istruzioni per l'uso del modulo Instabot

**Importante! Leggi le istruzioni dall'inizio alla fine, e poi passa all'utilizzo! Buona Fortuna!**

## Come farlo funzionare?

Avrai bisogno di un progetto scaricato. Nella cartella ***instabot/examples/*** ci sono script lavorabili.

## Come far funzionare il bot?

Apri la linea di comando, utilizza ***cd*** per navigare nella directory del progetto, solitamente ***instabot/examples***. 
Digita

``` python
python scriptscelto.py param
```

Dove ***scriptscelto*** è il nome dello script... scelto ;) , ***param*** è il parametro richiesto per weseguire lo script. Non tutti gli script necessitano di parametri.

## Come faccio a capire se lo script necessita di parametri?

Avvia lo script digitando

``` python
python scriptscelto.py
```

Se non ci sono parametri necessari, lo script si fermerà e mostrerà un errore.
Per esempio.
Avvia uno script.
Digita.

``` python
python like_hashtags.py. 
```

Lo script si fermerà e mostrerà un messaggio:

``` python
error: the following arguments are required: hashtags.
```

Eccolo, dovremo quindi inserire un hashtag. Esempio corretto. 

``` python
python like_hashtags.py follow
```

## Script Al Inclusive

***multi_script_CLI.py*** è uno script che contiene tutte le funzioni. LA prima volta che lo avvii, verrà richiesto di configurarlo. La configurazione viene salvata nel file ***setting.txt***. Anche questi file vengono creati: ***hashtag_file.txt, users_file.txt, whitelist.txt, blacklist.txt, comment.txt***.

## 24/7

Sì, c'è uno script che aumenta i follower e le persone che segui durantetutto l'arco della giornata, e può mettere like anche alle foto in base a nome profilo e hashtag. queste sono solo alcune delle funzionalità dello script - *** ultimate.py ***, che trovi nella cartella *** instabot / examples / ultimate ***. La cartella contiene anche altri file di testo per eseguire lo script. In questi file, ogni nuovo parametro deve essere scritto da una nuova linea.

## Schedule

C'è un secndo script che può lavorare per tutta la giornata, MA questo script agirà secondo un piano. questo script è ***ultimate.py*** che trovi nella cartella ***instabot/examples/ultimate_schedule***. Puoi aprire il codice con un editor di testo e programmare il tutto. Dovrebbe essere molto semplice, perchè il codice è molto ben commentato.

## Come configurare correttamente lo script

Per garantire che il tuo account non venga bannato, devi configurare lo script example. Supponiamo che dobbiamo monitorare le foto con un determinato hashtag ogni minuto. Prima di tutto, indichiamo il tempo in secondi. Apri *** like_hashtags.py *** con un editor di testo. Trova queste linee (più o meno dovrebbero essere come queste).

``` python
bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)
```
E nelle linee successive

``` python
bot = Bot()
```

Dobbiamo scrivere un parametro nelle parentesi. Questo parametro è ***like_delay***. Questo parametro deve essere settato a 60, siccome abbiamo bisogno che il bot metta like alle foto con un determinato hashtag. Alla fine, dovrebbe risultare qualcosa di simile. 

``` python
bot = Bot(like_delay=60)
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)
```

## Lista dei Parametri

| parametro| descrizione | esempio |
| ------------- |:-------------:| ------:|
| proxy | Proxy per Instabot | None|
| max_likes_per_day| Quanti like il bot invierà al giorno| 1000|
| max_unlikes_per_day | A quanti media il bot toglierà il like al giorno| 1000|
| max_follows_per_day| Massimo numero di persone seguite al giorno| 350|
| max_unfollows_per_day| Massimo numero di unfollow al giorno| 350|
| max_comments_per_day| Massimo numero di commenti al giorno| 100|
| max_likes_to_like| Se il media ha più like di questo valore, - viene ignorato e non viene messo like | 200|
| filter_users | Filtra gli utenti se True | True|
| max_followers_to_follow| Se l'utente ha più followers di questo valore - l'utente non verrà nè seguito nè verrà messo like | 2000|
| min_followers_to_follow| Se l'utente ha meno followers di questo valore - l'utente non verrà nè seguito nè verrà messo like| 10|
| max_following_to_follow| Se l'utente segue più utenti di questo valore - l'utente non verrà nè seguito nè verrà messo like| 10000|
| min_following_to_follow| Se l'utente segue meno utenti di questo valore - l'utente non verrà nè seguito nè verrà messo like| 10|
| max_followers_to_following_ratio| Se il rapporto tra followers/persone seguite dall'utente è più grande di questo valore - l'utente non verrà nè seguito nè verrà messo like| 10|
| max_following_to_followers_ratio| Se il rapporto tra persone seguite/followers dall'utente è più grande di questo valore - he will not be followed or liked.| 2|
| min_media_count_to_follow| Se l'utente ha meno media di questo valore - l'utente non verrà seguito | 3|
| max_likes_to_like | Max number of likes that can media have to be liked | 100 |
|max_following_to_block|Se l'utente segue più persone di questo valore - l'utente verrà bloccato attraverso gli script di blocco, perchè è un massfollower | 2000|
| like_delay | Ritardo tra i like, in secondi| 10|
| unlike_delay | Ritardo tra gli un-like, in secondi | 10|
| follow_delay | Ritardo tra i follow, in secondi | 30|
| unfollow_delay | Ritardo tra gli un-follow, in secondi | 30|
| comment_delay | Ritardo tra i commenti, in secondi |  60|
| whitelist | Indirizzo della "lista bianca" degli utenti che non si smetterà di seguire | "whitelist.txt"|
| blacklist | Indirizzo della "lista nera" degli utenti a cui non verrà messo follow, like o commento | "blacklist.txt"|
| comments_file | Indirizzo del file contenente i commenti | "comments.txt" |
| stop_words| Una lista di Stop Words: non seguire un utente se ha almeno una di queste parole in descrizione| ['shop', 'store', 'free']|
