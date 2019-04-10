#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : main.py
# Description   : Función main del bot
# Author        : jesusFx
# Author        : Veltys
# Date          : 11-03-2019
# Version       : 0.1.0
# Usage         : python3 main.py
# Notes         : 


DEBUG           = True                                                                              # Flag de depuración


import sys                                                                                          # Funcionalidades varias del sistema

from bot import bot                                                                                 # Clase contenedora del bot


def main(argv):
    ''' Función main del programa:
            - Intenta crear una instancia del bot
            - Si tiene éxito:
                - Arranca el bot
                - No debería de llegar a este puto, pero llegado el caso, procede al cierre del mismo
            - Si no:
                - Muestra el error por pantalla
    '''


    my_bot = bot()

    if my_bot != None:
        my_bot.arrancar()

        my_bot.cerrar()

    else:
        print('Error: No se ha encontrado el archivo con el token para este bot')


if __name__ == '__main__':
    main(sys.argv)
