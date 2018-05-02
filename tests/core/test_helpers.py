import logging
import os

from nesbi.core.helpers import deepupdate
from nesbi.core.helpers.logger import setup_logging


class Test(object):
    def test_deepupdate(self):
        dict_one = {'key1': 'value1', 'key2': {'key3': 'value3', 'key4': 'value4'}}
        dict_two = {'key1': 'value1', 'key2': {'key5': 'value5'}}

        dict_expected = {'key1': 'value1', 'key2': {'key3': 'value3', 'key4': 'value4',
                         'key5': 'value5'}}
        dict_deep_updated = deepupdate(dict_one, dict_two)

        assert(dict_deep_updated == dict_expected)

    def test_logger_level_debug(self):
        setup_logging('debug', '', True)
        logger = logging.getLogger('nesbi.test')

        assert(logging.getLevelName(logger.getEffectiveLevel()) == 'DEBUG')

    def test_logger_level_info(self):
        setup_logging('info', '', True)
        logger = logging.getLogger('nesbi.test')

        assert(logging.getLevelName(logger.getEffectiveLevel()) == 'INFO')

    def test_logger_file(self):
        setup_logging('info', 'test.log', False)
        logger = logging.getLogger('nesbi.test')
        logger.info('testlog')
        content = None

        with open('test.log') as f:
            content = f.read()

        os.remove('test.log')
        assert('INFO - testlog' in content)
