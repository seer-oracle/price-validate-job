# -*- coding: utf-8 -*-

# File: price.py

"""
   Description: 
        -
        -
"""
from bson import ObjectId

from lib.decorators import handle_exception
from src.task import worker


@worker.task(name='worker.save_price', rate_limit='100/s')
@handle_exception()
def check_price(dex_result: dict, dex_price: dict, key: str):
    prefix_key = "Oracle:price"
    key_symbol = f"{prefix_key}_{dex_result.get('symbol')}_{key}"
    expired_time = 60*60*1 # 1 hour
  
    return
