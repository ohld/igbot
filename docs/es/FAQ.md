# Preguntas frecuentes en Instabot.

### ¿Como instalo el bot?

La instalacion en sí depende del sistema operativo. [Instalacion en Windows](/docs/en/Installation_on_Windows.md). [Instalacion en Unix](/docs/en/Installation_on_Unix.md) (Linux, MacOS).

El uso y la instalacion del bot se hace a travez de consola de comandos (terminal / CMD). No tengas miedo, no es para nada complicado!

### ¿ Como ejecuto el bot?

Primero tenes que instalarlo. Despues vas a la carpeta de ejemplos y ejecutas alguno de los scripts via linea de comandos, por ejemplo:
``` python
python multi_script_CLI.py
```

Si el script necesita que le pasen algun parametro para ejecutarse, por ejemplo, una lista de hashtags para a likear, el script lo notificara. Por ejemplo, like_hashtags.py, tendra como salida:
```
Usage: Pass hashtags to like
Example: python like_hashtags.py dog cat
```

Explica claramente como funciona el script en particular. Por ejemplo, si quiere likear los contenidos mas recientes con el hashtag **#cat** o **#dog**, entonces debe ejecutar:
``` python
python like_hashtags.py cat dog
```

### ¿Donde debo ingresar el nombre de usario y contraseña de Instagram?

El bot pedira que los ingrese la primera vez que se ejecute. Se guardaran en secret.txt y se tomaran de dicho archivo en futuras ejecuciones. Tambien pueden ingresarse manualmente usando la funcion login():
``` python
bot.login(username=«my_username», password=«my_password»)
```

Ademas, cuando ejecute el script por primera vez, podra agregar multiples cuentas a Instabot. En futuras ejecuciones, si ingreso mas de una cuenta, antes de que comience el stript, podra elegir la cuenta a usar.

### Cuando ingreso la contraseña no se ve en pantalla! ¿Que hago?

La contraseña no se muestra especificamente para que no sea vista por otros. Не переживайте, он вводится корректно. Если вы случайно ввели неправильный пароль, то при следующем запуске, если пароль не подойдет, Вас попросят ввести его еще раз. 

### Cuando ingreso mi usuario y contraseña de Instagram ¿Donde se guardan? ¿Se retrasmiten a algun lado?

El/los usuarios y contraseñas ingresadas se guardan localmente en la computadora donde se ejecutaron en el archivo secret.txt. No son reenviados a ningun sitio externo.

### ¿Instagram va a bannear/bloquear mi cuenta por usar Instabot?

Los Términos de servicio Instagram establecen que no se puede usar bots. Para evitar ser detectado como tal, Instabot tiene establecidos limites en el numero de subscripciones / likes / commentarios y demas por dia, asi como tambien en la frecuencia de las requests(llamadas) - para, por ejemplo, evitar subscribirse demasiado rapido. Instabot ya viene preconfigurado con sus propios limites, los cuales garantizan un uso seguro. Estos valores pueden ser cambiados, pero sea cuidadoso. Aqui hay mas detalles (make a page with a description of these parameters and how to change). El bot guarda el numero de likes / follows / unfollows etc y los resetea una vez al dia.

### ¿Es posible acelerar los tiempos de espera, por ejemplo, entre unfollows/desuscripciones? ¿Es seguro?

Son parametros de la clase `instabot.Bot ()`. Si usa el script __milti_script_CLI__ , puede abrirlo con un editor de texto, buscar el valor __unfollow_delay = 30__ , y cambiarlo a lo que desee. De igual manera, puede cambiar los demas parameteros. Pero note que esto puede ser inseguro.

Si usted se desubscribe/unfollow 100 personar por segundo, su cuenta va a ser seguramente banneada/bloqueada/suspendida. Los limites dependen de la antiguedad y el tamaño de la cuenta, entonces el ajuste fino de su cuenta en particular depuende exclusivamente de usted mismo. Los valores configurados por defecto son los seguros _para la mayoria_. Nadie que haya usado los valores por defecto ha sido baneado.

### I want the bot to unsubscribe from accounts that did not respond with a mutual subscription.

For your task, the already written script, which lies in the examples folder: unfollow_non_followes.py, is suitable. Just go to the folder with this script on your computer and run it in the terminal.
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

You can:
* Put the star in Github. To do this, just click on the star here https://github.com/instagrambot (top right), May need to register (for free).
* Login to [Telegram Group](https://t.me/instabotproject) and help newcomers to understand the installation and configuration of Instabot. 
* Tell us about our project wherever possible. It will be enough to throw off the link: https://instagrambot.github.io.
* You can find bugs and errors found in [Issues](https://github.com/instagrambot/instabot/issues), be sure to attach the _screenshots_ and _commands_ that you entered. This will help correct these errors and make Instabot better!
* Correct these errors if you are a developer. Do this through the Pull request, following the standard PEP8.
* To develop our [site](https://github.com/instagrambot/instagrambot.github.io). We need both a designer and a frontend developer. If you have long wanted to do something from scratch, welcome.
