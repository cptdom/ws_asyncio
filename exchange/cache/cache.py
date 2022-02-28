import time


class Cache:
    '''
    Simple cache object
    default ttl: two hours
    '''
    def __init__(self, ttl=7200.0):
        self.data = {}
        self.ttl = ttl


    def _cleanup(self):
        '''
        remove old keys
        '''
        for key in self.data.keys():
            if self.data[key]['valid_until'] < time.time():
                del self.data[key]


    def set(self, key: str, data: object, ttl=None):
        '''
        set object 'data' to the cache under the key 'key'
        '''

        if ttl is None:
            ttl = self.ttl

        tmp = {}
        tmp['data'] = data
        tmp['valid_until'] = ttl + time.time()
        self.data[key] = tmp


    def get(self, key: str) -> object:
        '''
        return object stored under the key 'key'
        or returns None
        '''
        # check ttls
        self._cleanup()

        if key in self.data:
            return self.data[key]['data']

        return None
