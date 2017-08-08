# Come fa Instabot a filtrare i profili?

Non è un segreto che Instabot, prima di mettere follow a dei profili, li filtri in modo da non seguire account falsi o inattivi. Sotto, trovate l'intera lista di condizioni che Insabot applica nella sua opera di selezione.

## Opzioni

Per cominciare, vale la pena indicare le condizioni che sei libero di cambiare. Sotto, ti darò i parametri della funzione ccostruttrice del bot, che sono correlati con le operazioni di selezione. 

``` python
bot = Bot(max_likes_to_like=100,
          max_followers_to_follow=2000,
          min_followers_to_follow=10,
          max_following_to_follow=10000,
          min_following_to_follow=10,
          max_followers_to_following_ratio=10,
          max_following_to_followers_ratio=2,
          min_media_count_to_follow=3,
          stop_words=['shop', 'store', 'free'])
```
Se vuoi cambiare questi valori in qualcuno di tuo gradimento all'interno di qualche esempio, basta che sostituisci la linea `bot = Bot ()` con quella indicata qui sopra, ovviamente con i tuoi valori.
Qui sotto, invece, trovi i nomi di questi parametri, ed i valori relativi.

## Filtri per gli utenti

_Notation_: True - puoi seguire il profilo, False - non puoi.
* Se l'utente è in whitelist.txt - True,
* Se l'utente è in blacklist.txt - False,
* Se segui già il profilo - False,
* Se è un profilo Business - True,
* Se è un profilo verificato - True,
* Se il numero di follower è inferiore a min_followers_to_follow - False,
* Se il numero di follower è superiore a max_followers_to_follow - False,
* Se il numero di persone seguite è inferiore a min_following_to_follow - False,
* Se il numero di persone seguite è superiore a max_following_to_follow - False,
* Se il rapporto di  persone seguite / followers supera max_following_to_followers_ratio - False,
* Se il rapporto di follower / persone seguite supera max_followers_to_following_ratio - False,
* Se il numero di media è inferiore a min_media_count_to_follow - False,
* Se almeno una delle stop word viene trovato nello stato, nella buo, nel suo nome, o nelle descrizioni - False,
* Se non ancora filtrato - True.
