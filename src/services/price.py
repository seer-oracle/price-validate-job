import json, hmac, hashlib, time, base64
import asyncio
import time
import sys
from src.helpers.pricing import PriceHelper
from datetime import datetime, timezone
from src.worker.price import check_price
from thor_requests.connect import Connect
from thor_requests.wallet import Wallet
from thor_requests.contract import Contract
import requests
from src.config import DefaultConfig

# SeerOracleVETUSD: 0x3212feD5581DEFbb2d7Ea21d7F22f657cD3da97E
# SeerOracleVETHOUSD: 0x5E7A52743575FE6F8cD8937C0415640338eBdd29
# SeerOracleVBUSD: 0xDf925feC9932A1De0d2b4404cCfac09166624F94
# SeerOracleVEUSDUSD: 0xA2B0d7b38dc13a58A7B4c0E8E2400d650dad46EC
# SeerOracleBTCUSD: 0x18A2fEAae2fA06B3452fd094Ba802C93FF0dA972
# SeerOracleETHUSD: 0xed8e829cfEB0Cdd315C26c7df10e81B12a3abA95
   
contracts = [
    {
        'name': "SeerOracleVETUSD",
        'symbol': "VET",
        'address': "0x3212feD5581DEFbb2d7Ea21d7F22f657cD3da97E" 
    },
    {
        'name': "SeerOracleVETHOUSD",
        'symbol': "VTHO",
        'address': "0x5E7A52743575FE6F8cD8937C0415640338eBdd29" 
    },
    # {
    #     'name': "SeerOracleVBUSD",
    #     'symbol': "VB",
    #     'address': "0xDf925feC9932A1De0d2b4404cCfac09166624F94" 
    # },
    {
        'name': "SeerOracleVEUSDUSD",
        'symbol': "VEUSD",
        'address': "0xA2B0d7b38dc13a58A7B4c0E8E2400d650dad46EC" 
    },
    {
        'name': "SeerOracleBTCUSD",
        'symbol': "BTC",
        'address': "0x18A2fEAae2fA06B3452fd094Ba802C93FF0dA972" 
    },
    {
        'name': "SeerOracleETHUSD",
        'symbol': "ETH",
        'address': "0xed8e829cfEB0Cdd315C26c7df10e81B12a3abA95" 
    },
    # {
    #     'name': "SeerOracleUSDCUSD",
    #     'symbol': "USDC",
    #     'address': "0x109272eF2326d57A591dF5FD9D828AcdC72A212E" 
    # },
    # {
    #     'name': "SeerOracleUSDTUSD",
    #     'symbol': "USDT",
    #     'address': "0xbC8c3831117aC9A7E144f25A892A5410941d2C90" 
    # },
    # {
    #     'name': "SeerOracleBUSDUSDT",
    #     'symbol': "BUSD",
    #     'address': "0x5a513838ad80670aE8e48A99416b4D0897763fcA" 
    # },
]               
                
def check_price_interval():
    
    # get price feed on chain
    abi_path = 'src/abi/SeerOracle.json'
    connector = Connect("https://testnet.veblocks.net")
    _contract = Contract.fromFile(abi_path)
    
    
    # get price feed through api
    headers = {
                'Content-Type': 'application/json'
            }
    method = "GET"
    _body = None

    
    for contract in contracts:
        _contract_addr = contract.get("address")
        res = connector.call("0x22f8Cc65F04B107D1c5352Acfa3157Af98858D60", _contract, "latestAnswer", [], to=_contract_addr)
        print("FROM CONTRACT(",contract.get("name"), "): ", res.get("decoded"))
        
        
        url_request= f"https://api-stag.vebank.io/v1/oracle/price/symbol/{contract.get('symbol')}"
        response = requests.request(method=method, 
                                    url=url_request,
                                    json= _body,
                                    headers=headers
        )
        if response.status_code == 200:
                result = response.json()
                _prices = result.get("data").get("list_price")
                print("FROM API ", _prices)
        _hard_token_decimal = 18
        _price_smc = float(res.get("decoded")['0']) / 10**_hard_token_decimal
        _key = f'{contract.get("symbol")}USD'
        _price_api = _prices[0].get(_key)
         
        if len(_prices) > 2:
            _price_api = _prices[2].get(_key)

        if not _price_api:
            _key = f'{contract.get("symbol")}USDT'
            _price_api = _prices[0].get(_key)

        _diff_amount =  _price_smc - float(_price_api)
        _percent_diff = abs(_diff_amount)/_price_smc
        print("DIFF: ", _diff_amount, " PERCENT:", _percent_diff)
        if _percent_diff > float(DefaultConfig.PERCENT_DIFF_WARNING):
            
            _message = f'''<pre>
😡😡😡❗❗❗😥😥😥
SYMBOL     : {contract.get("symbol")}
CONTRACT   : {round(float(_price_smc), 10)}
API        : {round(float(_price_api), 10)}
PERCENT    : {round(float(_percent_diff)*100, 5)}
                        </pre>'''    
            
            send_notify_telegram(_message)
    
def send_notify_telegram( message_notify, channel=DefaultConfig.NOTIFY_CHANNEL_ORDER_ADMIN):
    
    _body = {
        "chat_id" : channel,
        "text" : message_notify,
        "parse_mode" : "HTML"
    }

    url = f'https://api.telegram.org/bot{DefaultConfig.TOKEN_BOT_ORDER}/sendMessage'
    
    response = requests.request(method="POST", url=url,
                                data=_body,
                                timeout=10,
                                verify=False)
    if response.status_code == 200:
        print("send_notify_telegram", _body)    
    
             
                