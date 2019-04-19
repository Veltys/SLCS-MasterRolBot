#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : bot.py
# Description   : Módulo del bot
# Author        : jesusFx
# Author        : Veltys
# Date          : 19-04-2019
# Version       : 0.6.0
# Usage         : import bot | from log bot ...
# Notes         : 

ADMINISTRADORES         = []                                                                # Lista de administradores
ADMINISTRADORES.append(***REMOVED***)                                                           # Jesús
ADMINISTRADORES.append(***REMOVED***)                                                           # Rafa
DEBUG                   = True                                                              # Flag de depuración
NOMBRE_ARCHIVO_REGISTRO = 'MasterRolBot.log'                                                # Archivo de registro


import signal                                                                               # Manejo de señales
import sqlite3                                                                              # Manejo de BB. DD. SQLite 3

import telebot                                                                              # Funcionalidades de la API del bot

from time       import gmtime, strftime                                                     # Funcionalidades varias de tiempo

from logger     import logger                                                               # Funcionalidad de registro
from pid        import pid                                                                  # Funcionalidad de PID


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
            '/play'     : bot.cmd_play      ,
            '/start'    : bot.cmd_start     ,

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


    def _filtrar_texto(self, texto):
        ''' Método de filtrado para extraer la id de un comando
        '''

        if texto[0] == '/':
            id_texto = texto[1:]

        else:
            id_texto = texto

        if id[0:4] == 'play':
            id_texto = id[5:]

        elif id[0:6] == 'option':
            id_texto = id[7:]

        return id_texto


    def _mostrar_estado(self, usuario):
        # TODO: Documentar

        letra = []

        letra.append('a')
        letra.append('b')
        letra.append('c')
        letra.append('d')

        self._bbdd.execute('SELECT `Estado` FROM `Usuarios` WHERE `Id` = (?)', (
            usuario ,
        ))

        estado = self._bbdd.fetchone()[0]

        self._bbdd.execute('''
SELECT `Nombre`, `Descripcion` FROM `Estados` WHERE `Id` = (?)
''', (
            estado  ,
        ))

        res = self._bbdd.fetchone()

        texto = '*' + res[0] + "*\n" + res[1]

        self._bbdd.execute('''
SELECT `Nombre` FROM `Estados` WHERE `Id` IN(
    SELECT `Siguiente` FROM `Opciones` WHERE `Estado` = (?)
)
''', (
            estado  ,
        ))

        botones = telebot.types.ReplyKeyboardMarkup()

        opciones = self._bbdd.fetchall()

        i = 0

        for opcion in opciones:
            texto += '/' + letra[i] + ' ' + opcion[0] + "\n"

            botones.add(telebot.types.KeyboardButton(letra[i]))

            i = i + 1

        else:
            texto += "/start Comenzar una nueva aventura\n"

            botones.add(telebot.types.KeyboardButton('start'))

        self._bot.send_message(usuario, texto, parse_mode = 'Markdown', reply_markup = botones)


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

        try:
            self.__bbdd.commit()

        except sqlite3.OperationalError as e:
            self._log.registrar('ERROR: Imposible guardar los cambios en la BB. DD. ➡ ' + str(e) + "\n")

        else:
            pass

        finally:
            self.__bbdd.close()

            if DEBUG:
                print('Debug: Desconectado de la BB. DD.')

        self._log.cerrar()

        if DEBUG:
            print('Debug: Desactivado el sistema de registro')

        self._pid.desactivar()


    def cmd_help(self, mensaje):
        ''' Método para responder al usuario con el texto de ayuda:
            - Responde con el texto de ayuda
        '''

        self._bot.send_message(mensaje.chat.id, '''
Soy *MasterRolBot*, el bot de juego de partidas de rol

Comandos disponibles:
- /help: Mostrar este texto de ayuda
- /start: Iniciar una nueva aventura
- /play _<aventura>_: Elegir una nueva aventura
- /option _<letra>_: Seleccionar la opción _<letra>_
''', reply_markup = telebot.types.ReplyKeyboardRemove(), parse_mode = 'Markdown')                                                               # El parámetro "parse_mode" permite mandar texto enriquecido


    def cmd_close(self, mensaje):
        ''' Método "wrapper" para llevar a cabo el cierre del bot
            - Cierra el bot si recibe dos veces el comando adecuado
        '''

        self._bot.send_message(mensaje.chat.id, 'OK: Ejecutando comando de cierre...', reply_markup = telebot.types.ReplyKeyboardRemove())

        if self.__cierre == False:
            self.__cierre = True

            self._bot.send_message(mensaje.chat.id, 'AVISO: Vuelva a ejecutar el comando para continuar con el cierre')

        else:
            self._bot.send_message(mensaje.chat.id, 'OK: Ejecutando cierre...', reply_markup = telebot.types.ReplyKeyboardRemove())

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

        id_opcion = self._filtrar_texto(mensaje.text)

        self._bbdd.execute('SELECT `Estado` FROM `Usuarios` WHERE `Id` = (?)', (
            mensaje.chat.id
        ))

        res = self._bbdd.fetchone()

        if res[0] != 0:
            if id_opcion == 'a':
                limite = 0

            elif id_opcion == 'b':
                limite = 1

            elif id_opcion == 'c':
                limite = 2

            else: # id_opcion == d
                limite = 3

            self._bbdd.execute('''
UPDATE `Usuarios` SET `Estado` = (
SELECT `Id` FROM `Opciones` WHERE `Estado` = (?) LIMIT (?), 1
) WHERE `Id` = (?)
''', (
                res[0]          ,
                limite          ,
                mensaje.chat.id ,
            ))

            self._mostrar_estado(mensaje.chat.id)

        else:
            texto = 'ERROR: Seleccione primero una aventura'

        self._bot.send_message(mensaje.chat.id, texto, reply_markup = telebot.types.ReplyKeyboardRemove())


    def cmd_play(self, mensaje):
        ''' Método de inicio de una aventura a través de una opción
            - Busca el nombre del juego solicitado por el usuario
            - Si existe:
                - Actualiza el estado del usuario al inicial de la aventura (el mínimo estado correspondiente)
            - Si no:
                - No existe tal aventura
            - Informa al usuario del resultado
        '''

        id_juego = self._filtrar_texto(mensaje.text)

        self._bbdd.execute('SELECT `Nombre` FROM `Juegos` WHERE `Id` = (?)', (
            id_juego    ,
        ))

        res = self._bbdd.fetchone()

        if res != None:
            self._bbdd.execute('''
UPDATE `Usuarios` SET `Estado` = (
    SELECT MIN(`Id`) FROM `Estados` WHERE `Juego` = (?)
) WHERE `Id` = (?)
''', (
                id_juego        ,
                mensaje.chat.id ,
            ))

            texto = 'OK: Comenzando nueva partida en ' + res[0]

        else:
            texto = 'ERROR: La aventura seleccionada (' + id_juego + ') no existe o no está disponible en este momento'

        self._bot.send_message(mensaje.chat.id, texto, reply_markup = telebot.types.ReplyKeyboardRemove())

        self._mostrar_estado(mensaje.chat.id)


    def cmd_start(self, mensaje):
        ''' Método de inicio del bot a través de una opción
            - Si existe el usuario:
                - Se le informa de las opciones que puede utilizar
            - Si no existe:
                - Se introduce en la BB. DD.
                - Se le da la bienvenida mostrando una lista con las aventuras disponibles
        '''

        try:
            self._bbdd.execute('INSERT INTO `Usuarios`(`Id`) VALUES (?)', (
                str(mensaje.chat.id)    ,
            ))

        except sqlite3.IntegrityError:
            self._bbdd.execute('SELECT Estado FROM Usuarios WHERE Id = (?)', (
                str(mensaje.chat.id)    ,
            ))

            if self._bbdd.fetchone()[0] == 0:
                texto = '¡Bienvenido, ' + mensaje.chat.first_name + "!\nLa lista de aventuras disponibles es:"

            else:
                texto = '¡Bienvenido, ' + mensaje.chat.first_name + '''!
Si deseas continuar, responde con la opción que desees.
Si deseas reiniciar tu aventura, puedes usar el comando /reiniciar
Si deseas cambiar de aventura, aquí tienes una lista de aventuras disponibles:
'''

        else:
            texto = '¡Bienvenido, ' + mensaje.chat.first_name + "!\nLa lista de aventuras disponibles es:"

        finally:
            self._bbdd.execute('SELECT `Id`, `Nombre` FROM `Juegos` WHERE `Id` != 0')

            botones = telebot.types.ReplyKeyboardMarkup()

            juegos = self._bbdd.fetchall()

            for juego in juegos:
                texto += '/' + str(juego[0]) + ' ' + juego[1] + "\n"

                botones.add(telebot.types.KeyboardButton(str(juego[0])))

            self._bot.send_message(mensaje.chat.id, texto, parse_mode = 'Markdown', reply_markup = botones)


    def interpretar(self, mensaje):
        ''' Método "parser" para interpretar el mensaje y actuar en consecuencia
            - Lee el texto del mensaje
            - Lo busca en la información de comandos
            - Si es encontrado:
                - Llama al método indicado
            - Si no:
                - No hace nada
        '''

        if mensaje.text[0] == '/':                                                          # Comando explícito, comenzando por /
            try:
                self.__comandos[mensaje.text.split(' ')[0]](self, mensaje)
    
            except KeyError:
                try:
                    int(mensaje.text[1:])                                                   # Comando explícito, número
    
                except ValueError:
                    if len(mensaje.text) == 2 and mensaje.text[1].isalpha():                # Comando explícito, letra
                        self.cmd_option(mensaje)
            
                    else:                                                                   # Comando no reconocido
                        self._bot.send_message(mensaje.chat.id, 'ERROR: Comando no reconocido', reply_markup = telebot.types.ReplyKeyboardRemove())
    
                        self.__comandos['/help'](self, mensaje)

                else:
                    self.cmd_play(mensaje)
    
                finally:
                    pass

            else:
                pass
    
            finally:
                pass
            
        elif mensaje.text[0] == '.':                                                        # Comando de administración explícito, comenzando por .
            if mensaje.chat.id in ADMINISTRADORES:
                try:
                    self.__comandos[mensaje.text.split(' ')[0]](self, mensaje)

                except KeyError:
                    self._bot.send_message(mensaje.chat.id, 'ERROR: Comando no reconocido', reply_markup = telebot.types.ReplyKeyboardRemove())

                    self.__comandos['/help'](self, mensaje)

                else:
                    pass
    
                finally:
                    pass

            else:
                self._bot.send_message(mensaje.chat.id, 'ERROR: No tiene los permisos necesarios para ejecutar este comando', reply_markup = telebot.types.ReplyKeyboardRemove())

        else:
            try:
                int(mensaje.text)                                                           # Comando implícito, número

            except ValueError:
                if len(mensaje.text) == 1 and mensaje.text.isalpha():                       # Comando implícito, letra
                    self.cmd_option(mensaje)
        
                else:                                                                       # Texto no reconocido
                    self._bot.send_message(mensaje.chat.id, 'ERROR: Texto no reconocido', reply_markup = telebot.types.ReplyKeyboardRemove())

            else:
                self.cmd_play(mensaje)

            finally:
                pass


    def listener(self, mensajes):
        ''' Método estático de escucha de mensajes entrantes
            - Accede al sistema de registro
            - Procesa los mensajes uno a uno
            - Los registra
        '''

        for mensaje in mensajes:
            texto = strftime("%d/%m/%Y, %H:%M:%S", gmtime()) + ' - '

            if mensaje.chat.id > 0:                                                         # Si el CID > 0 (chat con usuario):
                texto += str(mensaje.chat.first_name)                                       #     Obtención del nombre

            else:                                                                           # Si no (chat con grupo):
                texto += str(mensaje.from_user.first_name)                                  #     Obtención del nombre

            texto += "\t[" + str(mensaje.chat.id) + ']: ' + mensaje.text                     # Composición del resto del texto

            self._log.registrar(texto + "\n")

            if DEBUG:
                print('Debug: Nuevo mensaje ➡ ' + texto)

            self.interpretar(mensaje)
