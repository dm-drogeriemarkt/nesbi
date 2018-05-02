import json
import logging

import requests


class NSOTCmdb(object):
    def __init__(self, nsot_url, nsot_email, nsot_secret_key, nsot_auth_header,
                 nsot_site_id, nsot_delete_objects):
        self.logger = logging.getLogger(__name__)

        if nsot_secret_key:
            data = {'email': nsot_email, 'secret_key': nsot_secret_key}
            res = requests.post(f'{nsot_url}/authenticate/', data=data)
            auth_token = res.json().get('auth_token')
            headers = {'Authorization': f'AuthToken {nsot_email}:{auth_token}'}

        else:
            headers = {nsot_auth_header: nsot_email}

        headers['content-type'] = 'application/json'
        self.headers = headers
        self.nsot_url = nsot_url
        self.nsot_site_id = nsot_site_id
        self.nsot_delete_objects = nsot_delete_objects

    def import_data(self, data, dry_run):
        for d in data:
            self.logger.debug(f"data for {d.get('hostname')}:")
            self.logger.debug(d)

            if dry_run:
                self.logger.info(f"{d.get('hostname')} create dry-run")

            else:
                if self.nsot_delete_objects:
                    self._delete_data(d)

                self._create_data(d)

    def _create_data(self, d):
        response = requests.post(f'{self.nsot_url}/devices/',
                                 data=json.dumps(d), headers=self.headers, verify=False)

        status_code = response.status_code

        if status_code == 201:
            self.logger.info(f"{d.get('hostname')} created")
        elif status_code == 400:
            self.logger.warning(f"{d.get('hostname')} already in nsot or wrong attributes")
        else:
            self.logger.error(f"{d.get('hostname')} with problems, status-code:{status_code}")

    def _delete_data(self, d):
        h = d.get("hostname")
        response = requests.delete(f'{self.nsot_url}/sites/{self.nsot_site_id}/devices/{h}/',
                                   data=json.dumps(d), headers=self.headers, verify=False)

        status_code = response.status_code

        if status_code == 204:
            self.logger.info(f"{d.get('hostname')} deleted")
        elif status_code == 400:
            self.logger.warning(f"{d.get('hostname')} wrong attributes")
        else:
            self.logger.error(f"{d.get('hostname')} with problems, status-code: {status_code}")
