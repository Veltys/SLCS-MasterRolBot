#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : bot.py
# Description   : Módulo del bot
# Author        : jesusFx
# Author        : Veltys
# Date          : 12-04-2019
# Version       : 0.4.2
# Usage         : import bot | from log bot ...
# Notes         : 

ADMINISTRADORES         = []                                                                # Lista de administradores
ADMINISTRADORES.append(163732926)                                                           # Jesús
ADMINISTRADORES.append(281866468)                                                           # Rafa
DEBUG                   = True                                                              # Flag de depuración
NOMBRE_ARCHIVO_REGISTRO = 'MasterRolBot.log'                                                # Archivo de registro


import signal                                                                               # Manejo de señales
import sqlite3                                                                              # Manejo de BB. DD. SQLite 3

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
                - Activa el sistema de registro
                - Conecta con la api de Telegram
                - Conecta con el SGBD
                - Prepara la llamada al "listener"
                - Prepara el objeto pid
                - Captura la señal "sigterm"
        '''


        self.__cierre   = False

        self.__comandos = {
            '/help'     : bot.cmd_help      ,
            '/option'   : bot.cmd_option    ,

            '.close'    : bot.cmd_close     ,
        }

        self._cargar_token()

        if DEBUG:
            print('Debug: Inicializando bot...')
            print('Debug: El token para este bot es ' + self._token_bot)

        self._log       = logger(NOMBRE_ARCHIVO_REGISTRO)

        if DEBUG:
            print('Debug: Activado el sistema de registro')

        self.__bbdd     = sqlite3.connect('bbdd.sqlite')
        self._bbdd      = self.__bbdd.cursor()

        if DEBUG:
            print('Debug: Conectado a la BB. DD.')

        self._bot       = telebot.TeleBot(self._token_bot, threaded = False)                # FIXME: Comportamiento no controlado cuando el token no es válido
        self._bot.set_update_listener(self.listener)                                        # Asociación de la función listener al bot

        self._pid       = pid('MasterRolBot')

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

        exit()


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

        self.__bbdd.commit()
        self.__bbdd.close()

        if DEBUG:
            print('Debug: Desconectado de la BB. DD.')

        self._pid.desactivar()


    def cmd_help(self, mensaje):
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


    def cmd_close(self, mensaje):
        ''' Método "wrapper" para llevar a cabo el cierre del bot
            - Cierra el bot si recibe dos veces el comando adecuado
        '''

        self._bot.send_message(mensaje.chat.id, 'OK: Ejecutando comando de cierre...')

        if self.__cierre == False:
            self.__cierre = True

            self._bot.send_message(mensaje.chat.id, 'AVISO: Vuelva a ejecutar el comando para continuar con el cierre')

        else:
            self._bot.send_message(mensaje.chat.id, 'OK: Ejecutando cierre...')

            self.cerrar()

            exit()


    def cmd_option(self, mensaje):
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

    def cmd_start(self, mensaje):
        
        with self._bbdd:
            self._bbdd.execute("insert into Usuarios(Id) values (?)", (str(mensaje.chat.id),))

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
                self._bot.send_message(mensaje.chat.id, 'ERROR: Comando no reconocido')
    
                self.__comandos['/help'](self, mensaje)

            else:
                pass
    
            finally:
                pass

        elif mensaje.text[0] == '.':
            if mensaje.chat.id in ADMINISTRADORES:
                try:
                    self.__comandos[mensaje.text.split(' ')[0]](self, mensaje)

                except KeyError:
                    self._bot.send_message(mensaje.chat.id, 'ERROR: Comando no reconocido')

                    self.__comandos['/help'](self, mensaje)

                else:
                    pass
    
                finally:
                    pass

            else:
                self._bot.send_message(mensaje.chat.id, 'ERROR: No tiene los permisos necesarios para ejecutar este comando')

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

            texto += "\t[" + str(mensaje.chat.id) + ']: ' + mensaje.text                     # Composición del resto del texto

            log.registrar(texto + "\n")

            if DEBUG:
                print('Debug: Nuevo mensaje ➡ ' + texto)

            self.interpretar(mensaje)

