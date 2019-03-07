#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : main.py
# Description   : Función main del bot
# Author        : jesusFx
# Author        : Veltys
# Date          : 07-03-2019
# Version       : 0.0.1
# Usage         : python3 main.py
# Notes         : 


DEBUG           = False                                                                             # Flag de depuración


import sys                                                                                          # Funcionalidades varias del sistema


def cargar_token():
    try:
        archivo_token_bot = open('.bot.token', 'r')

        token_bot = archivo_token_bot.read()
    
        archivo_token_bot.close()
        
        return token_bot

    except FileNotFoundError:
        return None


def main(argv):
    token_bot = cargar_token()

    if(token_bot != None):
        print('El token para este bot es ' + token_bot)

        # TODO: Seguir aquí

    else:
        print('Error: No se ha encontrado el archivo con el token para este bot')


if __name__ == '__main__':
    main(sys.argv)
