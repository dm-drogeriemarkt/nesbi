import os

import yaml

ATTRIBUTES = [('nesbi_username', ''),
              ('nesbi_password', ''),
              ('nesbi_dry_run', False),
              ('nsot_url', ''),
              ('nsot_email', ''),
              ('nsot_secret_key', ''),
              ('nsot_auth_header', 'X-NSoT-Email'),
              ('nsot_site_id', '1'),
              ('nsot_delete_objects', False),
              ('nesbi_snmp_version', '2c'),
              ('nesbi_snmp_community', ''),
              ('nesbi_scan_ports', [22]),
              ('nesbi_logging_level', 'info'),
              ('nesbi_logging_file', 'nesbi.log'),
              ('nesbi_logging_to_stdout', False),
              ('nesbi_thread_limit', 5)]


class Config:
    def __init__(self, config_file, **kwargs):
        with open(config_file, 'r') as f:
            data = yaml.load(f.read()) or {}

        for k, v in data.items():
                setattr(self, k, v)

        for attr in ATTRIBUTES:
            self._set_self_attribute(attr[0], attr[1], **kwargs)

    def _set_self_attribute(self, attr, default, **kwargs):
        if kwargs.get(attr):
            setattr(self, attr, kwargs.get(attr))
        elif hasattr(self, attr):
            setattr(self, attr, getattr(self, attr))
        elif attr.upper() in os.environ:
            setattr(self, attr, os.environ.get(attr.upper()))
        else:
            setattr(self, attr, default)
