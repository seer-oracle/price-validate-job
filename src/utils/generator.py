# -*- coding: utf-8 -*-

# File: generator.py
# Created at 03/04/2022
"""
   Description:
        -
        -
"""
import string
from random import choice


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(choice(chars) for x in range(size))
