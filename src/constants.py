# -*- coding: utf-8 -*-


# File: constants.py
# Created at 03/04/2022
"""
   Description:
        -
        -
"""


class Constants(object):
    # Does not cache to limit below IP
    IP_WHITE_LIST = ['127.0.0.1']
    # Number of request allow one IP request in a limit time
    LIMIT_REQUEST_QUOTA = 100
    # A period time to limit one IP request, in minute
    LIMIT_REQUEST_TIME = 10
    # Interval time between two times call the same function, in second
    INTERVAL_BETWEEN_CALLS = 25
    # Message
    MSG_REQUIRED_AUTH = 'Vui lòng đăng nhập để tiếp tục'
    # Response status
    STATUS_OK = 1
    STATUS_NOT_OK = 0
    # messgae

    MSG_NOT_FOUND = 'not found'
    MSG_UNKNOWN_ERROR = 'unknown error'
    MSG_SUCCCESS = 'success'
    # Error code
    CODE_NOT_E = ''
    E_NOT_FOUND = 'E_NOT_FOUND'
    E_SERVER = 'E_SERVER'
    E_AUTH = 'E_AUTH'
    E_INVALID_PARAMS = 'E_INVALID_PARAMS'
