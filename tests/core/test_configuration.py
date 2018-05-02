import os

from nesbi.core.configuration import Config


dir_path = os.path.dirname(os.path.realpath(__file__))
config_file = f'{dir_path}/../../examples/config.yml'


class Test(object):
    def test_config_file_only(self):
        config = Config(config_file)

        for k, v in config.networks.items():
            assert(k == 'mylocation' or k == 'mylocation2')
            assert(v.get('range') == '192.168.0.0/25' or v.get('range') == '192.168.0.1/25')

        assert(config.networks.get('mylocation2').get('attributes').get('owner_person') == 'myself')

        assert(config.nsot_url == 'http://nsot.local/api')
        assert(config.nsot_email == 'nsotuser@example.com')
        assert(config.nsot_secret_key == 12345)
        assert(config.nsot_site_id == '1')
        assert(config.nsot_update_objects is False)
        assert(config.nesbi_snmp_community == 'mycomm')

    def test_config_kwargs(self):
        config = Config(config_file, nsot_site_id='2', nsot_email='kwarg@overwritten.com')

        assert(config.nsot_secret_key == 12345)
        assert(config.nsot_site_id == '2')
        assert(config.nsot_email == 'kwarg@overwritten.com')

    def test_config_env(self):
        os.environ['NESBI_LOGGING_LEVEL'] = 'debug'
        config = Config(config_file)

        assert(config.nsot_secret_key == 12345)
        assert(config.nesbi_logging_level == 'debug')

    def test_config_kwargs_env(self):
        os.environ['NESBI_LOGGING_LEVEL'] = 'debug'
        config = Config(config_file, nesbi_logging_level='warning')

        assert(config.nesbi_logging_level == 'warning')
