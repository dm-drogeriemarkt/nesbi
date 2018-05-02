import logging.config


def setup_logging(logging_level, logging_file, logging_to_stdout):
    dict_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {'normal': {'format':
                                  '%(asctime)s - %(name)25s - %(levelname)8s - %(message)s'}},
        'handlers': {},
        'loggers': {},
    }

    handlers = list()

    if logging_file:
        handlers.append('info_file_handler')
        dict_config['handlers']['info_file_handler'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'NOTSET',
            'formatter': 'normal',
            'filename': logging_file,
            'maxBytes': 20971520,
            'backupCount': 10,
            'encoding': 'utf8',
        }

    if logging_to_stdout:
        handlers.append('info_console')
        dict_config['handlers']['info_console'] = {
            'class': 'logging.StreamHandler',
            'level': 'NOTSET',
            'formatter': 'normal',
            'stream': 'ext://sys.stdout',
        }

    dict_config['loggers']['nesbi'] = {'level': logging_level.upper(),
                                       'handlers': handlers}

    if handlers:
        logging.config.dictConfig(dict_config)
