## Documentazione

### Bot Class

``` python
from instabot import Bot
bot = Bot(
            proxy=None,
            max_likes_per_day=1000,
            max_unlikes_per_day=1000,
            max_follows_per_day=350,
            max_unfollows_per_day=350,
            max_comments_per_day=100,
            max_likes_to_like=100,
            filter_users=True,
            max_followers_to_follow=2000,
            min_followers_to_follow=10,
            max_following_to_follow=7500,
            min_following_to_follow=10,
            max_followers_to_following_ratio=10,
            max_following_to_followers_ratio=2,
            max_following_to_block=2000,
            min_media_count_to_follow=3,
            like_delay=10,
            unlike_delay=10,
            follow_delay=30,
            unfollow_delay=30,
            comment_delay=60,
            whitelist=False,
            blacklist=False,
            comments_file=False,
            stop_words=['shop', 'store', 'free']
)
```

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

In tutti i file:

*prima riga - un oggetto*

*seconda riga - un oggetto*

Ad esempio, il file comments.txt
``` python
wow! 
Bellissima immagine!
Era da tanto tempo che non vedevo un profilo così!
```

Questo vale sia per i commenti, che per le liste di hashtag ed utenti nei vari file .txt

### Get

| method        | descrizione | esempio  |
| ------------- |:-------------:| ------:|
| get_your_medias | Ottiene una lista dei tui media | bot.get_you_medias()|
| get_timeline_medias | Ottiene una lista dei media_ids dal feed della tua timeline | bot.get_timeline_medias()|
| get_user_medias | Ottiene una lista dei media di un dato utente | bot.get_user_medias("ohld")|
| get_hashtag_medias| Ottiene una lista dei media in base all'hashtag | bot.get_hashtag_medias("Dog")|
| get_geotag_medias| Ottiene una lista dei media in base al geotag| TODO |
| get_timeline_users| Ottiene una lista di utenti in base al feed della tua timeline | bot.get_timeline_users()|
| get_hashtag_users| Ottiene una lista di utenti in base all'hashtag| bot.get_hashtag_users("Dog") |
| get_geotag_users| Ottiene una lista di utenti in base al geotag| TODO |
| get_userid_from_username| Converte username nell'user_id| bot.get_userid_from_username("ohld") |
| get_user_followers| Ottiene una lista di utenti che seguono un utente | bot.get_user_followers("competitor") |
| get_user_following| Ottiene una lista di utenti seguiti da un dato utente | bot.get_user_following("competitor") |
| get_media_likers | Ottiene una lista di utenti a cui piace un media | bot.get_media_likers("12312412") |
| get_media_comments | Ottiene una lista di commenti sotto un media | bot.get_media_comments("12312412") |
| get_comment | Ottiene una lista di commenti da un file | bot.get_comment()|
| get_media_commenters| Ottiene una lista di utenti che hanno commentato sotto un media | bot.get_media_commenters("12321")|


### Like

| method        | descrizione | esempio  |
| ------------- |:-------------:| ------:|
| like | Mette like ad un media | bot.like("1231241210")|
| like_medias | Mette like ad un media presente in una lista | bot.like_medias(["1323124", "123141245"])|
| like_timeline | Mette like ai media della timeline | bot.like_timeline()|
| like_user | Mette like agli ultimi media dell'utente | bot.like_user("activefollower")|
| like_hashtag | Mette like agli ultimi media in base all'hashtag | bot.like_hashtag("dog")|
| like_geotag | Mette like agli ultimi media in base al geotag |TODO|

### Unlike

| method        | descrizione | esempio  |
| ------------- |:-------------:| ------:|
| unlike | Toglie il like da un media | bot.unlike("12321412512")|
| unlike_medias | Toglie il like da un media presente nella lista | bot.unlike_medias(["123", "321"])|

### Follow

| method        | descrizione | esempio  |
| ------------- |:-------------:| ------:|
| follow | Segui utenti | bot.follow("activefollower")|
| follow_users | Segui utenti dalla lista | bot.follow(["activefollower1", "activefollower2"])|

### Unfollow

| method        | descrizione | esempio  |
| ------------- |:-------------:| ------:|
| unfollow | Smetti di seguire gli utenti | bot.unfollow("competitor")|
| unfollow_users | Smetti di seguire gli utenti dalla lista | bot.unfollow(["competitor1", "competitor2"])|
| unfollow_non_followers | Smetti di seguire gli utenti che non ti seguono | bot.unfollow_non_followers()|

### Commenti

| method        | descrizione | esempio  |
| ------------- |:-------------:| ------:|
| comment | Metti un commento sotto il media | bot.comment("1231234", "Nice pic!")|
| comment_medias | Metti un commento sotto il media nella lista | bot.comment_medias(["123", "321"])|
| comment_hashtag | Metti un commento sotto il media contenente l'hashtag | bot.comment_hashtag("Dog")|
| comment_geotag | Metti un commento sotto il media geolocalizzato | TODO |
| comment_users | Metti un commento sotto gli ultimi media degli utenti | bot.comment_users(["activefollower1", "activefollower2"]) |
| is_commented | Controlla il media se ha già commentati | bot.is_commented("123321") |
