#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : main.py
# Description   : Módulo de registro (log) del bot
# Author        : jesusFx
# Author        : Veltys
# Date          : 10-04-2019
# Version       : 0.1.1
# Usage         : import log | from log import ...
# Notes         : Implementado con el patrón singleton para evitar más de un sistema de registro simultáneo


from platform import system


class logger:
    ''' Clase con todo lo necesario para manejar un archivo de registro
    '''


    __instancia         = None                                                                      # Declarar una variable directamente en la clase la hace estática


    def __new__(cls, nombre_archivo):
        ''' Creador de la clase:
                Al implementar el patrón Singleton, es necesario interceptar la creación de la clase, para no crear más de una instancia de la misma

                - Comprueba si existe alguna otra instancia
                - Si no:
                    - Crea una nueva instancia de la clase

                - Devuelve la instancia de la clase
        '''


        if logger.__instancia == None:
            logger.__instancia = object.__new__(cls)

        return logger.__instancia


    def __init__(self, nombre_archivo):
        ''' Constructor de la clase:
                - Abre el archivo de registro
        '''


        self._archivo_registro = open(self.ruta_log() + nombre_archivo, 'a', encoding='utf-8')


    def cerrar(self):
        ''' Método de cierre de la clase:
                - Si hay un archivo de registro abierto:
                    - Lo cierra
                
        '''


        try:
            self._archivo_registro.close()

        except AttributeError:
            pass


    def registrar(self, texto):
        ''' Método de registro de texto:
                - Registra el texto recibido
        '''


        try:
            self._archivo_registro.write(texto + "\n")

        except AttributeError:
            return False

        else:
            return True


    @staticmethod
    def ruta_log():
        ''' Método estático de obtención de la ruta donde guardar el archivo de registro:
                - Si estamos en Windows:
                    - La ruta será en el mismo directorio
                - Si estamos en Linux
                    - La ruta será en /var/log/
                - Devuelve la ruta
        '''


        if system() == 'Windows':
            ruta_archivo = '.\\'
    
        else:
            ruta_archivo = '/var/log/'

        # TODO: Otros sistemas operativos
    
        return ruta_archivo


    def __del__(self):
        ''' Destructor de la clase:
                - Invoca al método de cierre
        '''


        self.cerrar()
