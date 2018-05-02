from nesbi.core.configuration import Config
from nesbi.core.helpers.logger import setup_logging
from nesbi.core.nsot import NSOTCmdb
from nesbi.core.scanner import NetworkScanner


class Nesbi(object):
    def __init__(self, config_file, **kwargs):
        self.config = Config(config_file, **kwargs)

        setup_logging(self.config.nesbi_logging_level, self.config.nesbi_logging_file,
                      self.config.nesbi_logging_to_stdout)

        self.attr_functions = kwargs.get('attr_functions', [])
        self.import_data = list()

        scanner = NetworkScanner(self.config.networks, self.config.nesbi_username,
                                 self.config.nesbi_password, self.config.nesbi_snmp_version,
                                 self.config.nesbi_snmp_community, self.config.nesbi_scan_ports,
                                 self.config.nesbi_thread_limit)

        self.scan_data = scanner.devices

    def generate_import_data(self):
        for location in self.scan_data:
            devices = self.scan_data.get(location)

            for device in devices:
                import_data = {}
                import_data['attributes'] = {}
                import_data['site_id'] = self.config.nsot_site_id
                import_data['hostname'] = device.get('hostname')

                try:
                    for k, v in self.config.napalm.items():
                        import_data['attributes'][k] = device.get(v)
                except AttributeError as e:
                    pass

                try:
                    for k, v in self.config.types.get(device.get('model')).items():
                        import_data['attributes'][k] = v
                except AttributeError as e:
                    pass

                try:
                    for k, v in self.config.attr_functions.items():
                        func = next(x for x in self.attr_functions if x.__name__ == v)
                        import_data['attributes'][k] = func(device)
                except AttributeError as e:
                    pass

                try:
                    for k, v in self.config.networks.get(location).get('attributes').items():
                        import_data['attributes'][k] = v
                except AttributeError as e:
                    pass

                self.import_data.append(import_data)

    def process_import_data(self):
        cmdb = NSOTCmdb(self.config.nsot_url, self.config.nsot_email, self.config.nsot_secret_key,
                        self.config.nsot_auth_header, self.config.nsot_site_id,
                        self.config.nsot_delete_objects)

        cmdb.import_data(self.import_data, self.config.nesbi_dry_run)
