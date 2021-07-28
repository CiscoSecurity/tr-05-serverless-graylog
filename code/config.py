import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']

    USER_AGENT = ('SecureX Threat Response Integrations '
                  '<tr-integrations-support@cisco.com>')

    GRAYLOG_API_ENDPOINT = 'https://{host}/api/'
    REQUESTED_BY = 'SecureX Threat Response'

    SUPPORTED_TYPES = {
        'ip': 'IP',
        'ipv6': 'IPv6',
        'device': 'device',
        'user': 'user',
        'domain': 'domain',
        'sha256': 'SHA256',
        'md5': 'MD5',
        'sha1': 'SHA1',
        'url': 'URL',
        'pki_serial': 'PKI serial',
        'email': 'email',
        'imei': 'IMEI',
        'imsi': 'IMSI',
        'amp_computer_guid': 'AMP computer GUID',
        'hostname': 'hostname',
        'mac_address': 'MAC address',
        'file_name': 'file name',
        'file_path': 'file path',
        'odns_identity': 'ODNS identity',
        'odns_identity_label': 'ODNS identity label',
        'email_messageid': 'email message ID',
        'email_subject': 'email subject',
        'cisco_mid': 'Cisco message ID',
        'mutex': 'mutex',
    }

    CTR_DEFAULT_ENTITIES_LIMIT = 100
