# MasterRolBot
Trabajo práctico de la asignatura Software Libre y Compromiso Social de la Universidad de Córdoba [![Codacy Badge](https://app.codacy.com/project/badge/Grade/3bd07a5ec898417ea90357d75d4cd643)](https://www.codacy.com/manual/veltys/SLCS-MasterRolBot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Veltys/SLCS-MasterRolBot&amp;utm_campaign=Badge_Grade)

## Descripción
Bot para Telegram que permite generar una partida de rol

## Módulos
-   :on: **main.py**:   Módulo de arranque y control del bot
-   :on: **bot.py**:    Módulo principal del bot
-   :on: **logger.py**: Módulo de registro del bot
-   :on: **pid.py**:    Módulo de prevención de ejecución de más de una instancia y de control del PID

## Versiones
-   0.0.1 :arrow_right: 08/03/2019:
    -   :end: Creación del script **main.py**
    -   :end: Carga del token de Telegram generado por [@BotFather](https://telegram.me/botfather)
    -   :end: Redacción de **README.md**

-   0.1.0 :arrow_right: 11/03/2019:
    -   :end: Mejora de **README.md**
    -   :end: Implementación del registro de mensajes
    -   :end: Implementación de la funcionalidad de pid

-   0.2.0 :arrow_right: 12/04/2020:
    -   :end: Implementación del intérprete de comandos
    -   :end: Implementación del comando de ayuda

-   0.3.0 :arrow_right: 12/04/2020:
    -   :soon: Implementación del comando de selcección de opción

-   0.4.0 :arrow_right: 12/04/2020:
    -   :end: Implementación de la BB. DD.
    -   :end: Actualizado de **README.md**

-   0.4.1 :arrow_right: 12/04/2020:
    -   :end: Reorganización de directorios
    -   :end: Añadidas fechas en las versiones en **README.md**

-   0.4.2: :arrow_right: 09/06/2020:
    -   :end: Reorganización de directorios
    -   :end: Mejoras en la calidad del código
    -   :end: Fechas de los archivos en formato ISO 8601
    -   :end: Actualizado **pid.py** a la última versión disponible

-   0.5.0: :arrow_right: 22/04/2021:
    -   :end: Añadido el archivo requirements.txt con los paquetes requeridos
    -   :end: Añadidas más protecciones en .gitignore
    -   :end: Cambiado el sistema de carga de administradores
    -   :end: Cambiado el sistema de cierre del bot
    -   :end: Mejorado el sistema de carga del token
    -   :end: Puesta al día de README.md 

## Entorno de desarrolloo
-   Java SE Runtime Environment (build 13.0.2+8)
-   Eclipse IDE for PHP Developers 2021-03 (4.19.0)
-   PyDev for Eclipse 8.3.0
-   DBeaver IDE 21.0.2
-   Windows 10 Pro 20H2 x86_64
-   Python 3.9.2
-   Librería [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) 3.7.7
-   SQLite 3.35.5

## Entorno de ejecución
-   Debian GNU/Linux 4.19.181-1 x86_64
-   Python 3.7.3
-   Librería [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) 3.7.7
-   SQLite 3.35.5

## Agradecimientos, fuentes consultadas y otros créditos
-   A *Juan Antonio Romero* y *Domingo Ortiz*, profesores de Software libre y compromiso social (en adelante, SLCS) en la [Universidad de Córdoba](http://www.uco.es/) durante el curso 2018-2019, sin los cuales no habría sido posible este proyecto
-   A la [documentación oficial de Python](https://docs.python.org/3/), por motivos evidentes
-   A [Veltys](https://github.com/Veltys), por [el módulo pid](https://github.com/Veltys/RPPGCT/blob/master/Python/pid.py) de su proyecto [RPPGCT](https://github.com/Veltys/RPPGCT), el cuál está siendo muy útil para este proyecto
-   A [*guu*](https://www.flickr.com/photos/gustavo/), por la [Foto para el avatar del bot](https://www.flickr.com/photos/gustavo/354116197/)

<!--

## Chuletario de emojis

(Estado: iniciado       ➡ :on:          )
(Estado: en curso       ➡ :soon:        )
(Estado: finalizado     ➡ :end:         )

-->
