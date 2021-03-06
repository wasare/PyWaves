# Copyright (C) 2017 PyWaves Developers
#
# This file is part of PyWaves.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from __future__ import absolute_import, division, print_function, unicode_literals

DEFAULT_TX_FEE = 100000
DEFAULT_ASSET_FEE = 100000000
DEFAULT_MATCHER_FEE = 100000
DEFAULT_LEASE_FEE = 100000
DEFAULT_ALIAS_FEE = 100000
VALID_TIMEFRAMES = (5, 15, 30, 60, 240, 1440)
MAX_WDF_REQUEST = 100

import requests
import threading

from .address import *
from .asset import *
from .order import *

NODE = 'https://nodes.wavesnodes.com'
CHAIN = 'mainnet'
CHAIN_ID = 'W'
PYWAVES_DIR='/Users/paolo/.pywaves'
MATCHER = 'https://nodes.wavesnodes.com'
MATCHER_PUBLICKEY = ''

DATAFEED = 'http://marketdata.wavesplatform.com'

logging.getLogger("requests").setLevel(logging.WARNING)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def setNode(node = NODE, chain = CHAIN):
    global NODE, CHAIN, CHAIN_ID
    NODE = node
    if chain.lower()=='mainnet' or chain.lower()=='w':
        CHAIN = 'mainnet'
        CHAIN_ID = 'W'
    else:
        CHAIN = 'testnet'
        CHAIN_ID = 'T'
    logging.info('Connecting to %s node %s' % (CHAIN, NODE))

def setMatcher(node = MATCHER):
    global MATCHER, MATCHER_PUBLICKEY
    try:
        MATCHER_PUBLICKEY = wrapper('/matcher', host = node)
        MATCHER = node
        logging.info('Setting matcher %s %s' % (MATCHER, MATCHER_PUBLICKEY))
    except:
        MATCHER_PUBLICKEY = ''

def setDatafeed(wdf = DATAFEED):
    global DATAFEED
    DATAFEED = wdf
    logging.info('Setting datafeed %s ' % (DATAFEED))

def wrapper(api, postData='', host='', headers=''):
    if not host:
        host = NODE
    if postData:
        req = requests.post('%s%s' % (host, api), data=postData, headers={'content-type': 'application/json'}).json()
    else:
        req = requests.get('%s%s' % (host, api), headers=headers).json()
    return req

def height():
    return wrapper('/blocks/height')['height']

def lastblock():
    return wrapper('/blocks/last')

def block(n):
    return wrapper('/blocks/at/%d' % n)

def tx(id):
    return wrapper('/transactions/info/%s' % id)

def getOrderBook(assetPair):
    req = wrapper('/matcher/orderBook?asset1=%s&asset2=%s' % (assetPair.asset1, assetPair.asset2), '', host = 'http://%s:%s' % (pywaves.MATCHER_HOST, pywaves.MATCHER_PORT))
    try:
        bids = req['bids']
        asks = req['asks']
    except:
        bids = ''
        asks = ''
    return bids, asks

def symbols():
    return wrapper('/api/symbols', host=DATAFEED)

def markets():
    return wrapper('/api/markets', host = DATAFEED)

def matchers():
    return wrapper('/api/matchers', host = DATAFEED)

def loadSymbols():
    try:
        for s in symbols():
            setattr(pywaves, s['symbol'], Asset(s['assetID']))
    except:
        pass

setNode()
WAVES = Asset('')
t = threading.Thread(target=loadSymbols)
t.daemon = True
t.start()


