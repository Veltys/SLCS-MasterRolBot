#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : bot.py
# Description   : Módulo del bot
# Author        : jesusFx
# Author        : Veltys
# Date          : 12-04-2019
# Version       : 0.3.1
# Usage         : import bot | from log bot ...
# Notes         : 


DEBUG                   = True                                                              # Flag de depuración
NOMBRE_ARCHIVO_REGISTRO = 'MasterRolBot.log'                                                # Archivo de registro


import signal                                                                               # Manejo de señales

import telebot                                                                              # Funcionalidades de la API del bot

from time   import gmtime, strftime                                                         # Funcionalidades varias de tiempo

from logger import logger                                                                   # Funcionalidad de registro
from pid    import pid                                                                      # Funcionalidad de PID


class bot:
    ''' Clase con todo lo necesario para ejecutar el bot
    '''


    def __init__(self):
        ''' Constructor de la clase:
                - Carga el token del acceso a la api de Telegram
                - Si ha podido cargarlo con éxito:
                    - Activa el sistema de registro
                    - Conecta con la api de Telegram
                    - Prepara la llamada al "listener"
                    - Prepara el objeto pid
                    - Captura la señal "sigterm"
                - Si no:
                    - Retorna None y no hace nada más
        '''


        self.__comandos = {
            '/ayuda'    : bot.cmd_ayuda     ,
            '/help'     : bot.cmd_ayuda     ,
            '/opcion'   : bot.cmd_opcion    ,
            '/option'   : bot.cmd_opcion    ,
        }

        self._cargar_token()

        if DEBUG:
            print('Debug: Inicializando bot...')
            print('Debug: El token para este bot es ' + self._token_bot)

        self._log = logger(NOMBRE_ARCHIVO_REGISTRO)

        if DEBUG:
            print('Debug: Activado el sistema de registro')

        self._bot = telebot.TeleBot(self._token_bot, threaded = False)                      # FIXME: Comportamiento no controlado cuando el token no es válido
        self._bot.set_update_listener(self.listener)                                        # Asociación de la función listener al bot

        self._pid = pid('MasterRolBot')

        signal.signal(signal.SIGTERM, self._sig_cerrar)


    def _cargar_token(self):
        ''' Método privado de carga del token de Telegram:
                - Intenta abrir para su lectura el archivo del token
                - Si puede:
                    - Lo lee y lo almacena en la variable correspondiente
                    - Cierra el archivo
                - Si no:
                    - No hace nada
        '''


        archivo_token_bot = open('.bot.token', 'r')

        self._token_bot = archivo_token_bot.read()
    
        archivo_token_bot.close()

        self._token_bot = self._token_bot.lstrip().replace("\n", '')                        # Eliminación de espacios y demás del final... por si acaso...
    

    def _sig_cerrar(self, signum, frame):
        ''' Método "wrapper" para la captura de la señal "sigterm"
        '''


        self.cerrar()


    def arrancar(self):
        ''' Método de arranque del bot:
                - Activa el sistema de pid para su posterior recuperación
                - Lanza el sistema de espera de mensajes de la api de Telegram
        '''

        self._pid.activar()

        self._bot.polling(none_stop = True)                                                 # Recepción de mensajes


    def cerrar(self):
        ''' Método de cierre:
            - Realiza las operaciones necesarias pevias al cierre del sistema, tales como cierres de archivos y otros bloqueos
        '''

        if DEBUG:
            print('Debug: Invocado el cierre del sistema')

        self._log.cerrar()

        if DEBUG:
            print('Debug: Desactivado el sistema de registro')

        self._pid.desactivar()


    def cmd_ayuda(self, mensaje):
        ''' Método para responder al usuario con el texto de ayuda:
            - Responde con el texto de ayuda
        '''

        self._bot.send_message(mensaje.chat.id, '''
Soy *MasterRolBot*, el bot de juego de partidas de rol

Comandos disponibles:
- /ayuda o /help: Mostrar este texto de ayuda
- /iniciar o /start: Iniciar una nueva aventura
- /elegir _<aventura>_ o /choose _<aventura>_: Elegir una nueva aventura
- /opcion _<letra>_ o /option _<letra>_: Seleccionar la opción _<letra>_
''', parse_mode = 'Markdown')                                                               # El parámetro "parse_mode" permite mandar texto enriquecido


    def cmd_opcion(self, mensaje):
        ''' Método de avance en la aventura a través de una opción
            - Si existe aventura en curso para el usuario:
                - La carga
                - Si la opción es válida:
                    - Avanza al estado correspondiente e informa al usuario
                - Si no:
                    - Informa al usuario del error y de las opciones disponibles
            - Si no:
                - Informa al usuario de que no está jugando y le ofrece el catálogo de aventuras disponibles
        '''


        pass


    def interpretar(self, mensaje):
        ''' Método "parser" para interpretar el mensaje y actuar en consecuencia
            - Lee el texto del mensaje
            - Lo busca en la información de comandos
            - Si es encontrado:
                - Llama al método indicado
            - Si no:
                - No hace nada
        '''

        if mensaje.text[0] == '/':
            try:
                self.__comandos[mensaje.text.split(' ')[0]](self, mensaje)
    
            except KeyError:
                pass
    
            else:
                pass
    
            finally:
                pass

        else:
            pass


    def listener(self, mensajes):
        ''' Método estático de escucha de mensajes entrantes
            - Accede al sistema de registro
            - Procesa los mensajes uno a uno
            - Los registra
        '''

        log = logger(NOMBRE_ARCHIVO_REGISTRO)

        for mensaje in mensajes:
            texto = strftime("%d/%m/%Y, %H:%M:%S", gmtime()) + ' - '

            if mensaje.chat.id > 0:                                                         # Si el CID > 0 (chat con usuario):
                texto += str(mensaje.chat.first_name)                                       #     Obtención del nombre

            else:                                                                           # Si no (chat con grupo):
                texto += str(mensaje.from_user.first_name)                                  #     Obtención del nombre

            texto += ' [' + str(mensaje.chat.id) + ']: ' + mensaje.text                     # Composición del resto del texto

            log.registrar(texto + "\n")

            if DEBUG:
                print('Debug: Nuevo mensaje ➡ ' + texto)

            self.interpretar(mensaje)

