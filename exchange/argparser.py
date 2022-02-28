import logging
import os
from argparse import ArgumentParser, ArgumentTypeError
from exchange.version import __version__, APP_NAME

LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
LOG_LEVEL_DEFAULT = 'INFO'
LOG_VERBOSE_DEFAULT = False


def log_level_string_to_int(arg_string: str) -> int:
    '''
    gets log level int from string
    '''

    log_level_string = arg_string.upper()
    if log_level_string not in LOG_LEVEL_STRINGS:
        message = (f'invalid choice: {log_level_string} '
                   f'(choose from {LOG_LEVEL_STRINGS})')
        raise ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.INFO)
    assert isinstance(log_level_int, int)

    return log_level_int


def get_pars():
    '''
    looks for pars in the environment
    '''
    env_vars = {
        'LOG_LEVEL': {
            'default': LOG_LEVEL_DEFAULT
        },
    }

    # defaults overriden from ENVs
    for env_var, env_pars in env_vars.items():
        if env_var in os.environ:
            default = os.environ[env_var]
            if 'default' in env_pars:
                if isinstance(env_pars['default'], bool):
                    default = bool(os.environ[env_var])
                elif isinstance(env_pars['default'], int):
                    default = int(os.environ[env_var])
            env_pars['default'] = default
            env_pars['required'] = False

    parser = ArgumentParser(description=f'{APP_NAME} {__version__}')

    parser.add_argument('-V',
                        '--version',
                        action='version',
                        version=str(__version__))

    parser.add_argument('-l',
                        '--log-level',
                        action='store',
                        dest='log_level',
                        help=('set the logging output level. '
                              f'{LOG_LEVEL_STRINGS} '
                              f'(default {LOG_LEVEL_DEFAULT})'),
                        type=log_level_string_to_int,
                        **env_vars['LOG_LEVEL'])

    return parser.parse_args()

# get parameters from command line arguments
pars = get_pars()
