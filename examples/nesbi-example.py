from nesbi.core import Nesbi


def get_monitoring_interfaces(device):
    monitoring_interfaces = list()
    interfaces_list = device.get('interface_list')
    for interface in interfaces_list:
        if device.get(interface).get('description') == "##UPLINK##":
            monitoring_interfaces.append(interface)

    return monitoring_interfaces


def main():
    config_file = 'config.yaml'

    attr_functions = [get_monitoring_interfaces]
    nesbi = Nesbi(config_file, attr_functions=attr_functions, nesbi_dry_run=True,
                  nesbi_sername="usr", nesbi_password="pw")
    nesbi.generate_import_data()
    nesbi.process_import_data()


if __name__ == "__main__":
    main()
