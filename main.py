#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : main.py
# Description   : Función main del bot
# Author        : jesusFx
# Author        : Veltys
# Date          : 10-04-2019
# Version       : 0.1.1
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


    try:
        my_bot = bot()

    except FileNotFoundError:
        print('Error: No se ha encontrado el archivo con el token para este bot')

    except PermissionError:
        print('Error: Sin permisos suficientes para guardar el archivo de registro de este bot')

    else:
        my_bot.arrancar()
        my_bot.cerrar()


if __name__ == '__main__':
    main(sys.argv)
