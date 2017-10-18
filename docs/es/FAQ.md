# Preguntas frecuentes en Instabot.

### ¿Como instalo el bot?

La instalacion en sí depende del sistema operativo. [Instalacion en Windows](/docs/en/Installation_on_Windows.md). [Instalacion en Unix](/docs/en/Installation_on_Unix.md) (Linux, MacOS).

El uso y la instalación del bot se lleva a cabo través de consola de comandos (terminal / CMD). No tengas miedo, no es para nada complicado!

### ¿Como ejecuto el bot?

Primero tenes que instalarlo. Despues vas a la carpeta de ejemplos y ejecutas alguno de los scripts via linea de comandos, por ejemplo:
``` python
python multi_script_CLI.py
```

Si el script necesita que le pasen algun parametro para ejecutarse, por ejemplo, una lista de hashtags para a likear, el script lo notificará. Por ejemplo, like_hashtags.py, tendra como salida:
```
Usage: Pass hashtags to like
Example: python like_hashtags.py perro gato
```

Explica claramente como funciona el script en particular. Por ejemplo, si quiere likear los contenidos mas recientes con el hashtag **#perro** o **#gato**, entonces debe ejecutar:
``` python
python like_hashtags.py perro gato
```

### ¿Donde debo ingresar el nombre de usario y contraseña de Instagram?

El bot pedirá que los ingrese la primera vez que se ejecute. Se guardaran en secret.txt y se tomaran de dicho archivo en futuras ejecuciones. Tambien pueden ingresarse manualmente usando la funcion login():
``` python
bot.login(username=«my_username», password=«my_password»)
```

Ademas, cuando ejecute el script por primera vez, podra agregar múltiples cuentas a Instabot. En futuras ejecuciones, si ingresa mas de una cuenta, antes de que comience el stript, podra elegir la cuenta a usar.

### Cuando ingreso la contraseña no se ve en pantalla! ¿Que hago?

La contraseña no se muestra especificamente para que no sea vista por otros. No se preocupe, se ingresó correctamente. Si accidentalmente ingresó la contraseña incorrecta, la próxima vez que lo ejecute, si la contraseña no funciona, le pedirá que la ingrese nuevamente.

### Cuando ingreso mi usuario y contraseña de Instagram ¿Donde se guardan? ¿Se envían a algun lado?

El/los usuarios y contraseñas ingresadas se guardan localmente en la computadora donde se ejecutaron en el archivo secret.txt. No son reenviados a ningun sitio externo.

### ¿Instagram va a bannear/bloquear mi cuenta por usar Instabot?

Los Términos de servicio Instagram establecen que no se puede usar bots. Para evitar ser detectado como tal, Instabot tiene establecidos limites en el numero de subscripciones / likes / commentarios y demas por dia, asi como tambien en la frecuencia de las requests (llamadas) - para, por ejemplo, evitar subscribirse demasiado rápido. Instabot ya viene preconfigurado con sus propios límites, los cuales garantizan un uso seguro. Estos valores pueden ser cambiados, pero sea cuidadoso. Aqui hay mas detalles (hacer una página con la descripción de éstos parametros e ingresar el link). El bot guarda el numero de likes / follows / unfollows etc y los resetea una vez al dia.

### ¿Es posible acelerar los tiempos de espera, por ejemplo, entre unfollows/desuscripciones? ¿Es seguro?

Son parámetros de la clase `instabot.Bot ()`. Si usa el script __milti_script_CLI__.py , puede abrirlo con un editor de texto, buscar el valor __unfollow_delay = 30__ , y cambiarlo a lo que desee. De igual manera, puede cambiar los demas parameteros. Pero tenga en cuenta que esto puede ser inseguro.

Si usted se desubscribe/unfollow 100 personas por segundo, su cuenta va a ser seguramente banneada/bloqueada/suspendida. Los limites dependen de la antiguedad y el tamaño de la cuenta, entonces el ajuste fino de su cuenta en particular depuende exclusivamente de usted mismo. Los valores configurados por defecto son los seguros para la mayoria. Nadie que haya usado los valores por defecto ha sido baneado.

### Quiero que el bot se unsubscriba de cuentas que seguimos pero que no han correspondido con una subscripción mútua (sigo pero no me siguen)

Para ello, el script ya escrito, que se encuentra en la carpeta de ejemplos: unfollow_non_followes.py, es adecuado. Sólo tienes que ir a la carpeta con este script en tu ordenador y ejecutarlo en el terminal

``` python
python unfollow_non_followers.py
```

### Quiero que el bot ponga likes de posts con determinados hashtags, que indicaré en una lista.

De nuevo todo es muy simple! Ejecuta el programa like_hashtags.py de la carpeta \example, por ejemplo así:

``` python
python like_hashtags.py perro gato
```

### Demasiados scripts! Hay algún tipo de paquete?

Lo hay. Gracias a los esfuerzos de nuestra comunidad, un se escribió una secuencia muy guay. Puede encontrarlo bajo el nombre [multi_script_CLI.py] (/examples/multi_script_CLI.py). Está en inglés, pero creo que se entiende. ¡Le aconsejo encarecidamente que lo pruebe!

### Como puedo organizar el auto-posting (publicación automática de una foto) de una foto en Instagram?

Para ello, tenenemos una muestra en examples.
En esa página usted encontrará cómo configurar y poner en marcha la auto-publicación (auto-post).

### AutoPost, publica solo una foto o también el Hashtag?

Hastags es la misma descripción, solo tienes que añadirlos allí.

### Puedo publicar un vídeo via autoposting?

Desafortunadamente, no. Ésta funcionalidad, incrementaria mucho el tamaño del proyecto.

### Como puedo ayudar al proyecto?

Puedes así:
* Ponga la estrella en Github. Para hacer esto, basta con hacer clic en la estrella aquí https://github.com/instagrambot (arriba a la derecha), puede tener que registrarse (de forma gratuita).
* Inicie sesión en [Telegram Group] (https://t.me/instabotproject) y ayude a los recién llegados a comprender la instalación y configuración de Instabot.
* Cuénta sobre nuestro proyecto siempre que sea posible. Será suficiente dar salida al enlace: https://instagrambot.github.io
* Puedes encontrar errores y buhs detectados en [Issues] (https://github.com/instagrambot/instabot/issues), asegúrese de adjuntar las capturas de pantalla y commandos que ha introducido. Esto nos ayudará ha tener un Instabot mejor!
* Corrige éstos errores si eres un desarrollador. Hazlo a través de una petición Pull request, siguiendo el estandart PEP8.
* Para desarrollar nuestro [sitio] (https://github.com/instagrambot/instagrambot.github.io). Necesitamos un diseñador y un desarrollador de frontend. Si hace tiempo que quieres hacer algo desde cero, bienvenido.
