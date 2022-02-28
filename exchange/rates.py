import re
import requests
from typing import Union
from exchange.logger import logger
from exchange.cache import Cache

class Exchanger:


    def __init__(self, base_url: str='https://api.exchangerate.host/', target: str='EUR'):
        self.Cache = Cache()
        self.url = base_url
        self.target = target


    @staticmethod
    def get_date(date: str) -> str:
        '''
        regex for date resolving
        '''
        _pattern = r'\d{4}-\d{2}-\d{2}'

        return re.findall(_pattern, date)[0]


    def _refetch_rate(self, base: str, date: str) -> float:
        '''
        used internally if cache empty
        fetches the desired rate
        '''
        url_queries = f'?base={base}&symbols={self.target}'
        url = self.url + date + '/' + url_queries
        # this can raise an error
        res = requests.get(url).json()
        rates = res.get('rates')
        # api specific behavior: returns target as a base if currency not found, thus:
        if (rate := rates.get(self.target)) and res.get('base') == base:
            # cache result
            self.Cache.set(f'{base}-{self.target}-{date}', rate)
            return rate

        # failed
        logger.debug('Rate for params %s, %s not found', base, date)
        raise ValueError('No valid data for given params')


    def _check_cache(self, base: str, date: str) -> float:
        '''
        checks if the requested rate is present
        in the local cache
        '''
        lookup_string = f'{base}-{self.target}-{date}'
        if not (rate := self.Cache.get(lookup_string)):
            return 0 # lets assume no rate will ever be 0

        return rate


    def _get_rate(self, base:str, date: str) -> float:
        '''
        attempts to find a rate either in the cache,
        or online
        '''
        if not (cached_rate := self._check_cache(base=base, date=date)):
            fresh_rate = self._refetch_rate(base=base, date=date)

            return fresh_rate

        return cached_rate


    def calculate(self, payload: dict) -> Union[dict, str]:
        '''
        external entrypoint for stake calculation
        '''
        # get the rate
        attrs = [
            'marketId',
            'selectionId',
            'odds',
            'stake',
            'currency',
            'date',
        ]
        # check if all attrs are present
        if not all(attr in payload.keys() for attr in attrs):
            return 'Invalid payload format'

        strip_date = self.get_date(payload['date'])
        try:
            rate = self._get_rate(base=payload['currency'], date=strip_date)
        except Exception as e:
            logger.warning('Exception while trying to get a rate: %s', e)
            return e

        payload['currency'] = self.target
        payload['stake'] = round(payload['stake'] * rate, 5)

        return payload
