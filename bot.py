#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : bot.py
# Description   : Módulo del bot
# Author        : jesusFx
# Author        : Veltys
# Date          : 09-04-2019
# Version       : 0.1.1
# Usage         : import bot | from log bot ...
# Notes         : 


DEBUG                   = True                                                                      # Flag de depuración
NOMBRE_ARCHIVO_REGISTRO = 'MasterRolBot.log'


import signal                                                                                       # Manejo de señales

import telebot                                                                                      # Funcionalidades de la API del bot

from time   import gmtime, strftime                                                                 # Funcionalidades varias de tiempo

from logger import logger                                                                           # Funcionalidad de registro
from pid    import pid                                                                              # Funcionalidad de PID


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


        self._cargar_token()

        if DEBUG:
            print('Debug: Inicializando bot...')
            print('Debug: El token para este bot es ' + self._token_bot)

        self._log = logger(NOMBRE_ARCHIVO_REGISTRO)

        self._bot = telebot.TeleBot(self._token_bot, threaded = False)                          # FIXME: Comportamiento no controlado cuando el token no es válido
        self._bot.set_update_listener(self.listener)                                            # Asociación de la función listener al bot

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

        self._bot.polling(none_stop = True)                                                         # Recepción de mensajes


    def cerrar(self):
        ''' Método de cierre:
            - Realiza las operaciones necesarias pevias al cierre del sistema, tales como cierres de archivos y otros bloqueos
        '''


        self._log.cerrar()

        self._pid.desactivar()


    # @staticmethod
    def listener(self, mensajes):
        ''' Método estático de escucha de mensajes entrantes
            - Accede al sistema de registro
            - Procesa los mensajes uno a uno
            - Los registra
        '''

        log = logger(NOMBRE_ARCHIVO_REGISTRO)

        for str_mensaje in mensajes:
            mensaje = strftime("%d/%m/%Y, %H:%M:%S", gmtime()) + ' - '

            if str_mensaje.chat.id > 0:                                                         # Si el CID > 0 (chat con usuario):
                mensaje += str(str_mensaje.chat.first_name)                                     #     Obtención del nombre

            else:                                                                               # Si no (chat con grupo):
                mensaje += str(str_mensaje.from_user.first_name)                                #     Obtención del nombre

            mensaje += ' [' + str(str_mensaje.chat.id) + ']: ' + str_mensaje.text               # Composición del resto del mensaje

            log.registrar(mensaje + "\n")

            if DEBUG:
                print('Debug: Nuevo mensaje ➡ ' + mensaje)

            # TODO: Parser de mensajes

            if str_mensaje.text == '/help':
                self._bot.send_message(str_mensaje.chat.id, "The following commands are available: \n")

