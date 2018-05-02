import logging
import queue
import socket
import threading
import time
from ipaddress import IPv4Address, ip_network

import napalm

from nelsnmp.errors import SnmpError
from nelsnmp.hostinfo.device import HostInfo
from nelsnmp.snmp import SnmpHandler

from nesbi.core.helpers import deepupdate

from netmiko.ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException


class NetworkScanner(object):
    def __init__(self, networks, username, password, snmp_version, snmp_community,
                 scan_ports, thread_limit):
        self.logger = logging.getLogger(__name__)
        self.networks = networks
        self.username = username
        self.password = password
        self.snmp_version = snmp_version
        self.snmp_community = snmp_community
        self.scan_ports = scan_ports
        self.thread_limit = thread_limit
        self.devices = self._get_network_devices()

    def _get_hosts_in_network(self):
        hosts = dict()

        for k, v in self.networks.items():
            if v.get('range')[-3:] == '/32':
                hosts[k] = list([IPv4Address(v.get('range')[:-3])])

            else:
                hosts[k] = list(ip_network(v.get('range')).hosts())

                if v.get('exclude'):
                    for e in v.get('exclude'):
                        if IPv4Address(e) in hosts[k]:
                            hosts[k].remove(IPv4Address(e))

        return hosts

    def _get_reachable_devices(self):
        hosts = self._get_hosts_in_network()
        reachable_devices = dict()

        for k, v in hosts.items():
            self.logger.info(f'Start port-scan for network/location {k}')

            reachable_devices[k] = list()
            threads = list()
            q = queue.Queue()
            s = threading.Semaphore(self.thread_limit)

            for host in v:
                threads.append(threading.Thread(target=self._thread_get_reachable_devices,
                                                args=(s, str(host), q)))
                threads[-1].start()

            for t in threads:
                t.join()

            while not q.empty():
                reachable_devices[k].append(q.get())

        return reachable_devices

    def _thread_get_reachable_devices(self, s, ip, q):
        already_reachable = False

        with s:
            threading.Lock()

            for tcp_port in self.scan_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.15)
                    sock.connect((ip, tcp_port))
                    self.logger.info(f'{ip} reachable at tcp-port {tcp_port}')

                    if not already_reachable:
                        q.put(ip)
                        already_reachable = True

                except socket.error as e:
                    self.logger.debug(f'{ip} not reachable at tcp-port {tcp_port}')
                    pass

                sock.close()

    def _get_network_devices(self):
        hosts = self._get_reachable_devices()
        ios_devices = dict()

        for k, v in hosts.items():
            self.logger.info(f'Start device-scan for network/location {k}')
            ios_devices[k] = list()
            threads = list()
            q = queue.Queue()
            s = threading.Semaphore(self.thread_limit)

            for host in v:
                threads.append(threading.Thread(target=self._thread_get_device_facts,
                                                args=(s, host, q)))
                threads[-1].start()

            for t in threads:
                t.join()

            while not q.empty():
                ios_devices[k].append(q.get())

        return ios_devices

    def _thread_get_device_facts(self, s, host, q):
        ip = str(host)
        os = self._get_device_os(ip)

        with s:
            threading.Lock()

            if os != 'UNKNOWN':
                driver = napalm.get_network_driver(os)
                facts = dict()

                time.sleep(0.15)

                try:
                    with driver(hostname=ip, username=self.username,
                                password=self.password) as device:
                        facts = device.get_facts()
                        interfaces = device.get_interfaces()
                        interfaces_ip = device.get_interfaces_ip()
                        snmp = device.get_snmp_information()

                        first_merge = deepupdate(facts, snmp)
                        second_merge = deepupdate(interfaces, interfaces_ip)
                        final_merge = deepupdate(first_merge, second_merge)

                        q.put(final_merge)
                        self.logger.info(f"{facts.get('hostname')} scanned with napalm")

                except NetMikoAuthenticationException as e:
                    self.logger.error(f"{facts.get('hostname') or ip}: auth failed")

                except NetMikoTimeoutException as e:
                    self.logger.error(f"{facts.get('hostname') or ip}: socket-timeout")

                except napalm.base.exceptions.ConnectionClosedException as e:
                    self.logger.error(f"{facts.get('hostname') or ip}: {e}")

                except ValueError as e:
                    self.logger.error(f"{facts.get('hostname') or ip}: {e}")

    def _get_device_os(self, ip):
        dev = SnmpHandler(host=ip, version=self.snmp_version, community=self.snmp_community)
        hostinfo = HostInfo(dev)

        try:
            hostinfo.get_version()
            self.logger.info(f'{ip}: detected os "{hostinfo.os}"')
        except SnmpError as e:
            self.logger.error(f'{ip}: snmp-timeout')
            return False

        return hostinfo.os
