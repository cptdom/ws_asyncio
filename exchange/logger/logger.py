''' custom logger setup '''

import logging
from exchange.argparser import pars

class ConfLogger:
    '''
    basic logger config
    '''
    def __init__(self, name, log_level=logging.INFO):
        '''
        '''
        handlers = [
            logging.StreamHandler(),
        ]

        logging.basicConfig(format='%(asctime)s: %(module)s @ %(levelname)s:'
                            ' %(message)s',
                            level=log_level,
                            handlers=handlers,
                            datefmt='%m/%d/%Y %I:%M:%S')

        self.logger = logging.getLogger(name)

    def get_logger(self):
        '''
        '''
        return self.logger

cl = ConfLogger(__name__, log_level=pars.log_level)
logger = cl.get_logger()
